# app/routers/reviews.py
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from app.auth import get_current_user
from app.db import get_db
from app.crud import create_analysis
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
import httpx

router = APIRouter(prefix="/reviews", tags=["reviews"])


async def call_analysis_service(document_id: str, storage_path: str, contract_type: str, analysis_id: str):
    """
    This runs in the background and posts the file / metadata to the AI/Edge service,
    then writes the result back via a callback to an endpoint or via direct DB update (Edge service can POST to our webhook).
    """
    payload = {"document_id": document_id, "storage_path": storage_path, "contract_type": contract_type, "analysis_id": analysis_id}
    async with httpx.AsyncClient(timeout=120) as client:
        url = f"{settings.ANALYSIS_API_URL.rstrip('/')}/analyze"
        try:
            r = await client.post(url, json=payload)
            r.raise_for_status()
        except Exception as e:
            # In a real app, update Analysis row as failed; edges will call our webhook when done
            print("Analysis invocation failed:", e)


@router.post("/", summary="Create a review job")
async def create_review(document_id: str, contract_type: str, background_tasks: BackgroundTasks, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Create a review job and call the edge service in background.
    The front end must supply document_id and contract_type.
    """
    # create analysis DB row
    analysis = await create_analysis(db, document_id=document_id)
    # get storage_path from document row
    from sqlalchemy.future import select
    from app.models import Document
    q = await db.execute(select(Document).where(Document.id == document_id))
    doc = q.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    # call the edge in background
    background_tasks.add_task(call_analysis_service, document_id, doc.storage_path, contract_type, analysis.id)
    return {"analysis_id": analysis.id, "status": "pending"}
