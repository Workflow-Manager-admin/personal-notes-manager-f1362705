from .db import db_cursor
from .models import Note
from datetime import datetime

# PUBLIC_INTERFACE
def list_notes():
    """
    Returns all notes, ordered by latest updated.
    """
    with db_cursor() as cur:
        cur.execute("SELECT * FROM notes ORDER BY updated_at DESC;")
        rows = cur.fetchall()
        return [Note.from_row(row) for row in rows]

# PUBLIC_INTERFACE
def get_note(note_id: int):
    """
    Gets a note by its ID.
    """
    with db_cursor() as cur:
        cur.execute("SELECT * FROM notes WHERE id = %s;", (note_id,))
        row = cur.fetchone()
        return Note.from_row(row) if row else None

# PUBLIC_INTERFACE
def create_note(title: str, content: str):
    """
    Creates a new note and returns it.
    """
    now = datetime.utcnow()
    with db_cursor() as cur:
        cur.execute(
            "INSERT INTO notes (title, content, created_at, updated_at) VALUES (%s, %s, %s, %s) RETURNING *;",
            (title, content, now, now),
        )
        row = cur.fetchone()
        return Note.from_row(row)

# PUBLIC_INTERFACE
def update_note(note_id: int, title: str = None, content: str = None):
    """
    Updates an existing note.
    """
    now = datetime.utcnow()
    set_clauses = []
    values = []
    if title is not None:
        set_clauses.append("title = %s")
        values.append(title)
    if content is not None:
        set_clauses.append("content = %s")
        values.append(content)
    if not set_clauses:
        return get_note(note_id)
    set_clauses.append("updated_at = %s")
    values.append(now)
    values.append(note_id)
    set_sql = ", ".join(set_clauses)
    sql = f"UPDATE notes SET {set_sql} WHERE id = %s RETURNING *;"
    with db_cursor() as cur:
        cur.execute(sql, tuple(values))
        row = cur.fetchone()
        return Note.from_row(row) if row else None

# PUBLIC_INTERFACE
def delete_note(note_id: int):
    """
    Deletes a note by its ID.
    """
    with db_cursor() as cur:
        cur.execute("DELETE FROM notes WHERE id = %s RETURNING *;", (note_id,))
        row = cur.fetchone()
        return Note.from_row(row) if row else None
