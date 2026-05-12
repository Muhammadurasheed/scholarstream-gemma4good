"""
In-Memory Event Broker (Adapter)
Uses asyncio.Queue and direct callbacks for high-speed, local event routing.
"""
import asyncio
import structlog
from typing import Dict, Any, List, Callable, Awaitable
from collections import defaultdict
from app.core.events import EventBroker

logger = structlog.get_logger()

class MemoryBroker:
    """
    In-Memory implementation of EventBroker.
    Uses asyncio for asynchronous event dispatch.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._running = False
        self._queue: asyncio.Queue = asyncio.Queue()
        self._worker_task = None

    async def start(self) -> None:
        """Start the background dispatcher"""
        self._running = True
        self._worker_task = asyncio.create_task(self._dispatcher())
        logger.info("MemoryBroker started")

    async def stop(self) -> None:
        """Stop the dispatcher"""
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        logger.info("MemoryBroker stopped")

    async def publish(self, topic: str, key: str, payload: Dict[str, Any]) -> bool:
        """
        Publish event to the in-memory queue.
        Returns True immediately if queued.
        """
        if not self._running:
            logger.warning("MemoryBroker is not running, dropping event", topic=topic)
            return False

        event = {
            "topic": topic,
            "key": key,
            "payload": payload
        }
        await self._queue.put(event)
        return True

    async def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        """Register a handler for a topic"""
        self._subscribers[topic].append(handler)
        logger.info("Handler subscribed", topic=topic, handler=handler.__name__)

    async def _dispatcher(self):
        """Background loop to process events from queue with Circuit Breaker"""
        while self._running:
            try:
                event = await self._queue.get()
                topic = event["topic"]
                payload = event["payload"]
                
                handlers = self._subscribers.get(topic, [])
                if not handlers:
                    self._queue.task_done()
                    continue

                # Dispatch to all handlers concurrently
                tasks = [self._safe_execute(h, payload) for h in handlers]
                results = await asyncio.gather(*tasks)
                
                # CIRCUIT BREAKER: Check if any handler hit a 429 Quota Error
                if any(r == "429" for r in results):
                    logger.critical("Circuit Breaker OPEN — Vertex AI Quota Exhausted. Pausing global queue for 60s.")
                    await asyncio.sleep(60)
                    logger.info("Circuit Breaker CLOSED — Resuming queue processing.")
                
                self._queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("MemoryBroker dispatcher error", error=str(e))

    async def _safe_execute(self, handler, payload) -> str:
        """Execute handler with error catching and Circuit Breaker signaling"""
        try:
            await handler(payload)
            return "OK"
        except Exception as e:
            error_msg = str(e)
            logger.error("EventHandler failed", handler=handler.__name__, error=error_msg)
            
            # Detect Google Cloud 429 Quota / Resource Exhausted
            if "429" in error_msg or "queue is full" in error_msg.lower() or "resource_exhausted" in error_msg.lower():
                return "429"
            return "ERROR"
