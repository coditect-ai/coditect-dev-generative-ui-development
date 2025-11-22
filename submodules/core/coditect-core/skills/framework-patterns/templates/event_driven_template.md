# Event-Driven Architecture Template

## Event Definition

```rust
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Event {
    pub event_id: Uuid,
    pub timestamp: DateTime<Utc>,
    pub event_type: EventType,
    pub payload: serde_json::Value,
    pub metadata: EventMetadata,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum EventType {
    // Authentication events
    UserLoggedIn,
    UserLoggedOut,
    TokenRefreshed,
    SessionExpired,

    // Session events
    SessionCreated,
    SessionInvalidated,
    SessionExtended,

    // Workflow events
    WorkflowStarted,
    WorkflowStateChanged,
    WorkflowCompleted,
    WorkflowFailed,

    // Custom events
    Custom(String),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EventMetadata {
    pub correlation_id: Uuid,
    pub causation_id: Option<Uuid>,
    pub user_id: Option<Uuid>,
    pub tenant_id: Option<Uuid>,
    pub source: String,
}
```

## Event Producer

```rust
#[async_trait]
pub trait EventProducer: Send + Sync {
    async fn emit(&self, event: Event) -> Result<(), EventError>;
}

pub struct DefaultEventProducer {
    event_bus: Arc<EventBus>,
}

#[async_trait]
impl EventProducer for DefaultEventProducer {
    async fn emit(&self, event: Event) -> Result<(), EventError> {
        self.event_bus.publish(event).await
    }
}
```

## Event Consumer

```rust
#[async_trait]
pub trait EventConsumer: Send + Sync {
    async fn handle(&self, event: Event) -> Result<(), EventError>;
    fn event_types(&self) -> Vec<EventType>;
    fn name(&self) -> &str;
}

// Example: Audit Logger
pub struct AuditLogger {
    fdb: Arc<FDBService>,
}

#[async_trait]
impl EventConsumer for AuditLogger {
    async fn handle(&self, event: Event) -> Result<(), EventError> {
        // Log to FDB audit table
        let audit_entry = AuditEntry {
            audit_id: Uuid::new_v4(),
            event_id: event.event_id,
            event_type: format!("{:?}", event.event_type),
            timestamp: event.timestamp,
            payload: event.payload,
            metadata: event.metadata,
        };

        self.fdb.audit()
            .create(&audit_entry)
            .await
            .map_err(|e| EventError::ConsumerFailed(e.to_string()))?;

        Ok(())
    }

    fn event_types(&self) -> Vec<EventType> {
        vec![
            EventType::UserLoggedIn,
            EventType::UserLoggedOut,
            EventType::SessionInvalidated,
        ]
    }

    fn name(&self) -> &str {
        "AuditLogger"
    }
}

// Example: Metrics Collector
pub struct MetricsCollector;

#[async_trait]
impl EventConsumer for MetricsCollector {
    async fn handle(&self, event: Event) -> Result<(), EventError> {
        match event.event_type {
            EventType::UserLoggedIn => {
                increment_counter("user_logins_total").await;
            }
            EventType::SessionExpired => {
                increment_counter("sessions_expired_total").await;
            }
            _ => {}
        }
        Ok(())
    }

    fn event_types(&self) -> Vec<EventType> {
        vec![
            EventType::UserLoggedIn,
            EventType::SessionExpired,
        ]
    }

    fn name(&self) -> &str {
        "MetricsCollector"
    }
}
```

## Event Bus

```rust
use tokio::sync::RwLock;
use std::collections::HashMap;

pub struct EventBus {
    consumers: RwLock<HashMap<EventType, Vec<Arc<dyn EventConsumer>>>>,
}

impl EventBus {
    pub fn new() -> Self {
        Self {
            consumers: RwLock::new(HashMap::new()),
        }
    }

    pub async fn subscribe(&self, consumer: Arc<dyn EventConsumer>) {
        let mut consumers = self.consumers.write().await;

        for event_type in consumer.event_types() {
            consumers
                .entry(event_type)
                .or_insert_with(Vec::new)
                .push(Arc::clone(&consumer));
        }

        info!("Consumer '{}' subscribed to {} event types",
              consumer.name(), consumer.event_types().len());
    }

    pub async fn publish(&self, event: Event) -> Result<(), EventError> {
        let consumers = self.consumers.read().await;

        if let Some(event_consumers) = consumers.get(&event.event_type) {
            info!("Publishing event {:?} to {} consumers",
                  event.event_type, event_consumers.len());

            // Process events concurrently
            let futures = event_consumers
                .iter()
                .map(|consumer| {
                    let event = event.clone();
                    let consumer = Arc::clone(consumer);
                    async move {
                        consumer.handle(event).await
                    }
                });

            let results = futures::future::join_all(futures).await;

            // Check for errors
            for (i, result) in results.iter().enumerate() {
                if let Err(e) = result {
                    error!("Consumer {} failed: {}", i, e);
                }
            }
        }

        Ok(())
    }
}
```

## Usage Example

```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Create event bus
    let event_bus = Arc::new(EventBus::new());

    // Create consumers
    let audit_logger = Arc::new(AuditLogger::new(fdb_service.clone()));
    let metrics_collector = Arc::new(MetricsCollector);

    // Subscribe consumers
    event_bus.subscribe(audit_logger).await;
    event_bus.subscribe(metrics_collector).await;

    // Create event producer
    let event_producer = Arc::new(DefaultEventProducer {
        event_bus: event_bus.clone(),
    });

    // Use in handler
    async fn login_handler(
        credentials: LoginRequest,
        event_producer: Arc<dyn EventProducer>,
        fdb: Arc<FDBService>,
    ) -> Result<HttpResponse, ApiError> {
        // Authenticate
        let user = fdb.users().verify_credentials(&credentials).await?;
        let session = fdb.sessions().create(&user.user_id).await?;
        let token = generate_jwt(&session)?;

        // Emit event (async, non-blocking)
        event_producer.emit(Event {
            event_id: Uuid::new_v4(),
            timestamp: Utc::now(),
            event_type: EventType::UserLoggedIn,
            payload: json!({
                "user_id": user.user_id,
                "session_id": session.session_id,
            }),
            metadata: EventMetadata {
                correlation_id: Uuid::new_v4(),
                causation_id: None,
                user_id: Some(user.user_id),
                tenant_id: Some(user.tenant_id),
                source: "login_handler".to_string(),
            },
        }).await?;

        // Return immediately (don't wait for event processing)
        Ok(HttpResponse::Ok().json(LoginResponse { token, session }))
    }

    Ok(())
}
```

## Best Practices

### ✅ DO

- **Emit events asynchronously** - Don't block the main request
- **Make events immutable** - Never modify after creation
- **Use past tense** - "UserLoggedIn", not "LoginUser"
- **Include correlation ID** - For tracing event chains
- **Handle errors gracefully** - Don't crash on consumer failure
- **Provide event replay** - Store events for debugging

### ❌ DON'T

- **Don't use events for RPC** - Events announce facts, don't command
- **Don't couple producers to consumers** - Use event bus abstraction
- **Don't block on event emission** - Fire and forget
- **Don't modify events** - Create new events instead
- **Don't leak implementation details** - Keep payload generic

## Event Sourcing Pattern

```rust
// Store all events for replay
pub struct EventStore {
    fdb: Arc<FDBService>,
}

impl EventStore {
    pub async fn append(&self, event: Event) -> Result<(), EventError> {
        // Store event in FDB
        let key = format!("/{}/events/{}", event.metadata.tenant_id?, event.event_id);
        let value = serde_json::to_vec(&event)?;

        let trx = self.fdb.create_transaction()?;
        trx.set(&key.as_bytes(), &value);
        trx.commit().await?;

        Ok(())
    }

    pub async fn replay(&self, from: DateTime<Utc>) -> Result<Vec<Event>, EventError> {
        // Fetch events since timestamp
        // Useful for rebuilding state or debugging
        todo!()
    }
}
```
