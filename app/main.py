from contextlib import asynccontextmanager
from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import init_db

from .routes.auth import router as auth_router
from .routes.pages import router as pages_router
from .routes.planners import router as planner_router
from .routes.api import router as api_router


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


# ============================================================
# APPLICATION SETTINGS
# ============================================================

settings = get_settings()


# ============================================================
# APPLICATION LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs when the FastAPI application starts
    and when the application shuts down.
    """

    # Initialize database
    init_db()

    print()
    print("=" * 50)
    print("          PocketSmart AI - Starting")
    print("=" * 50)
    print(f"Application : {settings.app_name}")
    print("Database    : Initialized")

    if settings.gemini_api_key:
        print("Gemini      : Configured")
    else:
        print("Gemini      : NOT CONFIGURED")

    print("=" * 50)
    print()

    yield

    print()
    print("PocketSmart AI - Application stopped")
    print()


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title=settings.app_name,
    description=(
        "Budget-aware multimodal recommendation assistant "
        "for home interiors, party planning and jewelry."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ============================================================
# SESSION MIDDLEWARE
# ============================================================
#
# Required because templates use:
#
#     request.session.get("user")
#
# IMPORTANT:
# SessionMiddleware comes from STARLETTE,
# not fastapi.middleware.sessions.
#

SESSION_SECRET_KEY = os.getenv(
    "SESSION_SECRET_KEY",
    "pocketsmart-development-session-secret-key-2026"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    max_age=60 * 60 * 24 * 7,
    same_site="lax",
    https_only=False,
)


# ============================================================
# CORS MIDDLEWARE
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# STATIC FILES
# ============================================================

STATIC_DIR.mkdir(
    parents=True,
    exist_ok=True
)

app.mount(
    "/static",
    StaticFiles(
        directory=str(STATIC_DIR)
    ),
    name="static",
)


# ============================================================
# ROUTERS
# ============================================================

# Website pages
app.include_router(
    pages_router
)

# Authentication
app.include_router(
    auth_router
)

# Planner routes
app.include_router(
    planner_router
)

# API routes
app.include_router(
    api_router
)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():
    """
    Check whether PocketSmart AI is running.
    """

    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
    }


# ============================================================
# STARTUP CHECK
# ============================================================

@app.get("/startup")
async def startup():
    """
    Confirm that PocketSmart AI services
    are initialized.
    """

    return {
        "status": "initialized",
        "message": (
            "PocketSmart AI services are ready."
        ),
    }


# ============================================================
# APPLICATION STATUS
# ============================================================

@app.get("/status")
async def status():
    """
    Simple application status endpoint.
    """

    return {
        "application": settings.app_name,
        "version": "1.0.0",
        "status": "running",
    }


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )