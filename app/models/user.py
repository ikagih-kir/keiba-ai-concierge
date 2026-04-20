from sqlalchemy import Column, BigInteger, String, Enum, Integer, DateTime
from app.db.base import Base
import enum
from datetime import datetime
from sqlalchemy.orm import relationship




class RegisterStatus(enum.Enum):
    temp = "temp"
    active = "active"
    suspended = "suspended"
    withdrawn = "withdrawn"


class PaymentStatus(enum.Enum):
    unpaid = "unpaid"
    paid = "paid"


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    nickname = Column(String(100))
    email = Column(String(255))
    register_status = Column(Enum(RegisterStatus), nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False)
    total_payment = Column(Integer, default=0)
    last_access_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

