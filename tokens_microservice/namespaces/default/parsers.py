"""Default namespace parsers."""

from flask_restx import reqparse

verify_parser = reqparse.RequestParser()
verify_parser.add_argument(
    'BookBNB_Authorization',
    type=str,
    location='headers',
    required=True,
    help="The bookbnb token of the requester",
)
verify_parser.add_argument(
    'token', type=str, location='json', required=True, help="The token to be verified"
)
