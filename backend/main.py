# backend/main.py
"""
PitchIQ — FastAPI Application Entry Point
──────────────────────────────────────────
Wires together:
  - CORS middleware (frontend ↔ backend)
  - Rate limiting (via slowapi)
  - Structured logging (structlog)
  - Database initialization
  - API routers
  - Health check endpoint

Run locally:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager
import structlog
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from config import get_settings
from database import init_db
from routers.generate import router as generate_router
from routers.status import router as status_router

# ── Logging Setup ─────────────────────────────────────────────────────────────
# structlog gives us JSON-formatted logs with no secrets leaking
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),  # All logs are JSON
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)
logging.basicConfig(level=logging.INFO)
logger = structlog.get_logger(__name__)

settings = get_settings()


# ── Lifespan: startup + shutdown ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Code before 'yield' runs at application startup.
    Code after 'yield' runs at application shutdown.
    This is the modern FastAPI pattern (replaces @app.on_event).
    """
    # Startup
    logger.info("pitchiq.starting", environment=settings.environment)
    await init_db()                  # Create SQLite tables
    logger.info("pitchiq.ready", port=settings.backend_port)

    yield  # App is running here

    # Shutdown
    logger.info("pitchiq.shutting_down")


# ── Rate Limiter ──────────────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)


# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="PitchIQ API",
    description=(
        "AI-powered investor memo generator. "
        "A multi-agent system built with Google ADK and Gemini 2.5 Flash."
    ),
    version="1.0.0",
    docs_url="/docs",          # Swagger UI at /docs (great for judges)
    redoc_url="/redoc",        # ReDoc at /redoc
    lifespan=lifespan,
)

# Attach rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ── CORS Middleware ────────────────────────────────────────────────────────────
# Allows the Next.js frontend (port 3000) to call the backend (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(generate_router)
app.include_router(status_router)


# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["system"])
async def health_check():
    """
    Simple health check for Docker and Cloud Run.
    Returns 200 OK when the app is running.
    """
    return {
        "status": "healthy",
        "service": "PitchIQ API",
        "version": "1.0.0",
        "environment": settings.environment,
    }

@app.get("/health/db", tags=["system"])
async def db_health_check():
    """
    Detailed database health check.
    """
    from database import test_connection, get_db_stats
    from scripts.db_health import check_health
    
    results = await check_health()
    return results

# ── Global Exception Handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches any unhandled exception and returns a clean JSON error.
    In production, we never expose internal error details to the client.
    """
    logger.exception(
        "unhandled.exception",
        path=str(request.url),
        method=request.method,
        # exc_info is captured by structlog automatically
    )

    detail = str(exc) if settings.environment == "development" else "Internal server error"

    return JSONResponse(
        status_code=500,
        content={"detail": detail, "job_id": None},
    )