"""
Todo API - Main application entry point

FastAPI application providing RESTful todo management with JWT authentication.
Features:
- Create, read, update, delete todos
- JWT-based authentication with user sessions
- Google OAuth integration
- Health check endpoint for monitoring
- Auto-generated interactive API docs at /docs
"""

import logging
import signal
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import todos, auth, chat
import asyncio

# Configure logging (console only, no file logging)
logging.basicConfig(
    level=logging.WARNING,  # Changed from INFO to WARNING to reduce noise
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Console only, no file handler
    ]
)
logger = logging.getLogger(__name__)

# Global flag for graceful shutdown
_SHUTDOWN_SIGNAL = False

def signal_handler(signum, frame):
    global _SHUTDOWN_SIGNAL
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    _SHUTDOWN_SIGNAL = True
    sys.exit(0)

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan event handler with graceful shutdown"""
    global _SHUTDOWN_SIGNAL
    logger.warning("Todo API starting up with JWT authentication...")  # Changed to warning level
    logger.warning("Server running on http://localhost:8000")
    logger.warning("Interactive API docs available at http://localhost:8000/docs")
    logger.warning("API endpoints available at /api")

    yield  # Application runs here

    logger.warning("Todo API shutting down gracefully...")
    # Perform cleanup operations here if needed
    # Close database connections, cancel background tasks, etc.

    # Force cleanup if needed
    tasks = [t for t in asyncio.all_tasks() if not t.done()]
    if tasks:
        logger.warning(f"Cancelling {len(tasks)} remaining tasks...")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


# Create FastAPI application instance
app = FastAPI(
    title="Todo API",
    description="RESTful API for managing todo items with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# Configure CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",  # Alternative localhost format
        "http://localhost:3001",  # Alternative port for Next.js
        "http://127.0.0.1:3001",  # Alternative localhost with port 3001
        "http://localhost:3002",  # Additional port for Next.js
        "http://127.0.0.1:3002",  # Alternative localhost with port 3002
        "http://0.0.0.0:3000",   # Docker/WSL compatibility
        "http://0.0.0.0:3001",   # Docker/WSL compatibility
        "http://0.0.0.0:3002",   # Docker/WSL compatibility
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PATCH, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include auth routes
app.include_router(auth.router)

# Include todo routes (protected)
app.include_router(todos.router)

# Include chat routes (protected)
app.include_router(chat.router)



@app.get("/health", tags=["health"], summary="Health check")
async def health_check():
    """
    Health check endpoint for monitoring

    Returns:
        dict: Server health status

    This endpoint is used by monitoring systems and deployment tools
    to verify the API server is running and responsive.
    """
    return {"status": "healthy"}
