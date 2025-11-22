---
name: rust-backend-patterns
description: Rust/Actix-web patterns, error handling, auth middleware, and repository patterns for T2 backend. Use when implementing backend endpoints, handlers, or services.
license: MIT
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  token-efficiency: "Endpoint patterns reduce implementation time 50% (40→20 min)"
  integration: "Orchestrator Phase 3 - Backend implementation with Actix-web"
  tech-stack: "Rust 1.70+, Actix-web 4.x, JWT auth, FoundationDB 7.1+"
---

# Rust Backend Patterns

Expert skill for Rust/Actix-web development in the T2 backend (GCP-deployed API).

## When to Use

✅ **Use this skill when:**
- Implementing new REST API endpoints (GET, POST, PUT, DELETE)
- Adding authentication middleware or authorization logic
- Creating custom error types and error handling patterns
- Writing repository methods for FDB data access
- Setting up CORS, rate limiting, or other middleware
- Structuring Actix-web handlers with proper dependency injection
- Writing integration tests for backend endpoints
- Need time savings: 50% faster endpoint implementation (40→20 min)

❌ **Don't use this skill when:**
- Working on frontend-only features (use React/TypeScript patterns)
- Debugging FDB queries (use foundationdb-queries skill)
- Deploying to GKE (use build-deploy-workflow skill)
- Writing production error handling (use production-patterns skill for circuit breakers)

## Handler Pattern

```rust
// backend/src/handlers/*.rs
use actix_web::{web, HttpResponse};
use crate::db::FDBService;
use crate::middleware::Claims;

#[post("/api/v5/resource")]
async fn create_resource(
    claims: Claims,  // JWT auth - always required!
    data: web::Json<CreateResourceRequest>,
    fdb: web::Data<FDBService>,
) -> Result<HttpResponse, ApiError> {
    // 1. Extract tenant from claims (auto-validated by middleware)
    let tenant_id = claims.tenant_id;

    // 2. Use repository pattern
    let resource = fdb.resources()
        .create_with_tenant(tenant_id, data.into_inner())
        .await?;

    // 3. Return success
    Ok(HttpResponse::Created().json(resource))
}
```

## Error Handling Pattern

```rust
// Use map_err() for TransactionCommitError
trx.commit().await.map_err(|e| {
    ApiError::DatabaseError(format!("Failed to commit: {:?}", e))
})?;
```

## Auth Middleware

**ALL endpoints** except `/health` and `/ready` require JWT:

```rust
// Automatically validates JWT and provides Claims
async fn handler(claims: Claims) -> Result<HttpResponse, ApiError> {
    let tenant_id = claims.tenant_id;  // ✅ Validated
    let user_id = claims.user_id;      // ✅ Validated
    // ...
}
```

## Repository Pattern

**NEVER** use FDB directly. Always use repositories:

```rust
// ✅ CORRECT
let user = fdb.users().get_by_id(&tenant_id, &user_id).await?;

// ❌ WRONG
let key = format!("/{}/users/{}", tenant_id, user_id);
let value = trx.get(&key.as_bytes()).await?;
```

## Complete CRUD Endpoint Patterns

### GET - Retrieve Single Resource

```rust
// backend/src/handlers/users.rs
use actix_web::{get, web, HttpResponse};
use crate::middleware::Claims;
use crate::db::repositories::UserRepository;

#[get("/api/v5/users/{user_id}")]
async fn get_user(
    claims: Claims,
    path: web::Path<Uuid>,
    db: web::Data<Database>,
) -> Result<HttpResponse, ApiError> {
    let user_id = path.into_inner();
    let tenant_id = claims.tenant_id;

    // Repository pattern with tenant isolation
    match UserRepository::get(&db, &tenant_id, &user_id).await? {
        Some(user) => Ok(HttpResponse::Ok().json(user)),
        None => Err(ApiError::NotFound(format!("User {} not found", user_id))),
    }
}
```

### GET - List Resources with Pagination

```rust
#[derive(Deserialize)]
struct ListUsersQuery {
    #[serde(default = "default_limit")]
    limit: usize,
    #[serde(default)]
    offset: usize,
}

fn default_limit() -> usize { 50 }

#[get("/api/v5/users")]
async fn list_users(
    claims: Claims,
    query: web::Query<ListUsersQuery>,
    db: web::Data<Database>,
) -> Result<HttpResponse, ApiError> {
    let tenant_id = claims.tenant_id;

    let users = UserRepository::list_by_tenant(&db, &tenant_id).await?;

    // Apply pagination
    let total = users.len();
    let paginated: Vec<_> = users
        .into_iter()
        .skip(query.offset)
        .take(query.limit)
        .collect();

    Ok(HttpResponse::Ok().json(json!({
        "users": paginated,
        "total": total,
        "limit": query.limit,
        "offset": query.offset,
    })))
}
```

### POST - Create Resource

```rust
#[derive(Deserialize, Validate)]
struct CreateUserRequest {
    #[validate(email)]
    email: String,
    #[validate(length(min = 8))]
    password: String,
    #[validate(length(min = 1, max = 100))]
    name: String,
}

#[post("/api/v5/users")]
async fn create_user(
    claims: Claims,
    data: web::Json<CreateUserRequest>,
    db: web::Data<Database>,
) -> Result<HttpResponse, ApiError> {
    // 1. Validate input
    data.validate()
        .map_err(|e| ApiError::ValidationError(format!("{}", e)))?;

    // 2. Extract tenant from claims
    let tenant_id = claims.tenant_id;

    // 3. Create via repository
    let user = UserRepository::create(&db, &tenant_id, &data.into_inner()).await?;

    // 4. Return 201 Created
    Ok(HttpResponse::Created().json(user))
}
```

### PUT - Update Resource

```rust
#[derive(Deserialize, Validate)]
struct UpdateUserRequest {
    #[validate(length(min = 1, max = 100))]
    name: Option<String>,
    #[validate(email)]
    email: Option<String>,
}

#[put("/api/v5/users/{user_id}")]
async fn update_user(
    claims: Claims,
    path: web::Path<Uuid>,
    data: web::Json<UpdateUserRequest>,
    db: web::Data<Database>,
) -> Result<HttpResponse, ApiError> {
    data.validate()
        .map_err(|e| ApiError::ValidationError(format!("{}", e)))?;

    let user_id = path.into_inner();
    let tenant_id = claims.tenant_id;

    // Check if user exists and belongs to tenant
    let mut user = UserRepository::get(&db, &tenant_id, &user_id).await?
        .ok_or_else(|| ApiError::NotFound(format!("User {} not found", user_id)))?;

    // Apply updates
    if let Some(name) = &data.name {
        user.name = name.clone();
    }
    if let Some(email) = &data.email {
        user.email = email.clone();
    }

    // Save changes
    let updated_user = UserRepository::update(&db, &tenant_id, &user_id, user).await?;

    Ok(HttpResponse::Ok().json(updated_user))
}
```

### DELETE - Remove Resource

```rust
#[delete("/api/v5/users/{user_id}")]
async fn delete_user(
    claims: Claims,
    path: web::Path<Uuid>,
    db: web::Data<Database>,
) -> Result<HttpResponse, ApiError> {
    let user_id = path.into_inner();
    let tenant_id = claims.tenant_id;

    // Verify user exists before deleting
    UserRepository::get(&db, &tenant_id, &user_id).await?
        .ok_or_else(|| ApiError::NotFound(format!("User {} not found", user_id)))?;

    // Delete
    UserRepository::delete(&db, &tenant_id, &user_id).await?;

    // Return 204 No Content
    Ok(HttpResponse::NoContent().finish())
}
```

## Custom Error Types

```rust
// backend/src/error.rs
use actix_web::{error::ResponseError, http::StatusCode, HttpResponse};
use derive_more::{Display, Error};

#[derive(Debug, Display, Error)]
pub enum ApiError {
    #[display(fmt = "Not found: {}", _0)]
    NotFound(String),

    #[display(fmt = "Validation error: {}", _0)]
    ValidationError(String),

    #[display(fmt = "Unauthorized: {}", _0)]
    Unauthorized(String),

    #[display(fmt = "Forbidden: {}", _0)]
    Forbidden(String),

    #[display(fmt = "Database error: {}", _0)]
    DatabaseError(String),

    #[display(fmt = "Internal server error: {}", _0)]
    InternalError(String),
}

impl ResponseError for ApiError {
    fn error_response(&self) -> HttpResponse {
        let (status, message) = match self {
            ApiError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
            ApiError::ValidationError(msg) => (StatusCode::BAD_REQUEST, msg),
            ApiError::Unauthorized(msg) => (StatusCode::UNAUTHORIZED, msg),
            ApiError::Forbidden(msg) => (StatusCode::FORBIDDEN, msg),
            ApiError::DatabaseError(msg) => (StatusCode::INTERNAL_SERVER_ERROR, "Database error"),
            ApiError::InternalError(msg) => (StatusCode::INTERNAL_SERVER_ERROR, "Internal error"),
        };

        HttpResponse::build(status).json(json!({
            "error": message,
            "status": status.as_u16(),
        }))
    }

    fn status_code(&self) -> StatusCode {
        match self {
            ApiError::NotFound(_) => StatusCode::NOT_FOUND,
            ApiError::ValidationError(_) => StatusCode::BAD_REQUEST,
            ApiError::Unauthorized(_) => StatusCode::UNAUTHORIZED,
            ApiError::Forbidden(_) => StatusCode::FORBIDDEN,
            ApiError::DatabaseError(_) | ApiError::InternalError(_) => StatusCode::INTERNAL_SERVER_ERROR,
        }
    }
}

// Convert FDB errors to ApiError
impl From<FdbError> for ApiError {
    fn from(err: FdbError) -> Self {
        match err {
            FdbError::NotFound(msg) => ApiError::NotFound(msg),
            FdbError::TransactionError(msg) => ApiError::DatabaseError(msg),
            _ => ApiError::InternalError(format!("FDB error: {}", err)),
        }
    }
}
```

## Middleware Patterns

### CORS Configuration

```rust
// backend/src/main.rs
use actix_cors::Cors;

HttpServer::new(move || {
    // CORS middleware - configure for production
    let cors = Cors::default()
        .allowed_origin("https://coditect.ai")
        .allowed_origin("https://api.coditect.ai")
        .allowed_methods(vec!["GET", "POST", "PUT", "DELETE"])
        .allowed_headers(vec![
            actix_web::http::header::AUTHORIZATION,
            actix_web::http::header::CONTENT_TYPE,
        ])
        .max_age(3600);

    App::new()
        .wrap(cors)
        .wrap(middleware::Logger::default())
        .configure(configure_routes)
})
```

### Rate Limiting Middleware

```rust
// backend/src/middleware/rate_limit.rs
use actix_web::dev::{Service, ServiceRequest, ServiceResponse, Transform};
use std::sync::Arc;
use tokio::sync::Mutex;
use std::collections::HashMap;
use std::time::{Duration, Instant};

pub struct RateLimiter {
    requests: Arc<Mutex<HashMap<String, Vec<Instant>>>>,
    max_requests: usize,
    window: Duration,
}

impl RateLimiter {
    pub fn new(max_requests: usize, window: Duration) -> Self {
        Self {
            requests: Arc::new(Mutex::new(HashMap::new())),
            max_requests,
            window,
        }
    }

    pub async fn check(&self, key: &str) -> Result<(), ApiError> {
        let mut requests = self.requests.lock().await;
        let now = Instant::now();

        // Get or create entry
        let entry = requests.entry(key.to_string()).or_insert_with(Vec::new);

        // Remove expired requests
        entry.retain(|&req_time| now.duration_since(req_time) < self.window);

        // Check limit
        if entry.len() >= self.max_requests {
            return Err(ApiError::TooManyRequests(format!(
                "Rate limit exceeded: {} requests per {:?}",
                self.max_requests, self.window
            )));
        }

        // Add current request
        entry.push(now);
        Ok(())
    }
}
```

## Testing Patterns

### Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use actix_web::test;

    #[actix_web::test]
    async fn test_create_user_success() {
        let app = test::init_service(
            App::new().service(create_user)
        ).await;

        let req = test::TestRequest::post()
            .uri("/api/v5/users")
            .insert_header(("Authorization", "Bearer test_token"))
            .set_json(&json!({
                "email": "test@example.com",
                "password": "securepass123",
                "name": "Test User"
            }))
            .to_request();

        let resp = test::call_service(&app, req).await;
        assert_eq!(resp.status(), StatusCode::CREATED);
    }

    #[actix_web::test]
    async fn test_create_user_validation_error() {
        let app = test::init_service(
            App::new().service(create_user)
        ).await;

        let req = test::TestRequest::post()
            .uri("/api/v5/users")
            .insert_header(("Authorization", "Bearer test_token"))
            .set_json(&json!({
                "email": "invalid-email",  // ❌ Invalid email
                "password": "short",       // ❌ Too short
                "name": "Test User"
            }))
            .to_request();

        let resp = test::call_service(&app, req).await;
        assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
    }
}
```

### Integration Tests with Mock FDB

```rust
// tests/integration_test.rs
use actix_web::{test, App};

#[actix_web::test]
async fn test_user_crud_flow() {
    // Setup mock FDB
    let db = setup_test_db().await;

    let app = test::init_service(
        App::new()
            .app_data(web::Data::new(db))
            .service(create_user)
            .service(get_user)
            .service(update_user)
            .service(delete_user)
    ).await;

    // 1. Create user
    let create_req = test::TestRequest::post()
        .uri("/api/v5/users")
        .insert_header(("Authorization", "Bearer test_token"))
        .set_json(&json!({
            "email": "test@example.com",
            "password": "securepass123",
            "name": "Test User"
        }))
        .to_request();

    let create_resp = test::call_service(&app, create_req).await;
    assert_eq!(create_resp.status(), StatusCode::CREATED);
    let user: User = test::read_body_json(create_resp).await;

    // 2. Get user
    let get_req = test::TestRequest::get()
        .uri(&format!("/api/v5/users/{}", user.user_id))
        .insert_header(("Authorization", "Bearer test_token"))
        .to_request();

    let get_resp = test::call_service(&app, get_req).await;
    assert_eq!(get_resp.status(), StatusCode::OK);

    // 3. Update user
    let update_req = test::TestRequest::put()
        .uri(&format!("/api/v5/users/{}", user.user_id))
        .insert_header(("Authorization", "Bearer test_token"))
        .set_json(&json!({"name": "Updated Name"}))
        .to_request();

    let update_resp = test::call_service(&app, update_req).await;
    assert_eq!(update_resp.status(), StatusCode::OK);

    // 4. Delete user
    let delete_req = test::TestRequest::delete()
        .uri(&format!("/api/v5/users/{}", user.user_id))
        .insert_header(("Authorization", "Bearer test_token"))
        .to_request();

    let delete_resp = test::call_service(&app, delete_req).await;
    assert_eq!(delete_resp.status(), StatusCode::NO_CONTENT);
}
```

## Integration with T2 Orchestrator

**Orchestrator Phase 3: Backend Implementation**

When the orchestrator coordinates backend feature development, it uses this skill for Actix-web endpoints:

```
Orchestrator Phase 3: Backend Implementation
├─ Use rust-backend-patterns for endpoint structure ← THIS SKILL
├─ Use foundationdb-queries for data persistence
├─ Use production-patterns for error handling
└─ Validate with TDD validator (endpoint tests)
```

**Example Delegation:**
```
"Use rust-backend-patterns skill to implement user profile CRUD endpoints with JWT auth."
```

**Token Efficiency**: Endpoint patterns save 50% implementation time (40→20 min) by providing:
- Ready-to-adapt CRUD templates
- Proven error handling patterns
- Middleware configuration examples
- Testing patterns with mocks

## Troubleshooting

### Issue 1: JWT Middleware Not Applied

**Symptom:** Endpoints accessible without JWT token

**Cause:** Middleware not registered in App configuration

**Fix:** Ensure JWT middleware is registered before routes
```rust
// WRONG: Middleware registered after routes
App::new()
    .service(create_user)  // ❌ No JWT validation
    .wrap(JwtMiddleware::new());

// CORRECT: Middleware registered before routes
App::new()
    .wrap(JwtMiddleware::new())  // ✅ Applied to all routes
    .service(create_user);
```

### Issue 2: CORS Errors in Browser

**Symptom:** Frontend requests blocked with CORS error

**Cause:** Missing or incorrect CORS configuration

**Fix:** Configure CORS with correct origins
```rust
let cors = Cors::default()
    .allowed_origin("https://coditect.ai")  // ✅ Production domain
    .allowed_origin("http://localhost:5173")  // ✅ Dev server
    .allowed_methods(vec!["GET", "POST", "PUT", "DELETE"])
    .allowed_headers(vec![
        actix_web::http::header::AUTHORIZATION,
        actix_web::http::header::CONTENT_TYPE,
    ]);
```

### Issue 3: Request Body Deserialization Fails

**Symptom:**
```
Error: Json deserialize error: missing field `name`
```

**Cause:** Frontend sends different field names than backend expects

**Fix:** Use `#[serde(rename)]` or make fields optional
```rust
#[derive(Deserialize)]
struct CreateUserRequest {
    #[serde(rename = "userName")]  // ✅ Matches frontend
    name: String,

    // Or make optional
    name: Option<String>,
}
```

### Issue 4: Database Connection Pool Exhausted

**Symptom:**
```
Error: DatabaseError("Connection pool exhausted")
```

**Cause:** Too many concurrent requests or slow FDB transactions

**Fix:** Increase pool size or optimize transactions
```rust
// Increase pool size
let db = Database::new()
    .max_connections(50)  // ✅ Increased from default 10
    .connect().await?;

// Or optimize transactions (keep them short)
let user = UserRepository::get(&db, &tenant_id, &user_id).await?;
// Don't do heavy processing inside transaction
process_user_data(&user);  // ✅ Outside transaction
```

### Issue 5: Validation Errors Not Returned

**Symptom:** Validation fails but client gets 500 Internal Error

**Cause:** Validation errors not mapped to ApiError

**Fix:** Use `map_err` to convert validation errors
```rust
data.validate()
    .map_err(|e| ApiError::ValidationError(format!("{}", e)))?;
```
