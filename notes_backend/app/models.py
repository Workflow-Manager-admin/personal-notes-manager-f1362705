from dataclasses import dataclass
from datetime import datetime

# PUBLIC_INTERFACE
@dataclass
class Note:
    """
    Represents a note object in the notes manager application.
    """
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_row(row: dict) -> 'Note':
        """Creates a Note from a database row dictionary."""
        return Note(
            id=row['id'],
            title=row['title'],
            content=row['content'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
