from fastapi.testclient import TestClient
from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.base import Base
from app.db.session import get_db

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_asset(test_db):
    """Test creating a new asset via API"""
    asset_data = {
        "name": "Test Asset",
        "category": "IT Equipment",
        "serial_number": "SN123456",
        "purchase_date": datetime.now().isoformat(),
        "purchase_price": 1000.00,
        "status": "active",
        "location": "Office A",
        "metadata": {"warranty": "2 years", "supplier": "Test Supplier"}
    }
    
    response = client.post("/api/v1/assets/", json=asset_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == asset_data["name"]
    assert data["serial_number"] == asset_data["serial_number"]
    assert "id" in data

def test_get_asset(test_db):
    """Test retrieving an asset"""
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
    
    # Then retrieve it
    response = client.get(f"/api/v1/assets/{asset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == asset_data["name"]
    assert data["serial_number"] == asset_data["serial_number"]

def test_list_assets(test_db):
    """Test listing all assets"""
    # Create multiple assets
    assets = [
        {
            "name": f"Test Asset {i}",
            "category": "IT Equipment",
            "serial_number": f"SN{i}",
            "purchase_date": datetime.now().isoformat(),
            "purchase_price": 1000.00,
            "status": "active"
        }
        for i in range(3)
    ]
    
    for asset in assets:
        client.post("/api/v1/assets/", json=asset)
    
    response = client.get("/api/v1/assets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_update_asset(test_db):
    """Test updating an asset"""
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
    
    # Update the asset
    update_data = {
        "name": "Updated Asset",
        "status": "maintenance"
    }
    response = client.patch(f"/api/v1/assets/{asset_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["status"] == update_data["status"]

def test_delete_asset(test_db):
    """Test deleting an asset"""
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
    
    # Delete the asset
    response = client.delete(f"/api/v1/assets/{asset_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/assets/{asset_id}")
    assert get_response.status_code == 404 