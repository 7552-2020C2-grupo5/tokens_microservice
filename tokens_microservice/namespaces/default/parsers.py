"""Default namespace parsers."""

from flask_restx import reqparse

from tokens_microservice.constants import Services

admin_parser = reqparse.RequestParser()
admin_parser.add_argument(
    'Authorization',
    type=str,
    location='headers',
    required=True,
    help="The bookbnb admin user jwt of the requester",
)

register_parser = admin_parser.copy()
register_parser.add_argument(
    "server_name",
    choices=[e.value for e in Services],
    help="The server to register",
    required=True,
    location='json',
)

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
