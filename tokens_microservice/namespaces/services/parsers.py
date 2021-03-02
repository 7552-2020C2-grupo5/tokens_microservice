"""Services parsers."""

from flask_restx import reqparse

admin_parser = reqparse.RequestParser()
admin_parser.add_argument(
    'Authorization',
    type=str,
    location='headers',
    required=True,
    help="The bookbnb admin user jwt of the requester",
)
