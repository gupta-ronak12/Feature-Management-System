from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from app.database.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    action = Column(String(50), nullable=False)
    performed_by = Column(String(150), nullable=True)

    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )