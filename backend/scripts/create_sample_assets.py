import sys
import os
from datetime import datetime, timedelta
import random

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.crud import asset as crud
from app.schemas.asset import AssetCreate

# Sample data
categories = ["Laptop", "Server", "Network Equipment", "Printer", "Mobile Device"]
locations = ["Office A", "Office B", "Data Center", "Warehouse", "Remote"]
statuses = ["ACTIVE", "MAINTENANCE", "RETIRED", "DISPOSED"]

def create_sample_assets():
    db = SessionLocal()
    try:
        for i in range(50):
            # Generate a unique serial number
            serial_number = f"SN{random.randint(10000, 99999)}"
            
            # Generate a random purchase date within the last 2 years
            days_ago = random.randint(0, 730)
            purchase_date = datetime.now() - timedelta(days=days_ago)
            
            # Create the asset
            asset_in = AssetCreate(
                name=f"Asset {i+1}",
                category=random.choice(categories),
                serial_number=serial_number,
                purchase_date=purchase_date,
                purchase_price=round(random.uniform(100.0, 5000.0), 2),
                status=random.choice(statuses),
                location=random.choice(locations),
                asset_metadata={
                    "manufacturer": f"Manufacturer {random.randint(1, 5)}",
                    "model": f"Model {random.randint(100, 999)}",
                    "warranty_expires": (purchase_date + timedelta(days=365)).isoformat()
                }
            )
            
            # Create the asset in the database
            crud.create_asset(db=db, asset=asset_in)
            print(f"Created asset: {asset_in.name} ({asset_in.serial_number})")
            
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_assets() 