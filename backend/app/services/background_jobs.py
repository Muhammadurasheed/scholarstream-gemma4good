"""
Background Jobs -- Cortex V3 Agentic Infrastructure
Schedules the Scholar Sentinel to patrol opportunity sources continuously.

Architecture:
  Tier 1 -- Sentinel patrol every 30 min (global opportunity pool)
  Tier 2 -- Scholar Sentinel per-user patrol every 12h (personalized)
  Tier 3 -- Gemma health check every 1h (monitors auth + rate limits)
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger()

# Global scheduler instance
scheduler = AsyncIOScheduler()


async def sentinel_patrol_job():
    """
    Tier 1: Deploy the Sentinel drone fleet to patrol all target URLs.
    Runs every 30 minutes -- feeds the global opportunity pool.
    Results stream to all connected WebSocket clients in real-time.
    """
    logger.info("Cortex V3 Sentinel Patrol: Starting mission")
    try:
        from app.services.cortex.navigator import sentinel
        await sentinel.patrol()
        logger.info("Cortex V3 Sentinel Patrol: Mission complete")
    except Exception as e:
        logger.error("Sentinel patrol failed", error=str(e), exc_info=True)


async def scholar_sentinel_per_user_job():
    """
    Tier 2: Run profile-specific Deep Scout for all users every 12h.
    Each user's Academic DNA drives personalized agent missions.
    """
    logger.info("Scholar Sentinel: Per-user profile scan starting")
    try:
        from app.services.scholar_sentinel import scholar_sentinel
        await scholar_sentinel.run_patrol_for_all_users()
        logger.info("Scholar Sentinel: Per-user scan complete")
    except Exception as e:
        logger.error("Scholar Sentinel per-user job failed", error=str(e), exc_info=True)


async def gemma_health_check_job():
    """
    Tier 3: Verify Gemma 4 Vertex AI auth is working every hour.
    Logs a warning with recovery instructions if auth fails.
    """
    logger.info("Gemma Health Check: Testing Vertex AI connection")
    try:
        from app.services.gemma_service import gemma_service
        token = await gemma_service.get_access_token()
        if token:
            logger.info("Gemma Health Check: Vertex AI auth OK (Bearer token valid)")
        else:
            logger.warning("Gemma Health Check: Token is empty -- check ADC/service account")
    except Exception as e:
        logger.error(
            "Gemma Health Check FAILED -- Vertex AI auth error",
            error=str(e),
            fix="Ensure GOOGLE_APPLICATION_CREDENTIALS env var points to valid service account JSON, "
                "or run 'gcloud auth application-default login' locally"
        )


def start_scheduler():
    """
    Initialize and start the background job scheduler.
    Called once on app startup from main.py.
    """
    logger.info("Initializing Cortex V3 background job scheduler")

    # -- Tier 1: Sentinel Patrol -- every 30 minutes --
    scheduler.add_job(
        sentinel_patrol_job,
        'interval',
        minutes=30,
        id='sentinel_patrol',
        replace_existing=True,
        max_instances=1,  # Never overlap -- one patrol at a time
        next_run_time=datetime.now() + timedelta(seconds=45),
    )

    # -- Tier 2: Per-User Scholar Sentinel -- every 12 hours --
    scheduler.add_job(
        scholar_sentinel_per_user_job,
        'interval',
        hours=12,
        id='scholar_sentinel_per_user',
        replace_existing=True,
        max_instances=1,
        next_run_time=datetime.now() + timedelta(minutes=5),
    )

    # -- Tier 3: Gemma Auth Health Check -- every hour --
    scheduler.add_job(
        gemma_health_check_job,
        'interval',
        hours=1,
        id='gemma_health_check',
        replace_existing=True,
        max_instances=1,
        next_run_time=datetime.now() + timedelta(seconds=10),
    )

    scheduler.start()
    logger.info(
        "Cortex V3 scheduler started",
        jobs=["sentinel_patrol (30min)", "scholar_sentinel (12h)", "gemma_health_check (1h)"]
    )


def stop_scheduler():
    """Stop the background job scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Cortex V3 scheduler stopped")
