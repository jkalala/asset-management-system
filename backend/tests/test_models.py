import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.base import Base
from app.models.asset import Asset
from app.core.config import settings

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_create_asset(db_session):
    """Test creating a new asset"""
    asset = Asset(
        name="Test Asset",
        category="IT Equipment",
        serial_number="SN123456",
        purchase_date=datetime.now(),
        purchase_price=1000.00,
        status="active",
        location="Office A",
        metadata={"warranty": "2 years", "supplier": "Test Supplier"}
    )
    
    db_session.add(asset)
    db_session.commit()
    
    # Verify the asset was created
    saved_asset = db_session.query(Asset).first()
    assert saved_asset.name == "Test Asset"
    assert saved_asset.category == "IT Equipment"
    assert saved_asset.serial_number == "SN123456"
    assert saved_asset.status == "active"
    assert saved_asset.metadata["warranty"] == "2 years"

def test_asset_validation(db_session):
    """Test asset validation rules"""
    with pytest.raises(ValueError):
        asset = Asset(
            name="",  # Empty name should raise error
            category="IT Equipment",
            serial_number="SN123456",
            purchase_date=datetime.now(),
            purchase_price=1000.00,
            status="active"
        )
        db_session.add(asset)
        db_session.commit()

def test_asset_status_transition(db_session):
    """Test asset status transitions"""
    asset = Asset(
        name="Test Asset",
        category="IT Equipment",
        serial_number="SN123456",
        purchase_date=datetime.now(),
        purchase_price=1000.00,
        status="active"
    )
    
    db_session.add(asset)
    db_session.commit()
    
    # Test valid status transition
    asset.status = "maintenance"
    db_session.commit()
    assert asset.status == "maintenance"
    
    # Test invalid status transition
    with pytest.raises(ValueError):
        asset.status = "invalid_status"
        db_session.commit() 