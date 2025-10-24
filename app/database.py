from sqlmodel import create_engine, SQLModel
import os
import logging
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError


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
    logging.warning(
        "Initial connection to DATABASE_URL failed (%s): %s — falling back to local SQLite ./dev.db",
        DATABASE_URL,
        exc,
    )
    engine = create_engine("sqlite:///./dev.db", echo=True)


def create_db_and_tables():
    """Create database tables.

    If the configured DATABASE_URL is unreachable (for example a remote
    Postgres instance that cannot be resolved/reached), this function will
    fall back to a local SQLite file database at `./dev.db` so the app can
    continue running locally during development.
    """
    global engine
    try:
        # Try an explicit connection first so we can detect unreachable hosts
        # and fall back before any table creation attempts.
        with engine.connect() as conn:
            pass
        SQLModel.metadata.create_all(engine)
        logging.info("Database tables created using DATABASE_URL")
    except Exception as exc:
        # Don't crash the whole application on startup; log and fall back.
        logging.warning(
            "Could not connect to DATABASE_URL (%s): %s. Falling back to local SQLite ./dev.db",
            DATABASE_URL,
            exc,
        )
        engine = create_engine("sqlite:///./dev.db", echo=True)
        SQLModel.metadata.create_all(engine)
        logging.info("Database tables created using fallback SQLite database ./dev.db")