# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List, Dict


class UserBase(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    company_id: Optional[str] = None

    class Config:
        orm_mode = True


class PlanOut(BaseModel):
    id: str
    name: str
    price_cents: int
    monthly: bool
    metadata: Optional[Dict] = None

    class Config:
        orm_mode = True


class SubscriptionOut(BaseModel):
    id: str
    plan: PlanOut
    quota_remaining: int
    active: bool

    class Config:
        orm_mode = True


class DocumentCreate(BaseModel):
    id: str
    filename: str
    storage_path: str
    contract_type: Optional[str]


class DocumentOut(BaseModel):
    id: str
    filename: str
    storage_path: str
    contract_type: Optional[str]

    class Config:
        orm_mode = True


class AnalysisCreate(BaseModel):
    id: str
    document_id: str


class AnalysisOut(BaseModel):
    id: str
    document_id: str
    status: str
    result_json: Optional[dict]

    class Config:
        orm_mode = True
