#!/usr/bin/env python3
"""
Production-ready orchestrator for the Todo API application.

This script provides optimized startup with:
- Performance-tuned configurations
- Graceful shutdown handling
- Resource optimization
- Production-ready settings
"""

import asyncio
import signal
import sys
import os
import logging
from typing import Optional
from contextlib import asynccontextmanager

import uvicorn
from main import app  # Import the main FastAPI app

# Suppress overly verbose logging
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

class ApplicationOrchestrator:
    """Manages the lifecycle of the Todo API application."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8000, workers: int = 1):
        self.host = host
        self.port = port
        self.workers = workers
        self._shutdown_requested = False

    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n🛑 Received signal {signum}, initiating graceful shutdown...")
        self._shutdown_requested = True
        sys.exit(0)

    def register_signal_handlers(self):
        """Register signal handlers for graceful shutdown."""
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

    def start(self):
        """Start the application server."""
        print("🚀 Starting Todo API server...")
        print(f"📍 Listening on {self.host}:{self.port}")
        print("⚡ Optimized for high-performance operation")

        # Register signal handlers
        self.register_signal_handlers()

        # Start the Uvicorn server with optimized settings
        uvicorn.run(
            "main:app",
            host=self.host,
            port=self.port,
            reload=False,  # Production mode - no hot reload
            workers=self.workers,
            log_level="warning",  # Reduced logging for performance
            timeout_keep_alive=30,
            timeout_graceful_shutdown=5,  # Graceful shutdown timeout
            loop="asyncio",
            http="httptools",  # High-performance HTTP parser
            ws="websockets",   # WebSocket implementation
            proxy_headers=True,  # Support for reverse proxies
            forwarded_allow_ips="*",  # Allow forwarded IPs
        )

def main():
    """Main entry point for the application orchestrator."""
    # Get configuration from environment or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    workers = int(os.getenv("WORKERS", "1"))

    # Create and start the orchestrator
    orchestrator = ApplicationOrchestrator(host=host, port=port, workers=workers)
    orchestrator.start()

if __name__ == "__main__":
    main()