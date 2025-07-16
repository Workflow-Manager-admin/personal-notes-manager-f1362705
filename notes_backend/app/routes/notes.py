from flask_smorest import Blueprint
from flask.views import MethodView
from flask import abort
from ..note_service import list_notes, get_note, create_note, update_note, delete_note
from ..schemas import NoteSchema, NoteCreateSchema, NoteUpdateSchema

blp = Blueprint(
    "Notes", "notes", url_prefix="/notes", description="CRUD operations for personal notes"
)

@blp.route("/")
class NotesList(MethodView):
    """
    Endpoint for listing and creating notes.
    """
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema(many=True))
    def get(self):
        """List all notes, ordered by most recently updated"""
        return list_notes()

    # PUBLIC_INTERFACE
    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteSchema)
    def post(self, note_data):
        """Create a new note"""
        note = create_note(note_data["title"], note_data["content"])
        return note

@blp.route("/<int:note_id>")
class NoteDetail(MethodView):
    """
    Endpoint for retrieving, updating, and deleting a single note.
    """
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema)
    def get(self, note_id):
        """Retrieve the details for a single note"""
        note = get_note(note_id)
        if not note:
            abort(404, description="Note not found")
        return note

    # PUBLIC_INTERFACE
    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteSchema)
    def patch(self, update_data, note_id):
        """Edit a note"""
        note = update_note(note_id, **update_data)
        if not note:
            abort(404, description="Note not found")
        return note

    # PUBLIC_INTERFACE
    @blp.response(204)
    def delete(self, note_id):
        """Delete a note"""
        deleted = delete_note(note_id)
        if not deleted:
            abort(404, description="Note not found")
        return None
