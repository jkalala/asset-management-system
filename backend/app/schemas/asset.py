from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class AssetBase(BaseModel):
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    serial_number: str = Field(..., min_length=1)
    purchase_date: datetime
    purchase_price: float = Field(..., gt=0)
    status: str = Field(..., pattern="^(ACTIVE|MAINTENANCE|RETIRED|DISPOSED)$")
    location: Optional[str] = None
    asset_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1)
    serial_number: Optional[str] = Field(None, min_length=1)
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = Field(None, gt=0)
    status: Optional[str] = Field(None, pattern="^(ACTIVE|MAINTENANCE|RETIRED|DISPOSED)$")
    location: Optional[str] = None
    asset_metadata: Optional[Dict[str, Any]] = None

class AssetInDB(AssetBase):
    id: int
    created_at: datetime
    updated_at: datetime
    qr_code: Optional[str] = None
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class Asset(AssetInDB):
    pass 