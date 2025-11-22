#!/usr/bin/env python3
"""
Circuit Breaker Implementation

Prevents cascading failures by breaking the circuit when error threshold exceeded.
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Any, Optional, TypeVar
import asyncio
import time

T = TypeVar('T')


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"          # Normal operation
    OPEN = "open"              # Circuit broken, fail fast
    HALF_OPEN = "half_open"    # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration"""
    failure_threshold: int = 5  # Failures before opening circuit
    timeout: timedelta = timedelta(seconds=60)  # Time before trying half-open
    success_threshold: int = 2  # Successes in half-open before closing
    expected_exception: type = Exception  # Exception type to count as failure


@dataclass
class CircuitBreakerStats:
    """Circuit breaker statistics"""
    state: CircuitState
    failure_count: int
    success_count: int
    last_failure_time: Optional[datetime]
    total_calls: int
    total_failures: int
    total_successes: int


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass


class CircuitBreaker:
    """
    Circuit breaker for fault tolerance.

    Implements the circuit breaker pattern to prevent cascading failures.
    """

    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.total_calls = 0
        self.total_failures = 0
        self.total_successes = 0

    async def call_async(self, func: Callable[[], T]) -> T:
        """Execute async function with circuit breaker protection"""
        self.total_calls += 1

        # If circuit is open, check if we should try half-open
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                print(f"[{self.name}] Attempting reset: OPEN -> HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker '{self.name}' is open. "
                    f"Last failure: {self.last_failure_time}"
                )

        try:
            # Execute the function
            result = await func()

            # On success
            self._on_success()
            return result

        except self.config.expected_exception as e:
            # On failure
            self._on_failure()
            raise

    def call(self, func: Callable[[], T]) -> T:
        """Execute sync function with circuit breaker protection"""
        self.total_calls += 1

        # If circuit is open, check if we should try half-open
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                print(f"[{self.name}] Attempting reset: OPEN -> HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker '{self.name}' is open. "
                    f"Last failure: {self.last_failure_time}"
                )

        try:
            # Execute the function
            result = func()

            # On success
            self._on_success()
            return result

        except self.config.expected_exception as e:
            # On failure
            self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to try half-open"""
        if self.last_failure_time is None:
            return True
        return datetime.now() - self.last_failure_time > self.config.timeout

    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.total_successes += 1

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            print(f"[{self.name}] Success in HALF_OPEN: {self.success_count}/{self.config.success_threshold}")

            if self.success_count >= self.config.success_threshold:
                print(f"[{self.name}] Circuit closed: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.success_count = 0

    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.total_failures += 1
        self.last_failure_time = datetime.now()

        print(f"[{self.name}] Failure #{self.failure_count} in {self.state.value} state")

        if self.state == CircuitState.HALF_OPEN:
            # Any failure in half-open immediately opens circuit
            print(f"[{self.name}] Failure in HALF_OPEN, reopening circuit")
            self.state = CircuitState.OPEN
            self.failure_count = self.config.failure_threshold

        elif self.failure_count >= self.config.failure_threshold:
            print(f"[{self.name}] Threshold reached, opening circuit: CLOSED -> OPEN")
            self.state = CircuitState.OPEN

    def reset(self):
        """Manually reset circuit breaker"""
        print(f"[{self.name}] Manual reset")
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0

    def get_stats(self) -> CircuitBreakerStats:
        """Get current statistics"""
        return CircuitBreakerStats(
            state=self.state,
            failure_count=self.failure_count,
            success_count=self.success_count,
            last_failure_time=self.last_failure_time,
            total_calls=self.total_calls,
            total_failures=self.total_failures,
            total_successes=self.total_successes
        )


async def main():
    """Example usage"""
    print("=== Circuit Breaker Example ===\n")

    # Create circuit breaker
    cb = CircuitBreaker(
        name="external_api",
        config=CircuitBreakerConfig(
            failure_threshold=3,
            timeout=timedelta(seconds=5),
            success_threshold=2
        )
    )

    # Simulated API call that fails
    call_count = 0

    async def unreliable_api_call():
        nonlocal call_count
        call_count += 1

        # Fail for first 5 calls, then succeed
        if call_count <= 5:
            print(f"  API call #{call_count}: FAILED")
            raise Exception("API temporarily unavailable")
        else:
            print(f"  API call #{call_count}: SUCCESS")
            return {"data": "success"}

    # Test circuit breaker
    print("1. Normal operation (CLOSED)")
    print("-" * 60)
    for i in range(5):
        try:
            result = await cb.call_async(unreliable_api_call)
            print(f"✓ Call {i+1} succeeded")
        except CircuitBreakerOpenError as e:
            print(f"✗ Call {i+1} failed: Circuit is open")
        except Exception as e:
            print(f"✗ Call {i+1} failed: {e}")

        print(f"  State: {cb.state.value}, Failures: {cb.failure_count}\n")
        await asyncio.sleep(0.1)

    print("\n2. Circuit is now OPEN, waiting for timeout...")
    print("-" * 60)

    # Try to call while circuit is open
    for i in range(2):
        try:
            result = await cb.call_async(unreliable_api_call)
            print(f"✓ Call succeeded")
        except CircuitBreakerOpenError as e:
            print(f"✗ Circuit breaker blocked call: {e}")

        await asyncio.sleep(1)

    print("\n3. Waiting for timeout to attempt HALF_OPEN...")
    print("-" * 60)
    await asyncio.sleep(4)  # Wait for timeout

    # Try again - circuit should be HALF_OPEN
    for i in range(3):
        try:
            result = await cb.call_async(unreliable_api_call)
            print(f"✓ Call {i+1} succeeded in HALF_OPEN")
        except Exception as e:
            print(f"✗ Call {i+1} failed: {e}")

        print(f"  State: {cb.state.value}, Successes: {cb.success_count}\n")
        await asyncio.sleep(0.1)

    # Print final stats
    print("\n4. Final Statistics")
    print("-" * 60)
    stats = cb.get_stats()
    print(f"State: {stats.state.value}")
    print(f"Total Calls: {stats.total_calls}")
    print(f"Total Successes: {stats.total_successes}")
    print(f"Total Failures: {stats.total_failures}")
    print(f"Success Rate: {stats.total_successes / stats.total_calls * 100:.1f}%")


if __name__ == "__main__":
    asyncio.run(main())
