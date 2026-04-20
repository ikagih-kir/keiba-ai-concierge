from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class OperationLog(Base):
    __tablename__ = "operation_logs"

    id = Column(BigInteger, primary_key=True)
    admin_id = Column(BigInteger, nullable=False)
    admin_email = Column(String(255), nullable=False)
    action = Column(String(50), nullable=False)
    target_type = Column(String(50), nullable=False)
    target_id = Column(BigInteger, nullable=False)
    detail = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
