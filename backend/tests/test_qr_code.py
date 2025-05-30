import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.base import Base
from app.models.asset import Asset
from app.core.qr_code import generate_qr_code, decode_qr_code
from app.api import deps

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[deps.get_db] = override_get_db

def test_generate_qr_code():
    """Test QR code generation"""
    asset_data = {
        "id": 1,
        "name": "Test Asset",
        "serial_number": "SN123456",
        "category": "IT Equipment"
    }
    
    # Generate QR code
    qr_code = generate_qr_code(asset_data)
    assert qr_code is not None
    
    # Decode QR code
    decoded_data = decode_qr_code(qr_code)
    assert decoded_data["id"] == asset_data["id"]
    assert decoded_data["name"] == asset_data["name"]
    assert decoded_data["serial_number"] == asset_data["serial_number"]

def test_qr_code_api_endpoint(test_db):
    """Test QR code generation API endpoint"""
    # First create an asset
    asset_data = {
        "name": "Test Asset",
        "category": "IT Equipment",
        "serial_number": "SN123456",
        "purchase_date": datetime.now().isoformat(),
        "purchase_price": 1000.00,
        "status": "active"
    }
    create_response = client.post("/api/v1/assets/", json=asset_data)
    asset_id = create_response.json()["id"]
    
    # Get QR code
    response = client.get(f"/api/v1/assets/{asset_id}/qr")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Verify QR code contains asset data
    qr_data = decode_qr_code(response.content)
    assert qr_data["id"] == asset_id
    assert qr_data["name"] == asset_data["name"]
    assert qr_data["serial_number"] == asset_data["serial_number"]

def test_qr_code_scan_endpoint(test_db):
    """Test QR code scanning API endpoint"""
    # First create an asset
    asset_data = {
        "name": "Test Asset",
        "category": "IT Equipment",
        "serial_number": "SN123456",
        "purchase_date": datetime.now().isoformat(),
        "purchase_price": 1000.00,
        "status": "active"
    }
    create_response = client.post("/api/v1/assets/", json=asset_data)
    asset_id = create_response.json()["id"]
    
    # Generate QR code
    qr_response = client.get(f"/api/v1/assets/{asset_id}/qr")
    qr_code = qr_response.content
    
    # Scan QR code
    response = client.post("/api/v1/assets/scan", files={"file": ("qr.png", qr_code, "image/png")})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == asset_id
    assert data["name"] == asset_data["name"]
    assert data["serial_number"] == asset_data["serial_number"] 