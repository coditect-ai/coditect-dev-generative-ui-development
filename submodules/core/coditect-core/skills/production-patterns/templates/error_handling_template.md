# Error Handling Template

Production-ready error handling patterns with structured errors, retries, and recovery.

## Structured Error Classes

```python
from typing import Optional, Dict, Any
from datetime import datetime
import traceback


class ApplicationError(Exception):
    """Base application error with structured context"""

    def __init__(
        self,
        message: str,
        error_code: str,
        details: Optional[Dict[str, Any]] = None,
        retryable: bool = False,
        original_exception: Optional[Exception] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.retryable = retryable
        self.original_exception = original_exception
        self.timestamp = datetime.now()
        self.stack_trace = traceback.format_exc() if original_exception else None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize error for logging/reporting"""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "retryable": self.retryable,
            "timestamp": self.timestamp.isoformat(),
            "stack_trace": self.stack_trace,
        }


# Domain-specific errors
class DatabaseError(ApplicationError):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="DB_ERROR", retryable=True, **kwargs)


class ValidationError(ApplicationError):
    def __init__(self, message: str, field: str, **kwargs):
        super().__init__(
            message,
            error_code="VALIDATION_ERROR",
            details={"field": field},
            retryable=False,
            **kwargs
        )


class ExternalServiceError(ApplicationError):
    def __init__(self, service_name: str, message: str, **kwargs):
        super().__init__(
            message,
            error_code="EXTERNAL_SERVICE_ERROR",
            details={"service": service_name},
            retryable=True,
            **kwargs
        )


class AuthenticationError(ApplicationError):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="AUTH_ERROR", retryable=False, **kwargs)


class RateLimitError(ApplicationError):
    def __init__(self, message: str, retry_after: int, **kwargs):
        super().__init__(
            message,
            error_code="RATE_LIMIT_ERROR",
            details={"retry_after": retry_after},
            retryable=True,
            **kwargs
        )
```

## Retry with Exponential Backoff

```python
import asyncio
from typing import TypeVar, Callable
from functools import wraps

T = TypeVar('T')


async def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: tuple = (Exception,)
) -> T:
    """Retry function with exponential backoff"""

    for attempt in range(max_retries):
        try:
            return await func()
        except retryable_exceptions as e:
            if attempt == max_retries - 1:
                raise

            delay = min(base_delay * (exponential_base ** attempt), max_delay)

            if jitter:
                import random
                delay = delay * (0.5 + random.random())

            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
            await asyncio.sleep(delay)


def with_retry(max_retries: int = 3, **kwargs):
    """Decorator for automatic retry"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **func_kwargs):
            return await retry_with_backoff(
                lambda: func(*args, **func_kwargs),
                max_retries=max_retries,
                **kwargs
            )
        return wrapper
    return decorator
```

## Error Recovery Patterns

### Pattern 1: Fallback to Cache

```python
async def get_user_data(user_id: str) -> dict:
    """Fetch user data with fallback to cache"""
    try:
        # Try primary source
        return await fetch_from_api(user_id)
    except ExternalServiceError as e:
        logger.warning(f"API failed, using cache: {e}")
        # Fallback to cache
        cached_data = await get_from_cache(user_id)
        if cached_data:
            return cached_data
        # No cache, re-raise
        raise
```

### Pattern 2: Graceful Degradation

```python
async def get_user_profile(user_id: str) -> dict:
    """Get user profile with graceful degradation"""
    profile = {"user_id": user_id}

    # Try to get user details (critical)
    try:
        user = await fetch_user(user_id)
        profile.update(user)
    except Exception as e:
        logger.error(f"Failed to fetch user: {e}")
        raise  # Critical data, must fail

    # Try to get preferences (non-critical)
    try:
        preferences = await fetch_preferences(user_id)
        profile["preferences"] = preferences
    except Exception as e:
        logger.warning(f"Failed to fetch preferences: {e}")
        profile["preferences"] = {}  # Use defaults

    # Try to get activity (non-critical)
    try:
        activity = await fetch_activity(user_id)
        profile["activity"] = activity
    except Exception as e:
        logger.warning(f"Failed to fetch activity: {e}")
        profile["activity"] = {}  # Use empty

    return profile
```

### Pattern 3: Circuit Breaker

```python
from production_patterns.core.circuit_breaker import CircuitBreaker

# Create circuit breaker for external service
external_api_cb = CircuitBreaker(
    name="external_api",
    config=CircuitBreakerConfig(
        failure_threshold=5,
        timeout=timedelta(seconds=60),
        success_threshold=2
    )
)


async def call_external_api(endpoint: str) -> dict:
    """Call external API with circuit breaker protection"""
    try:
        return await external_api_cb.call_async(lambda: fetch_data(endpoint))
    except CircuitBreakerOpenError:
        logger.error("Circuit breaker open for external API")
        return get_cached_data(endpoint)
```

## Error Handling Best Practices

### ✅ DO

```python
# Use specific exceptions
raise ValidationError("Invalid email format", field="email")

# Include context in error messages
raise DatabaseError(
    f"Failed to insert user {user_id}",
    details={"user_id": user_id, "table": "users"}
)

# Log errors with context
logger.error(
    "Payment processing failed",
    error=exc,
    user_id=user_id,
    amount=amount,
    payment_method=payment_method
)

# Retry only retryable errors
if error.retryable:
    await retry_operation()
else:
    raise
```

### ❌ DON'T

```python
# Don't use generic exceptions
raise Exception("Something went wrong")  # ❌

# Don't swallow errors silently
try:
    risky_operation()
except:
    pass  # ❌

# Don't retry non-retryable errors
try:
    validate_input(data)
except ValidationError:
    await retry()  # ❌ Validation errors aren't retryable

# Don't expose internal details to users
return {"error": str(exc)}  # ❌ May leak sensitive info
```

## Error Response Format (REST API)

```python
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standardized error response"""
    error_code: str
    message: str
    details: Dict[str, Any] = {}
    timestamp: str
    request_id: str
    retryable: bool = False


def error_to_response(error: ApplicationError, request_id: str) -> ErrorResponse:
    """Convert application error to API response"""
    return ErrorResponse(
        error_code=error.error_code,
        message=error.message,
        details=error.details,
        timestamp=error.timestamp.isoformat(),
        request_id=request_id,
        retryable=error.retryable
    )
```
