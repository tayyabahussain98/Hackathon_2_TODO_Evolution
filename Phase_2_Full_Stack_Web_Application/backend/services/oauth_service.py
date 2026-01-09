"""
OAuth service layer - Google OAuth operations

Implements Google OAuth integration with Better Auth and JWT token generation.
This module provides OAuth business logic for the auth routes.
"""

import os
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import httpx
from urllib.parse import urlencode

from models.user import User
from services import auth_service, jwt_service


async def get_google_user_info(access_token: str) -> dict:
    """
    Get user info from Google using access token

    Args:
        access_token: Google OAuth access token

    Returns:
        User info dictionary with email, name, etc.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info from Google")

        return response.json()


async def create_or_get_oauth_user(email: str, google_id: str, db: AsyncSession) -> User:
    """
    Create a new user for OAuth or get existing user by Google ID or email

    Args:
        email: User's email from Google
        google_id: Google user ID
        db: Database session

    Returns:
        User object
    """
    # First, try to find existing user by Google ID
    existing_user = await auth_service.get_user_by_google_id(google_id, db)
    if existing_user:
        return existing_user

    # If no user found by Google ID, try to find by email
    existing_user = await auth_service.get_user_by_email(email, db)
    if existing_user:
        # Update the existing user with Google ID
        existing_user.google_id = google_id
        await db.commit()
        await db.refresh(existing_user)
        return existing_user

    # Create new user with Google ID
    temp_password = auth_service.generate_temp_password()
    return await auth_service.create_user_with_google_id(email, google_id, temp_password, db)


async def handle_google_oauth_callback(code: str, db: AsyncSession) -> dict:
    """
    Handle Google OAuth callback and return JWT token

    Args:
        code: Authorization code from Google
        db: Database session

    Returns:
        Dictionary with access_token and user info
    """
    # Exchange authorization code for tokens
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": f"{os.getenv('NEXT_PUBLIC_API_URL', 'http://localhost:8000')}/auth/callback/google",
        "grant_type": "authorization_code"
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code for tokens")

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="No access token received from Google")

        # Get user info from Google
        user_info = await get_google_user_info(access_token)
        email = user_info.get("email")
        google_id = user_info.get("id")

        if not email or not google_id:
            raise HTTPException(status_code=400, detail="Invalid user info from Google")

        # Create or get user
        user = await create_or_get_oauth_user(email, google_id, db)

        # Generate JWT token
        jwt_token = jwt_service.create_access_token(user.id, user.email)

        # Store session token in database
        await jwt_service.create_session_token(user.id, jwt_token, db)

        return {
            "access_token": jwt_token,
            "user": {
                "id": user.id,
                "email": user.email
            }
        }