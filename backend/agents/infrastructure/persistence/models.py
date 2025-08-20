from sqlalchemy import Column, String, Text, DateTime, Integer, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class AgentModel(Base):
    __tablename__ = 'agents'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    tools = Column(JSON, default=[])
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class ToolModel(Base):
    __tablename__ = 'tools'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String, nullable=False)  # e.g., 'prebuilt', 'custom'
    config = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class ExecutionModel(Base):
    __tablename__ = 'executions'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, nullable=False)
    query = Column(Text, nullable=False)
    steps = Column(JSON, default=[])
    result = Column(Text)
    status = Column(String, nullable=False)  # e.g., 'running', 'completed', 'failed'
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
