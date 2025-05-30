from sqlalchemy.orm import Session

from app.models.base import Base
from app.db.session import engine

def init_db(db: Session) -> None:
    """Initialize the database with all tables."""
    Base.metadata.create_all(bind=engine) 