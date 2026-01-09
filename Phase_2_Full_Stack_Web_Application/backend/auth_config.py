import os
from fastapi import FastAPI
from typing import Optional, Dict, Any


class MockBetterAuth:
    """Mock implementation of Better Auth for local development"""

    def __init__(self, secret: str, database_url: str):
        self.secret = secret
        self.database_url = database_url
        self.oauth_providers = {}

    def add_oauth_provider(self, provider):
        """Add an OAuth provider"""
        if hasattr(provider, 'name'):
            self.oauth_providers[provider.name] = provider

    def create_route(self):
        """Create a FastAPI app for auth routes"""
        app = FastAPI()

        @app.get("/google")
        async def google_oauth():
            # This would redirect to Google OAuth in a real implementation
            return {"message": "Google OAuth endpoint - mock implementation"}

        @app.get("/callback/google")
        async def google_callback(code: str):
            # This would handle the Google OAuth callback in a real implementation
            return {"code": code, "message": "Google OAuth callback - mock implementation"}

        return app


class MockGoogleProvider:
    """Mock Google OAuth provider"""

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.name = "google"


# Initialize mock Better Auth with environment variables
auth = MockBetterAuth(
    secret=os.getenv("BETTER_AUTH_SECRET", "fallback-secret-key-change-in-production"),
    database_url=os.getenv("DATABASE_URL", "sqlite:///better_auth.db"),
)

# Add Google OAuth provider with environment variables
if os.getenv("GOOGLE_CLIENT_ID") and os.getenv("GOOGLE_CLIENT_SECRET"):
    google_provider = MockGoogleProvider(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )
    auth.add_oauth_provider(google_provider)

# Export the auth instance
better_auth = auth