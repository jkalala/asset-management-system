from app.models.base import Base
from app.models.asset import Asset
from app.db.session import engine

def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables() 