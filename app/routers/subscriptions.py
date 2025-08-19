# app/routers/subscriptions.py
from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Subscription
from app.schemas import SubscriptionOut

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("/", response_model=list[SubscriptionOut])
async def list_subscriptions(user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # list subscriptions for user's company
    user_id = user["id"]
    q = await db.execute(select(Subscription).where(Subscription.company_id == (await get_company_id_for_user(db, user_id))))
    subs = q.scalars().all()
    return subs


# helper
async def get_company_id_for_user(db: AsyncSession, user_id: str):
    from app.models import User
    q = await db.execute(select(User).where(User.id == user_id))
    u = q.scalar_one_or_none()
    return u.company_id if u else None
