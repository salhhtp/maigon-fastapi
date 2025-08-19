# app/routers/documents.py
from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user
from app.db import get_db
from app.crud import create_document
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import DocumentCreate, DocumentOut
import uuid

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/", response_model=DocumentOut)
async def create_doc(payload: DocumentCreate, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Create a document record in DB. The front end should upload the file to Supabase Storage
    and then call this endpoint with storage_path pointing to the stored file.
    """
    # Validate user and company
    user_id = user["id"]
    company_id = payload.id.split("-")[0] if False else None  # placeholder; ensure proper company id on client
    # In ensure_user we saved company if metadata had it; fetch user record from DB instead of this hack
    # Simpler: fetch local user row to read company_id - but to minimize code here, require company_id passed in payload or derived.
    # For now assume frontend includes company_id in payload.id or add payload.company_id in schema.
    # We'll refactor: expect company_id in storage path or pass it.
    # To keep example moving, assume user has company_id via supabase metadata and ensure_user set it.

    # Use a simple generation for doc id if not provided
    doc_id = payload.id if getattr(payload, "id", None) else str(uuid.uuid4())
    payload.id = doc_id
    # create doc record
    # Need company_id -> get it via DB user record
    from sqlalchemy.future import select
    from app.models import User
    q = await db.execute(select(User).where(User.id == user_id))
    local_user = q.scalar_one_or_none()
    if not local_user:
        raise HTTPException(status_code=400, detail="Local user not found")
    doc = await create_document(db, payload, user_id=local_user.id, company_id=local_user.company_id or "unknown")
    return doc
