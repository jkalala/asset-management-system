from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.db.init_db import SessionLocal

def seed_assets():
    db = SessionLocal()
    try:
        # Sample assets data
        assets = [
            Asset(
                name="Dell XPS 15 Laptop",
                description="High-performance development laptop",
                serial_number="DLXPS15-2023-001",
                category="IT Equipment",
                location="IT Department",
                status="ACTIVE",
                purchase_date=datetime.now() - timedelta(days=180),
                purchase_price=1999.99,
                current_value=1799.99,
                last_maintenance_date=datetime.now() - timedelta(days=30),
                next_maintenance_date=datetime.now() + timedelta(days=150),
                asset_metadata={"specs": {"ram": "32GB", "storage": "1TB SSD", "processor": "Intel i9"}}
            ),
            Asset(
                name="Canon EOS R5 Camera",
                description="Professional photography camera",
                serial_number="CNR5-2023-002",
                category="Photography Equipment",
                location="Media Department",
                status="ACTIVE",
                purchase_date=datetime.now() - timedelta(days=120),
                purchase_price=3499.99,
                current_value=3299.99,
                last_maintenance_date=datetime.now() - timedelta(days=15),
                next_maintenance_date=datetime.now() + timedelta(days=165),
                asset_metadata={"specs": {"resolution": "45MP", "lens": "24-70mm f/2.8"}}
            ),
            Asset(
                name="HP LaserJet Pro M404dn",
                description="Office printer",
                serial_number="HPLJ-2023-003",
                category="Office Equipment",
                location="Main Office",
                status="ACTIVE",
                purchase_date=datetime.now() - timedelta(days=90),
                purchase_price=299.99,
                current_value=249.99,
                last_maintenance_date=datetime.now() - timedelta(days=45),
                next_maintenance_date=datetime.now() + timedelta(days=135),
                asset_metadata={"specs": {"type": "Laser", "pages_per_minute": "40"}}
            ),
            Asset(
                name="Samsung 65\" QLED TV",
                description="Conference room display",
                serial_number="SMSQL-2023-004",
                category="AV Equipment",
                location="Conference Room A",
                status="ACTIVE",
                purchase_date=datetime.now() - timedelta(days=60),
                purchase_price=1499.99,
                current_value=1399.99,
                last_maintenance_date=None,
                next_maintenance_date=datetime.now() + timedelta(days=300),
                asset_metadata={"specs": {"resolution": "4K", "refresh_rate": "120Hz"}}
            ),
            Asset(
                name="Cisco Meraki MX84",
                description="Network security appliance",
                serial_number="CSMX-2023-005",
                category="Network Equipment",
                location="Server Room",
                status="ACTIVE",
                purchase_date=datetime.now() - timedelta(days=150),
                purchase_price=899.99,
                current_value=799.99,
                last_maintenance_date=datetime.now() - timedelta(days=60),
                next_maintenance_date=datetime.now() + timedelta(days=240),
                asset_metadata={"specs": {"throughput": "500Mbps", "ports": "8"}}
            ),
            Asset(
                name="Herman Miller Aeron Chair",
                description="Ergonomic office chair",
                serial_number="HMA-2023-006",
                category="Furniture",
                location="CEO Office",
                status="ACTIVE",
                purchase_date=datetime.now() - timedelta(days=30),
                purchase_price=1299.99,
                current_value=1199.99,
                last_maintenance_date=None,
                next_maintenance_date=datetime.now() + timedelta(days=330),
                asset_metadata={"specs": {"size": "B", "color": "Graphite"}}
            ),
            Asset(
                name="DJI Mavic 3 Pro",
                description="Professional drone",
                serial_number="DJM3-2023-007",
                category="Photography Equipment",
                location="Media Department",
                status="MAINTENANCE",
                purchase_date=datetime.now() - timedelta(days=45),
                purchase_price=2199.99,
                current_value=1999.99,
                last_maintenance_date=datetime.now() - timedelta(days=5),
                next_maintenance_date=datetime.now() + timedelta(days=25),
                asset_metadata={"specs": {"camera": "4/3 CMOS", "flight_time": "46min"}}
            ),
            Asset(
                name="Apple Mac Studio",
                description="Professional workstation",
                serial_number="APMS-2023-008",
                category="IT Equipment",
                location="Design Department",
                status="ACTIVE",
                purchase_date=datetime.now() - timedelta(days=20),
                purchase_price=3999.99,
                current_value=3899.99,
                last_maintenance_date=None,
                next_maintenance_date=datetime.now() + timedelta(days=340),
                asset_metadata={"specs": {"processor": "M2 Ultra", "ram": "64GB"}}
            ),
            Asset(
                name="Sony WH-1000XM5",
                description="Noise-cancelling headphones",
                serial_number="SNWH-2023-009",
                category="Audio Equipment",
                location="IT Department",
                status="ACTIVE",
                purchase_date=datetime.now() - timedelta(days=15),
                purchase_price=399.99,
                current_value=379.99,
                last_maintenance_date=None,
                next_maintenance_date=datetime.now() + timedelta(days=345),
                asset_metadata={"specs": {"battery_life": "30h", "bluetooth": "5.2"}}
            ),
            Asset(
                name="Epson EB-1781W",
                description="Portable projector",
                serial_number="EPEB-2023-010",
                category="AV Equipment",
                location="Meeting Room B",
                status="RETIRED",
                purchase_date=datetime.now() - timedelta(days=365),
                purchase_price=699.99,
                current_value=0.00,
                last_maintenance_date=datetime.now() - timedelta(days=30),
                next_maintenance_date=None,
                asset_metadata={"specs": {"resolution": "1280x800", "brightness": "3000 lumens"}}
            )
        ]

        # Add all assets to the database
        for asset in assets:
            db.add(asset)
        
        # Commit the changes
        db.commit()
        print("Successfully added 10 sample assets to the database.")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_assets() 