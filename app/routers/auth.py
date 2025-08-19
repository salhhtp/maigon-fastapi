# app/routers/auth.py
from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.db import get_db
from app.crud import ensure_user
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
async def me(user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Any:
    """
    Returns current Supabase user info + ensures a local user record exists.
    Pass Authorization: Bearer <token>
    """
    # create or update local user
    local_user = await ensure_user(db, user)
    return {"user": user, "local_user": {"id": local_user.id, "email": local_user.email, "company_id": local_user.company_id}}
