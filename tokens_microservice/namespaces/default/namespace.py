"""Default namespace module."""

from flask_restx import Namespace, Resource

from tokens_microservice.exceptions import (
    InvalidServerToken,
    ServerAlreadyRegistered,
    ServerTokenDoesNotExist,
)
from tokens_microservice.utils import validate_admin_request

from .controller import (
    create_server_token,
    delete_server_token,
    get_all_server_tokens,
    validate_server_token,
)
from .models import created_model, token_model
from .parsers import admin_parser, register_parser, verify_parser

ns = Namespace("Tokens", description="Server tokens operations.")

ns.models[created_model.name] = created_model
ns.models[token_model.name] = token_model


@ns.route('')
class TokenResource(Resource):
    @ns.doc('get_tokens')
    @ns.response(403, "Unauthorized")
    @ns.marshal_with(token_model)
    @ns.expect(admin_parser)
    def get(self):
        """Get all server tokens"""
        if not validate_admin_request(admin_parser.parse_args().Authorization):
            return {"message": "Unauthorized"}, 403
        return get_all_server_tokens()

    @ns.doc('create_token')
    @ns.expect(register_parser)
    @ns.response(403, "Unauthorized")
    @ns.response(400, "Server already registered")
    @ns.response(200, "Server registered", model=created_model)
    @ns.response(500, "Internal error")
    def post(self):
        """Create a new server token."""
        args = register_parser.parse_args()
        if not validate_admin_request(args.Authorization):
            return {"message": "Unauthorized"}, 403
        try:
            return ns.marshal(create_server_token(args.server_name), created_model)
        except ServerAlreadyRegistered:
            return {"message": "Server is already registered"}, 400
        except Exception as e:  # pylint:disable=broad-except
            ns.logger.error("Error deleting", exc_info=e)
            return {"message": "Error deleting"}, 500


@ns.route('/<int:server_token_id>')
class ServerTokenResource(Resource):
    @ns.doc('block_token')
    @ns.expect(admin_parser)
    @ns.response(200, "Token blocked")
    @ns.response(404, "Token does not exist")
    @ns.response(403, "Unauthorized")
    @ns.response(500, "Internal error")
    def delete(self, server_token_id):
        """Block server token."""
        if not validate_admin_request(admin_parser.parse_args().Authorization):
            return {"message": "Unauthorized"}, 403
        try:
            delete_server_token(server_token_id)
            return {"message": "Token blocked"}, 200
        except ServerTokenDoesNotExist:
            return {"message": "Token does not exist"}, 404
        except Exception as e:  # pylint:disable=broad-except
            ns.logger.error("Error deleting", exc_info=e)
            return {"message": "Error deleting"}, 500


@ns.route('/verification')
class ServerTokenVerification(Resource):
    @ns.doc('verify_token')
    @ns.response(200, "Valid token")
    @ns.response(400, "Invalid token")
    @ns.response(403, "Unauthorized")
    @ns.expect(verify_parser)
    def post(self):
        """Create a verification request."""
        args = verify_parser.parse_args()
        try:
            validate_server_token(args.BookBNB_Authorization)
        except InvalidServerToken:
            return {"message": "Unauthorized"}, 403

        try:
            validate_server_token(args.token)
        except InvalidServerToken:
            return {"message": "Invalid token"}, 400
        return {"message": "Token is valid."}
