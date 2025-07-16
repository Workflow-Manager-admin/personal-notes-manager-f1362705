import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

# PUBLIC_INTERFACE
def get_db_connection():
    """
    Returns a new PostgreSQL database connection using environment variables.
    """
    return psycopg2.connect(
        host=os.environ.get("NOTES_DB_HOST", "localhost"),
        database=os.environ.get("NOTES_DB_NAME", "notes"),
        user=os.environ.get("NOTES_DB_USER", "postgres"),
        password=os.environ.get("NOTES_DB_PASSWORD", "password"),
        port=int(os.environ.get("NOTES_DB_PORT", 5432)),
        cursor_factory=RealDictCursor
    )

@contextmanager
def db_cursor():
    """
    Context manager for obtaining a database cursor with automatic commit/rollback.
    """
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
