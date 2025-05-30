from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate

def get_asset(db: Session, asset_id: int) -> Optional[Asset]:
    return db.query(Asset).filter(Asset.id == asset_id).first()

def get_asset_by_serial(db: Session, serial_number: str) -> Optional[Asset]:
    return db.query(Asset).filter(Asset.serial_number == serial_number).first()

def get_assets(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[Asset]:
    query = db.query(Asset)
    
    if search:
        search_filter = or_(
            Asset.name.ilike(f"%{search}%"),
            Asset.serial_number.ilike(f"%{search}%"),
            Asset.category.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    return query.offset(skip).limit(limit).all()

def create_asset(db: Session, asset: AssetCreate) -> Asset:
    db_asset = Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def update_asset(
    db: Session,
    db_asset: Asset,
    asset_update: AssetUpdate
) -> Asset:
    update_data = asset_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_asset, field, value)
    
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def delete_asset(db: Session, asset_id: int) -> bool:
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if asset:
        db.delete(asset)
        db.commit()
        return True
    return False 