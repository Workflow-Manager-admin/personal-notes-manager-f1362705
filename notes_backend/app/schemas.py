from marshmallow import Schema, fields

# PUBLIC_INTERFACE
class NoteSchema(Schema):
    """
    Marshmallow schema representing a Note object (output schema).
    """
    id = fields.Int(required=True, description="Unique identifier")
    title = fields.Str(required=True, description="Note title")
    content = fields.Str(required=True, description="Note content")
    created_at = fields.DateTime(required=True, description="Creation date")
    updated_at = fields.DateTime(required=True, description="Last update date")

# PUBLIC_INTERFACE
class NoteCreateSchema(Schema):
    """
    Marshmallow schema for note creation (input schema).
    """
    title = fields.Str(required=True, description="Note title")
    content = fields.Str(required=True, description="Note content")

# PUBLIC_INTERFACE
class NoteUpdateSchema(Schema):
    """
    Marshmallow schema for note update (input schema).
    """
    title = fields.Str(required=False, description="Note title")
    content = fields.Str(required=False, description="Note content")
