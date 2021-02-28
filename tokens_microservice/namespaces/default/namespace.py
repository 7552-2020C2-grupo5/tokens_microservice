"""Default namespace module."""

from flask_restx import Namespace, Resource

from tokens_microservice.exceptions import (
    InvalidServerToken,
    ServerAlreadyRegistered,
    ServerTokenDoesNotExist,
)

from .controller import (
    create_server_token,
    delete_server_token,
    get_all_server_tokens,
    validate_server_token,
)
from .models import created_model, register_model, token_model, verification_model

ns = Namespace("Tokens", description="Server tokens operations.")

ns.models[created_model.name] = created_model
ns.models[register_model.name] = register_model
ns.models[token_model.name] = token_model
ns.models[verification_model.name] = verification_model


@ns.route('')
class TokenResource(Resource):
    @ns.doc('get_tokens')
    @ns.marshal_with(token_model)
    def get(self):
        """Get all server tokens"""
        return get_all_server_tokens()

    @ns.doc('create_token')
    @ns.expect(register_model)
    @ns.response(400, "Server already registered")
    @ns.response(200, "Server registered", model=created_model)
    def post(self):
        """Create a new server token."""
        data = ns.payload
        try:
            return ns.marshal(create_server_token(**data), created_model)
        except ServerAlreadyRegistered:
            return {"message": "Server is already registered"}, 400


@ns.route('/<int:server_token_id>')
class ServerTokenResource(Resource):
    @ns.doc('block_token')
    @ns.response(200, "Token blocked")
    @ns.response(404, "Token does not exist")
    def delete(self, server_token_id):
        """Block server token."""
        try:
            delete_server_token(server_token_id)
            return {"message": "Token blocked"}, 200
        except ServerTokenDoesNotExist:
            return {"message": "Token does not exist"}, 404


@ns.route('/verification')
class ServerTokenVerification(Resource):
    @ns.doc('verify_token')
    @ns.response(200, "Valid token")
    @ns.response(400, "Invalid token")
    @ns.expect(verification_model)
    def post(self):
        try:
            validate_server_token(ns.payload.get("token"))
            return {"message": "valid token"}, 200
        except InvalidServerToken:
            return {"message": "invalid token"}, 400
