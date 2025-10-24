from sqlmodel import create_engine, SQLModel
import os
import logging
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
from sqlalchemy import text  # Add import for text()


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set. Copy .env.example to .env and set it.")


# echo=False in production; True while developing helps debugging SQL
engine = create_engine(DATABASE_URL, echo=True)

# Try a quick connection at import time so the module's `engine` points to a
# reachable database. If the configured DB is unreachable (DNS/network issues)
# we fall back to a local SQLite file so the rest of the application can run
# locally without crashing on startup.
try:
    with engine.connect() as _conn:
        pass
except Exception as exc:
    logging.error(
        "Could not connect to DATABASE_URL (%s): %s\nPlease check:\n1. Your network connection\n2. VPN status if using one\n3. Supabase database status",
        DATABASE_URL,
        exc,
    )
    raise  # Prevent fallback to SQLite so we can fix the real issue


def create_db_and_tables():
    """Create database tables.
    Attempts to connect to configured DATABASE_URL and create necessary tables.
    """
    global engine
    logging.info(f"Attempting to connect to database with URL: {DATABASE_URL}")
    
    try:
        # Try an explicit connection first
        with engine.connect() as conn:
            # Test query to verify full connectivity
            result = conn.execute(text("SELECT 1"))
            logging.info("Successfully connected to database!")
            
        SQLModel.metadata.create_all(engine)
        logging.info("✓ Database tables created successfully")
        
    except Exception as exc:
        logging.error(f"Database connection failed: {exc}")
        logging.error("Check your database URL and network connection")
        logging.error("Database URL format should be: postgresql://user:password@host:5432/dbname")
        raise  # Re-raise to prevent silent failures