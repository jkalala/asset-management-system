from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class AssetStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    MAINTENANCE = "MAINTENANCE"
    RETIRED = "RETIRED"
    DISPOSED = "DISPOSED"

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    serial_number = Column(String, unique=True, index=True)
    category = Column(String, nullable=False)
    location = Column(String)
    status = Column(Enum(AssetStatus), nullable=False, default=AssetStatus.ACTIVE)
    purchase_date = Column(DateTime, nullable=False)
    purchase_price = Column(Float, nullable=False)
    current_value = Column(Float)
    last_maintenance_date = Column(DateTime, nullable=True)
    next_maintenance_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    asset_metadata = Column(JSON, nullable=True) 