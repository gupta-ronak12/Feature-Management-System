from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from app.database.database import Base


class FeatureFlag(Base):
    __tablename__ = "feature_flags"

    id = Column(Integer, primary_key=True, index=True)

    key = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    flag_type = Column(String(20), nullable=False)
    default_value = Column(JSON, nullable=False)

    enabled = Column(Boolean, default=True, nullable=False)

    owner_team = Column(String(150), nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )