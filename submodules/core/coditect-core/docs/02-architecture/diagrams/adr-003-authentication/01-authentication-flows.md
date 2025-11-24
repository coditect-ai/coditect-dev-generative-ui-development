# ADR-003 Diagram 1: Authentication Flows

**Related ADR:** [ADR-003: User Registration and Authentication](../../adrs/ADR-003-user-registration-authentication.md)

---

## User Registration Flow

### Standard Email/Password Registration

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant API as Auth API
    participant DB as User DB
    participant Email as SendGrid

    User->>Browser: Visit /signup
    Browser->>Browser: Fill form (email, password, name)

    Browser->>API: POST /api/v1/auth/register
    Note over Browser,API: {email, password, name}

    API->>API: Validate input<br/>(password strength, email format)

    alt Validation passed
        API->>API: Hash password (bcrypt, 12 rounds)
        API->>DB: INSERT INTO users
        DB-->>API: user_id created

        API->>API: Generate verification token
        API->>Email: Send verification email
        Email-->>User: Email with verification link

        API-->>Browser: 201 Created
        Note over API,Browser: {user_id, email_verified: false}

        Browser-->>User: "Check your email to verify"

        User->>Email: Click verification link
        Email->>API: GET /verify-email?token=abc123

        API->>DB: UPDATE users SET email_verified=TRUE
        API->>API: Generate license key (FREE tier)
        API->>DB: INSERT INTO licenses

        API-->>Browser: Redirect to /login

        Browser-->>User: "Email verified! Please log in"

    else Validation failed
        API-->>Browser: 400 Bad Request
        Note over API,Browser: {error: "Password too weak"}
        Browser-->>User: Show error
    end
```

---

### Social OAuth Registration (Google)

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant API as Auth API
    participant Google as Google OAuth
    participant DB as User DB

    User->>Browser: Click "Sign up with Google"

    Browser->>Google: Redirect to Google OAuth
    Note over Browser,Google: /oauth/authorize?<br/>client_id=...&<br/>scope=email,profile

    User->>Google: Authorize CODITECT
    Google-->>Browser: Redirect with auth code
    Note over Google,Browser: /auth/callback?code=abc123

    Browser->>API: POST /api/v1/auth/oauth/google
    Note over Browser,API: {code: "abc123"}

    API->>Google: Exchange code for tokens
    Note over API,Google: POST /oauth/token

    Google-->>API: {access_token, id_token}
    API->>API: Decode id_token (JWT)
    Note over API: Extract: email, name, picture

    API->>DB: SELECT * FROM users WHERE email=?

    alt User exists
        API->>DB: UPDATE last_login_at
        API->>API: Generate JWT access token
        API-->>Browser: {access_token, user}
    else User does not exist
        API->>DB: INSERT INTO users<br/>(email_verified=TRUE)
        Note over API,DB: OAuth emails are pre-verified

        API->>API: Generate license key (FREE tier)
        API->>DB: INSERT INTO licenses
        API->>API: Generate JWT access token
        API-->>Browser: {access_token, user, new_user: true}
    end

    Browser-->>User: Logged in!
```

---

## Authentication Flows

### Email/Password Login

```mermaid
sequenceDiagram
    actor User
    participant CLI as Local CLI
    participant Browser
    participant API as Auth API
    participant DB as User DB
    participant Redis

    User->>CLI: coditect login

    CLI->>CLI: Open browser to /cli-login
    CLI->>CLI: Start local server (localhost:8787)

    Browser->>Browser: Show login form

    User->>Browser: Enter email + password
    Browser->>API: POST /api/v1/auth/login
    Note over Browser,API: {email, password}

    API->>DB: SELECT * FROM users WHERE email=?

    alt User found
        API->>API: Verify password (bcrypt)

        alt Password correct
            API->>API: Check email_verified

            alt Email verified
                API->>API: Generate JWT (RS256)<br/>- Access token (1hr)<br/>- Refresh token (30 days)

                API->>Redis: SETEX session:{session_id}
                API->>DB: INSERT INTO user_sessions

                API-->>Browser: 200 OK
                Note over API,Browser: {access_token, refresh_token, user}

                Browser->>CLI: POST localhost:8787/callback
                Note over Browser,CLI: {access_token, refresh_token}

                CLI->>CLI: Save to ~/.coditect/auth.json
                CLI-->>User: ✅ Logged in as {name}

            else Email not verified
                API-->>Browser: 403 Forbidden
                Note over API,Browser: {error: "Email not verified"}
                Browser-->>User: Please verify your email
            end

        else Password incorrect
            API->>API: Increment failed_attempts
            API-->>Browser: 401 Unauthorized
            Browser-->>User: Invalid credentials
        end

    else User not found
        API-->>Browser: 401 Unauthorized
        Browser-->>User: Invalid credentials
    end
```

---

### Token Refresh Flow

```mermaid
sequenceDiagram
    participant CLI as Local CLI
    participant API as Auth API
    participant Redis
    participant DB as User DB

    Note over CLI: Access token expired

    CLI->>CLI: Load refresh token from ~/.coditect/auth.json

    CLI->>API: POST /api/v1/auth/refresh
    Note over CLI,API: {refresh_token: "rt_..."}

    API->>API: Decode refresh token (JWT)
    Note over API: Extract: session_id, user_id

    API->>Redis: GET session:{session_id}

    alt Session valid
        API->>DB: SELECT * FROM user_sessions<br/>WHERE session_id=? AND revoked=FALSE

        alt Session not revoked
            API->>API: Generate new access token (1hr)
            API->>API: Optionally rotate refresh token

            alt Rotate refresh token
                API->>Redis: DEL session:{old_session_id}
                API->>API: Generate new refresh token
                API->>Redis: SETEX session:{new_session_id}
                API->>DB: UPDATE user_sessions<br/>SET refresh_token_hash=?
            end

            API->>DB: UPDATE user_sessions<br/>SET last_used_at=NOW()

            API-->>CLI: 200 OK
            Note over API,CLI: {access_token,<br/>refresh_token (new)}

            CLI->>CLI: Update ~/.coditect/auth.json

        else Session revoked
            API-->>CLI: 401 Unauthorized
            Note over API,CLI: {error: "Session revoked"}
            CLI-->>User: ❌ Please login again
        end

    else Session not found in Redis
        API->>DB: SELECT * FROM user_sessions

        alt Session valid in DB
            API->>Redis: SETEX session:{session_id}
            Note over API,Redis: Rebuild cache from DB
            API->>API: Generate new access token
            API-->>CLI: 200 OK
        else Session invalid
            API-->>CLI: 401 Unauthorized
        end
    end
```

---

## Enterprise SSO Flows

### SAML 2.0 Authentication

```mermaid
sequenceDiagram
    actor User as Employee
    participant Browser
    participant CODITECT as CODITECT SP
    participant Okta as Okta IdP
    participant DB as User DB

    User->>Browser: Visit coditect.ai/login
    Browser->>Browser: Enter email: alice@acme.com

    Browser->>CODITECT: POST /api/v1/auth/login
    Note over Browser,CODITECT: {email: "alice@acme.com"}

    CODITECT->>CODITECT: Detect @acme.com → SSO required
    CODITECT->>DB: SELECT sso_config WHERE domain='acme.com'
    DB-->>CODITECT: {provider: 'okta', metadata_url: '...'}

    CODITECT->>CODITECT: Generate SAML AuthnRequest
    CODITECT-->>Browser: 302 Redirect to Okta
    Note over CODITECT,Browser: https://acme.okta.com/saml/login?<br/>SAMLRequest=base64(...)

    Browser->>Okta: GET /saml/login

    User->>Okta: Authenticate (username + password + MFA)
    Okta->>Okta: Validate credentials

    Okta->>Okta: Generate SAML Response
    Note over Okta: Includes:<br/>- email<br/>- name<br/>- groups

    Okta-->>Browser: 302 Redirect to CODITECT
    Note over Okta,Browser: POST /api/v1/auth/saml/callback<br/>SAMLResponse=base64(...)

    Browser->>CODITECT: POST /saml/callback

    CODITECT->>CODITECT: Validate SAML Response<br/>- Signature (Okta public key)<br/>- Expiration<br/>- Recipient URL

    alt SAML valid
        CODITECT->>CODITECT: Extract attributes<br/>(email, name, groups)

        CODITECT->>DB: SELECT * FROM users WHERE email=?

        alt User exists
            CODITECT->>DB: UPDATE last_login_at
        else JIT Provisioning enabled
            CODITECT->>DB: INSERT INTO users<br/>(email, name, org_id)
            Note over CODITECT,DB: Auto-create user from SAML
            CODITECT->>CODITECT: Map groups to roles
            CODITECT->>DB: INSERT INTO user_roles
        end

        CODITECT->>CODITECT: Generate JWT tokens
        CODITECT-->>Browser: Set-Cookie: session_token

        Browser-->>User: ✅ Logged in
    else SAML invalid
        CODITECT-->>Browser: 401 Unauthorized
        Browser-->>User: SSO authentication failed
    end
```

---

### OAuth 2.0 / OIDC (Azure AD)

```mermaid
sequenceDiagram
    actor User as Employee
    participant Browser
    participant CODITECT
    participant Azure as Azure AD
    participant DB as User DB

    User->>Browser: coditect login --sso

    Browser->>CODITECT: Initiate SSO login

    CODITECT->>CODITECT: Detect organization (via email domain)
    CODITECT->>DB: SELECT sso_config

    CODITECT-->>Browser: 302 Redirect to Azure AD
    Note over CODITECT,Browser: /oauth/authorize?<br/>client_id=...&<br/>response_type=code&<br/>scope=openid,email,profile

    Browser->>Azure: GET /oauth/authorize
    User->>Azure: Authenticate (corporate credentials)
    Azure->>Azure: Validate user

    Azure-->>Browser: 302 Redirect with code
    Note over Azure,Browser: /auth/callback?code=abc123

    Browser->>CODITECT: GET /auth/callback?code=abc123

    CODITECT->>Azure: POST /oauth/token
    Note over CODITECT,Azure: {code, client_id, client_secret}

    Azure-->>CODITECT: {access_token, id_token}

    CODITECT->>CODITECT: Verify id_token signature (JWT)
    CODITECT->>CODITECT: Extract claims<br/>(email, name, oid, groups)

    CODITECT->>DB: SELECT * FROM users WHERE email=?

    alt User exists
        CODITECT->>DB: UPDATE last_login_at
    else JIT provision
        CODITECT->>DB: INSERT INTO users
        CODITECT->>DB: Map Azure groups to roles
    end

    CODITECT->>CODITECT: Generate CODITECT JWT
    CODITECT-->>Browser: {access_token, user}

    Browser-->>User: ✅ Logged in via Azure AD
```

---

## Multi-Factor Authentication

### MFA Enrollment

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant API as Auth API
    participant DB as User DB

    User->>Browser: Account Settings → Enable MFA

    Browser->>API: POST /api/v1/auth/mfa/enroll
    Note over Browser,API: {Authorization: Bearer ...}

    API->>API: Generate TOTP secret<br/>(32-character base32)

    API->>API: Generate QR code
    Note over API: otpauth://totp/CODITECT:user@example.com?<br/>secret=JBSWY3DPEHPK3PXP&issuer=CODITECT

    API->>API: Generate 10 backup codes

    API-->>Browser: 200 OK
    Note over API,Browser: {<br/>  secret,<br/>  qr_code_url,<br/>  backup_codes<br/>}

    Browser-->>User: Display QR code + backup codes

    User->>User: Scan QR with Google Authenticator

    User->>Browser: Enter verification code
    Browser->>API: POST /api/v1/auth/mfa/verify
    Note over Browser,API: {code: "123456"}

    API->>API: Validate TOTP code
    Note over API: pyotp.TOTP(secret).verify(code)

    alt Code valid
        API->>DB: UPDATE users<br/>SET mfa_enabled=TRUE,<br/>mfa_secret=encrypt(secret)

        API->>DB: INSERT backup codes (hashed)

        API-->>Browser: 200 OK
        Browser-->>User: ✅ MFA enabled!

    else Code invalid
        API-->>Browser: 400 Bad Request
        Browser-->>User: Invalid code, try again
    end
```

---

### MFA Login Challenge

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant API as Auth API
    participant DB as User DB

    User->>Browser: Enter email + password
    Browser->>API: POST /api/v1/auth/login

    API->>DB: Verify credentials

    alt Credentials valid
        API->>DB: Check if MFA enabled

        alt MFA enabled
            API->>API: Generate temporary MFA token<br/>(5 minute expiry)

            API-->>Browser: 200 OK (MFA required)
            Note over API,Browser: {<br/>  mfa_required: true,<br/>  mfa_token: "temp_..."<br/>}

            Browser-->>User: Show MFA code input

            User->>User: Open authenticator app
            User->>User: Read 6-digit code

            User->>Browser: Enter code
            Browser->>API: POST /api/v1/auth/mfa/challenge
            Note over Browser,API: {<br/>  mfa_token: "temp_...",<br/>  code: "123456"<br/>}

            API->>API: Verify MFA token (not expired)
            API->>DB: Load encrypted MFA secret
            API->>API: Decrypt secret
            API->>API: Validate TOTP code

            alt Code valid
                API->>API: Generate session tokens
                API-->>Browser: {access_token, refresh_token}
                Browser-->>User: ✅ Logged in

            else Code invalid
                API->>API: Increment attempt count
                alt Attempts < 5
                    API-->>Browser: 401 Unauthorized
                    Browser-->>User: Invalid code (X attempts remaining)
                else Attempts >= 5
                    API->>DB: Lock account for 15 minutes
                    API-->>Browser: 429 Too Many Requests
                    Browser-->>User: Too many attempts. Try again in 15 min.
                end
            end

        else MFA not enabled
            API->>API: Generate session tokens
            API-->>Browser: {access_token, refresh_token}
            Browser-->>User: ✅ Logged in
        end
    end
```

---

## Session Management

### Active Sessions Overview

```mermaid
graph TB
    subgraph "User Account"
        User[user@example.com]
    end

    subgraph "Active Sessions"
        S1[Session 1<br/>MacBook Pro<br/>San Francisco<br/>Chrome]
        S2[Session 2<br/>iPhone 15<br/>San Francisco<br/>Safari]
        S3[Session 3<br/>Windows PC<br/>New York<br/>Edge]
    end

    User --> S1
    User --> S2
    User --> S3

    S1 -->|Refresh token| RT1[rt_abc123...<br/>Expires: 30 days]
    S2 -->|Refresh token| RT2[rt_def456...<br/>Expires: 30 days]
    S3 -->|Refresh token| RT3[rt_ghi789...<br/>Expires: 30 days]

    style S1 fill:#90EE90
    style S2 fill:#90EE90
    style S3 fill:#90EE90
```

### Session Revocation

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant API as Auth API
    participant DB as User DB
    participant Redis

    User->>Browser: Account Settings → Active Sessions

    Browser->>API: GET /api/v1/auth/sessions
    API->>DB: SELECT * FROM user_sessions<br/>WHERE user_id=? AND revoked=FALSE

    DB-->>API: List of sessions
    API-->>Browser: Display sessions

    Browser-->>User: Show: MacBook Pro (current)<br/>iPhone 15<br/>Windows PC

    User->>Browser: Click "Revoke" on Windows PC session

    Browser->>API: DELETE /api/v1/auth/sessions/{session_id}

    API->>DB: UPDATE user_sessions<br/>SET revoked=TRUE,<br/>revoked_at=NOW(),<br/>revoked_reason='user_action'

    API->>Redis: DEL session:{session_id}

    API-->>Browser: 200 OK
    Browser-->>User: ✅ Session revoked

    Note over User,Redis: Windows PC's refresh token<br/>is now invalid
```

---

**Related Documents:**
- [ADR-003: User Registration and Authentication](../../adrs/ADR-003-user-registration-authentication.md)
- [Diagram 2: Security Architecture](./02-security-architecture.md)
- [Diagram 3: JWT Token Structure](./03-jwt-tokens.md)
