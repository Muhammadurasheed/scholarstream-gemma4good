"""
ScholarStream FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import structlog
import logging
import asyncio
import os

# === NUCLEAR ENVIRONMENT SANITIZER ===
# Prevents [Errno 2] FileNotFoundError in httpx/ssl by stripping broken Conda/Windows variables.
for var in ["SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"]:
    if var in os.environ:
        del os.environ[var]
# =====================================

from app.config import settings
from app.routes import scholarships, applications, chat, websocket, extension, documents

# Configure structured logging with readable format for development
log_renderer = (
    structlog.processors.JSONRenderer() 
    if settings.environment == "production" 
    else structlog.dev.ConsoleRenderer(colors=True)
)

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S" if settings.environment != "production" else "iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        log_renderer
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="ScholarStream API",
    description="AI-powered scholarship discovery and matching platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
allow_origins = settings.cors_origins_list + [
    "http://localhost:8000",
    "http://localhost:8081",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8081",
    "chrome-extension://"  # Allow Chrome extensions
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
        "http://localhost:3000",
        "https://scholarstream-frontend-1086434452502.us-central1.run.app",
        "https://scholarstream-frontend-opdnpd6bsq-uc.a.run.app",
        "https://scholarstream.app",
        "https://www.scholarstream.app",
        "chrome-extension://iommjbdkgfhpconinoiagkjkiajdohnn",
        "chrome-extension://*", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    logger.info(
        "Request received",
        method=request.method,
        path=request.url.path,
        client=request.client.host if request.client else None
    )
    
    response = await call_next(request)
    
    logger.info(
        "Request completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code
    )
    
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(
        "Unhandled exception",
        error=str(exc),
        path=request.url.path,
        method=request.method,
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "ScholarStream API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(scholarships.router)
app.include_router(applications.router)
app.include_router(chat.router)
app.include_router(websocket.router)
app.include_router(extension.router)
app.include_router(documents.router)
from app.routes import crawler
app.include_router(crawler.router)


# Initialize Event Broker (Global)
from app.infrastructure.memory_broker import MemoryBroker
# In a real app, we'd use a factory based on settings.event_broker_type
broker = MemoryBroker()

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info(
        "Starting ScholarStream API",
        environment=settings.environment,
        debug=settings.debug
    )
    
    # 1. Start Event Broker
    await broker.start()
    
    # 2. Wire up Event Subscribers (The Wiring)
    # Refinery: Listens for Raw HTML -> Enriches
    from app.services.cortex.refinery import refinery_service
    await broker.subscribe(settings.topic_raw_html, refinery_service.handle_raw_html_event)
    
    # WebSocket: Listens for Enriched Data -> Pushes to UI
    from app.routes.websocket import subscribe_to_opportunities
    await subscribe_to_opportunities()
    
    logger.info("Event Mesh sub-systems wired successfully")

    # === CORTEX: START BACKGROUND SCHEDULER ===
    # Handles Heartbeats (6m), Sentinel Patrols (30m), and User Scans (12h)
    # NOTE: Cold-start scrapers removed. The Sentinel's aggregate_patrol() is
    # DNA-driven — it fetches active user profiles first, then targets sources.
    # Running scrapers with no user profile wastes resources and creates stale data.
    from app.services.background_jobs import start_scheduler, stop_scheduler
    start_scheduler()
    logger.info(
        "Cortex V3 scheduler started",
        gemma_engine_enabled=settings.gemma_engine_enabled,
        note="Agents will activate when users have profiles with patrol_enabled=True"
    )


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down ScholarStream API")
    
    # 1. Stop Scheduler
    from app.services.background_jobs import stop_scheduler
    stop_scheduler()
    
    # 2. Stop Event Broker
    await broker.stop()
    
    # 3. Close scraper HTTP client
    from app.services.scraper_service import scraper_service
    await scraper_service.close()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
