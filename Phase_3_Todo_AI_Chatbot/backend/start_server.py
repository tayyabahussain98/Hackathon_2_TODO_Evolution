#!/usr/bin/env python3
"""
Main orchestrator script to run the Todo API application.

This script serves as the primary entry point for the application and handles:
- Proper initialization of the FastAPI application
- Graceful startup and shutdown procedures
- Configuration management
- Process management
"""

import asyncio
import signal
import sys
import os
from contextlib import asynccontextmanager

import uvicorn
from main import app  # Import the main FastAPI app

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print(f"\nReceived signal {signum}, initiating graceful shutdown...")
    sys.exit(0)

def main():
    """Main entry point for the application."""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    print("🚀 Starting Todo API server...")
    print("📚 Loading configuration and initializing services...")

    # Start the Uvicorn server with optimized settings
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload in production for better performance
        workers=1,     # Adjust based on your needs
        log_level="warning",  # Reduced logging for better performance
        timeout_keep_alive=30,  # Keep-alive timeout
        loop="asyncio",
        http="httptools",  # Use httptools for better performance
    )

if __name__ == "__main__":
    main()