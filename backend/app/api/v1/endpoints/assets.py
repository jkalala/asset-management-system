from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Response
from sqlalchemy.orm import Session
import logging
from sqlalchemy.exc import SQLAlchemyError

from app.api import deps
from app.crud import asset as crud
from app.schemas.asset import Asset, AssetCreate, AssetUpdate
from app.core.qr_code import generate_qr_code, decode_qr_code
import json
from app.api.deps import get_db
from app.models.asset import Asset as DBAsset, AssetStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[Asset])
def get_assets(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all assets")
        assets = db.query(DBAsset).all()
        logger.info(f"Found {len(assets)} assets")
        return assets
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching assets: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while fetching assets: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.post("/", response_model=Asset)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating new asset: {asset.name}")
        db_asset = DBAsset(**asset.dict())
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        logger.info(f"Successfully created asset with ID: {db_asset.id}")
        return db_asset
    except SQLAlchemyError as e:
        logger.error(f"Database error while creating asset: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while creating asset: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/{asset_id}", response_model=Asset)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching asset with ID: {asset_id}")
        asset = db.query(DBAsset).filter(DBAsset.id == asset_id).first()
        if asset is None:
            logger.warning(f"Asset not found with ID: {asset_id}")
            raise HTTPException(status_code=404, detail="Asset not found")
        return asset
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching asset: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while fetching asset: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.put("/{asset_id}", response_model=Asset)
def update_asset(asset_id: int, asset: AssetUpdate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Updating asset with ID: {asset_id}")
        db_asset = db.query(DBAsset).filter(DBAsset.id == asset_id).first()
        if db_asset is None:
            logger.warning(f"Asset not found with ID: {asset_id}")
            raise HTTPException(status_code=404, detail="Asset not found")
        
        update_data = asset.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_asset, key, value)
        
        db.commit()
        db.refresh(db_asset)
        logger.info(f"Successfully updated asset with ID: {asset_id}")
        return db_asset
    except SQLAlchemyError as e:
        logger.error(f"Database error while updating asset: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while updating asset: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting asset with ID: {asset_id}")
        db_asset = db.query(DBAsset).filter(DBAsset.id == asset_id).first()
        if db_asset is None:
            logger.warning(f"Asset not found with ID: {asset_id}")
            raise HTTPException(status_code=404, detail="Asset not found")
        
        db.delete(db_asset)
        db.commit()
        logger.info(f"Successfully deleted asset with ID: {asset_id}")
        return {"message": "Asset deleted successfully"}
    except SQLAlchemyError as e:
        logger.error(f"Database error while deleting asset: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while deleting asset: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/{asset_id}/qr", response_class=Response)
def get_asset_qr(
    *,
    db: Session = Depends(deps.get_db),
    asset_id: int
):
    """
    Generate and return a QR code for the asset.
    """
    asset = crud.get_asset(db=db, asset_id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    qr_data = {
        "id": asset.id,
        "name": asset.name,
        "serial_number": asset.serial_number,
        "category": asset.category
    }
    qr_code = generate_qr_code(qr_data)
    return Response(content=qr_code, media_type="image/png")

@router.post("/scan")
def scan_asset_qr(
    file: UploadFile = File(...)
):
    """
    Scan a QR code image and return the asset data encoded in it.
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    image_bytes = file.file.read()
    try:
        data = decode_qr_code(image_bytes)
    except ImportError as e:
        logger.error(f"QR code decoding is not available: {str(e)}")
        raise HTTPException(status_code=500, detail=f"QR code decoding is not available: {str(e)}")
    except ValueError as e:
        logger.error(f"Invalid QR code: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid QR code: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    return data 