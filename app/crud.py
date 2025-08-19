# app/crud.py
import uuid
from sqlalchemy.future import select
from sqlalchemy import insert
from app.models import Company, User, Plan, Subscription, Document, Analysis
from app.schemas import DocumentCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def get_or_create_company(session: AsyncSession, name: str) -> Company:
    # naive: try to find by name, otherwise create
    q = await session.execute(select(Company).where(Company.name == name))
    comp = q.scalar_one_or_none()
    if comp:
        return comp
    comp = Company(id=str(uuid.uuid4()), name=name)
    session.add(comp)
    await session.commit()
    await session.refresh(comp)
    return comp


async def ensure_user(session: AsyncSession, user_info: dict):
    # user_info from supabase contains at least 'id', 'email', optionally 'user_metadata' for name/company
    user_id = user_info["id"]
    q = await session.execute(select(User).where(User.id == user_id))
    user = q.scalar_one_or_none()
    if user:
        return user
    # create company from metadata if present
    company_id = None
    company_name = None
    if user_info.get("user_metadata"):
        company_name = user_info["user_metadata"].get("company")
    if company_name:
        comp = await get_or_create_company(session, company_name)
        company_id = comp.id
    user = User(id=user_id, email=user_info["email"], full_name=user_info.get("user_metadata", {}).get("full_name"), company_id=company_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def create_document(session: AsyncSession, doc_in: DocumentCreate, user_id: str, company_id: str):
    doc = Document(id=doc_in.id, filename=doc_in.filename, storage_path=doc_in.storage_path, contract_type=doc_in.contract_type, user_id=user_id, company_id=company_id)
    session.add(doc)
    await session.commit()
    await session.refresh(doc)
    return doc


async def create_analysis(session: AsyncSession, document_id: str):
    import uuid
    anal = Analysis(id=str(uuid.uuid4()), document_id=document_id, status="pending")
    session.add(anal)
    await session.commit()
    await session.refresh(anal)
    return anal
