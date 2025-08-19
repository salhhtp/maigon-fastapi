# app/auth.py
import httpx
from fastapi import Header, HTTPException, Depends
from typing import Optional
from app.config import settings

SUPABASE_USER_ENDPOINT = f"{settings.SUPABASE_URL}/auth/v1/user"


async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Validate the Supabase JWT by calling /auth/v1/user (simple and reliable).
    Returns a dict with user info (must include 'id' and 'email').
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    token = authorization.split("Bearer ")[-1].strip()
    headers = {"Authorization": f"Bearer {token}", "APIKey": settings.SUPABASE_ANON_KEY} if settings.SUPABASE_ANON_KEY else {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(SUPABASE_USER_ENDPOINT, headers=headers)
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = r.json()
    # return at least id and email
    return user
