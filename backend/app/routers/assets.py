from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.deps import get_db
from app.models.asset import Asset as AssetModel
from app.schemas.asset import AssetCreate, AssetUpdate, Asset

router = APIRouter()

@router.get("/assets/", response_model=List[Asset])
def get_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        assets = db.query(AssetModel).offset(skip).limit(limit).all()
        return assets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assets/", response_model=Asset)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    try:
        db_asset = AssetModel(**asset.dict())
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assets/{asset_id}", response_model=Asset)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    try:
        asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
        if asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")
        return asset
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/assets/{asset_id}", response_model=Asset)
def update_asset(asset_id: int, asset: AssetUpdate, db: Session = Depends(get_db)):
    try:
        db_asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
        if db_asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        for key, value in asset.dict(exclude_unset=True).items():
            setattr(db_asset, key, value)
        
        db.commit()
        db.refresh(db_asset)
        return db_asset
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/assets/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    try:
        db_asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
        if db_asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        db.delete(db_asset)
        db.commit()
        return {"message": "Asset deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 