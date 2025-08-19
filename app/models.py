# app/models.py
from sqlalchemy import (
    Column, String, Integer, DateTime, ForeignKey, Text, Boolean, JSON, Numeric
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base


class Company(Base):
    __tablename__ = "companies"
    id = Column(String, primary_key=True)  # use uuid strings (we'll set them from code)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)  # will store supabase user id (uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", backref="users")


class Plan(Base):
    __tablename__ = "plans"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    price_cents = Column(Integer, nullable=False)
    monthly = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    plan_id = Column(String, ForeignKey("plans.id"), nullable=False)
    stripe_subscription_id = Column(String, nullable=True)
    quota_remaining = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company")
    plan = relationship("Plan")


class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)  # path in Supabase storage
    contract_type = Column(String, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company")
    user = relationship("User")


class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    status = Column(String, default="pending")  # pending, running, completed, failed
    result_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)

    document = relationship("Document")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True)
    company_id = Column(String, ForeignKey("companies.id"))
    stripe_event = Column(JSON, nullable=True)
    amount_cents = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UsageLog(Base):
    __tablename__ = "usage_logs"
    id = Column(String, primary_key=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    action = Column(String, nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
