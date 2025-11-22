# Async Patterns Template

Production-ready async/await patterns with timeouts, concurrency control, and error handling.

## Async Timeout Pattern

```python
import asyncio
from typing import TypeVar, Awaitable

T = TypeVar('T')


async def with_timeout(
    coro: Awaitable[T],
    timeout: float,
    timeout_error_message: str = "Operation timed out"
) -> T:
    """Execute coroutine with timeout"""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(timeout_error_message)


# Usage
try:
    result = await with_timeout(
        fetch_data(url),
        timeout=5.0,
        timeout_error_message=f"Failed to fetch from {url} within 5s"
    )
except TimeoutError as e:
    logger.error(f"Timeout: {e}")
    return default_value
```

## Bulkhead Pattern (Concurrency Limiting)

```python
class Bulkhead:
    """Limit concurrent operations to prevent resource exhaustion"""

    def __init__(self, max_concurrent: int):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def execute(self, coro: Awaitable[T]) -> T:
        """Execute with concurrency limit"""
        async with self.semaphore:
            return await coro


# Usage
bulkhead = Bulkhead(max_concurrent=10)


async def process_items(items: list):
    """Process items with concurrency limit"""
    tasks = [bulkhead.execute(process_item(item)) for item in items]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

## Async Queue Pattern

```python
import asyncio
from typing import TypeVar, Callable, Optional

T = TypeVar('T')


class AsyncWorkerPool:
    """Worker pool for processing items from a queue"""

    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self.queue: asyncio.Queue = asyncio.Queue()
        self.workers: list[asyncio.Task] = []

    async def worker(self, process_func: Callable[[T], Awaitable[None]]):
        """Worker that processes items from queue"""
        while True:
            item = await self.queue.get()
            if item is None:  # Sentinel to stop worker
                break
            try:
                await process_func(item)
            except Exception as e:
                logger.error(f"Worker failed to process item: {e}")
            finally:
                self.queue.task_done()

    async def start(self, process_func: Callable[[T], Awaitable[None]]):
        """Start worker pool"""
        self.workers = [
            asyncio.create_task(self.worker(process_func))
            for _ in range(self.num_workers)
        ]

    async def submit(self, item: T):
        """Submit item for processing"""
        await self.queue.put(item)

    async def wait_completion(self):
        """Wait for all queued items to be processed"""
        await self.queue.join()

    async def stop(self):
        """Stop all workers"""
        # Send sentinel to each worker
        for _ in range(self.num_workers):
            await self.queue.put(None)
        # Wait for workers to finish
        await asyncio.gather(*self.workers)


# Usage
async def process_item(item: dict):
    await asyncio.sleep(0.1)  # Simulate work
    print(f"Processed: {item}")


pool = AsyncWorkerPool(num_workers=5)
await pool.start(process_item)

for i in range(100):
    await pool.submit({"id": i})

await pool.wait_completion()
await pool.stop()
```

## Async Batching Pattern

```python
class AsyncBatcher:
    """Batch async operations for efficiency"""

    def __init__(self, batch_size: int, flush_interval: float):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.batch: list = []
        self.lock = asyncio.Lock()
        self.flush_task: Optional[asyncio.Task] = None

    async def add(self, item: T) -> None:
        """Add item to batch"""
        async with self.lock:
            self.batch.append(item)
            if len(self.batch) >= self.batch_size:
                await self._flush()

    async def _flush(self):
        """Flush current batch"""
        if not self.batch:
            return

        batch_to_process = self.batch
        self.batch = []

        # Process batch (implement this based on use case)
        await process_batch(batch_to_process)

    async def start_auto_flush(self):
        """Start automatic flushing on interval"""
        while True:
            await asyncio.sleep(self.flush_interval)
            async with self.lock:
                await self._flush()


# Usage
batcher = AsyncBatcher(batch_size=100, flush_interval=1.0)

# Start auto-flush in background
asyncio.create_task(batcher.start_auto_flush())

# Add items
for item in items:
    await batcher.add(item)
```

## Async Retry with Backoff

```python
import random


async def async_retry(
    func: Callable[[], Awaitable[T]],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True
) -> T:
    """Retry async function with exponential backoff"""

    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            # Calculate delay with exponential backoff
            delay = min(base_delay * (exponential_base ** attempt), max_delay)

            # Add jitter to prevent thundering herd
            if jitter:
                delay = delay * (0.5 + random.random())

            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s")
            await asyncio.sleep(delay)


# Usage with decorator
def retry(max_retries: int = 3, **kwargs):
    """Decorator for async retry"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **func_kwargs):
            return await async_retry(
                lambda: func(*args, **func_kwargs),
                max_retries=max_retries,
                **kwargs
            )
        return wrapper
    return decorator


@retry(max_retries=3, base_delay=1.0)
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
```

## Async Context Manager Pattern

```python
from contextlib import asynccontextmanager


class AsyncResourceManager:
    """Manage async resource lifecycle"""

    async def acquire(self):
        """Acquire resource"""
        print("Acquiring resource...")
        await asyncio.sleep(0.1)
        return "resource"

    async def release(self, resource):
        """Release resource"""
        print(f"Releasing {resource}...")
        await asyncio.sleep(0.1)


@asynccontextmanager
async def get_resource():
    """Context manager for resource"""
    manager = AsyncResourceManager()
    resource = await manager.acquire()
    try:
        yield resource
    finally:
        await manager.release(resource)


# Usage
async def use_resource():
    async with get_resource() as resource:
        print(f"Using {resource}")
        await asyncio.sleep(0.1)
```

## Async Event Pattern

```python
class AsyncEvent:
    """Async event emitter"""

    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}

    def on(self, event: str, handler: Callable):
        """Register event handler"""
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)

    async def emit(self, event: str, *args, **kwargs):
        """Emit event to all handlers"""
        if event in self.handlers:
            await asyncio.gather(
                *(handler(*args, **kwargs) for handler in self.handlers[event]),
                return_exceptions=True
            )


# Usage
events = AsyncEvent()


@events.on("user_created")
async def send_welcome_email(user):
    await send_email(user.email, "Welcome!")


@events.on("user_created")
async def create_profile(user):
    await create_user_profile(user.id)


# Emit event (all handlers run concurrently)
await events.emit("user_created", user=new_user)
```

## Best Practices

### ✅ DO

```python
# Always use timeout for external calls
result = await asyncio.wait_for(external_call(), timeout=5.0)

# Use semaphores to limit concurrency
semaphore = asyncio.Semaphore(10)
async with semaphore:
    await expensive_operation()

# Gather with return_exceptions to handle partial failures
results = await asyncio.gather(*tasks, return_exceptions=True)

# Use create_task for fire-and-forget
asyncio.create_task(background_work())

# Properly cancel tasks
task = asyncio.create_task(long_running())
try:
    await asyncio.wait_for(task, timeout=10)
except asyncio.TimeoutError:
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
```

### ❌ DON'T

```python
# Don't block the event loop
time.sleep(5)  # ❌ Use await asyncio.sleep(5)

# Don't forget to await
result = async_function()  # ❌ Creates coroutine, doesn't execute

# Don't mix sync and async without care
def sync_wrapper():
    asyncio.run(async_function())  # ❌ In async context

# Don't forget to handle exceptions in gather
await asyncio.gather(*tasks)  # ❌ One failure stops all

# Don't forget timeouts
await external_call()  # ❌ Can hang forever
```

## Common Pitfalls

### Pitfall 1: Blocking the Event Loop

```python
# ❌ BAD
async def process():
    time.sleep(1)  # Blocks event loop!

# ✅ GOOD
async def process():
    await asyncio.sleep(1)  # Async sleep
```

### Pitfall 2: Not Awaiting Coroutines

```python
# ❌ BAD
result = async_function()  # Creates coroutine, doesn't run it

# ✅ GOOD
result = await async_function()  # Actually runs it
```

### Pitfall 3: Creating Tasks Without Tracking

```python
# ❌ BAD
asyncio.create_task(background_work())  # Fire and forget, no error handling

# ✅ GOOD
task = asyncio.create_task(background_work())
try:
    await task
except Exception as e:
    logger.error(f"Background task failed: {e}")
```

### Pitfall 4: Unbounded Concurrency

```python
# ❌ BAD
tasks = [process_item(item) for item in huge_list]
await asyncio.gather(*tasks)  # May exhaust resources

# ✅ GOOD
semaphore = asyncio.Semaphore(10)

async def bounded_process(item):
    async with semaphore:
        return await process_item(item)

tasks = [bounded_process(item) for item in huge_list]
await asyncio.gather(*tasks)
```
