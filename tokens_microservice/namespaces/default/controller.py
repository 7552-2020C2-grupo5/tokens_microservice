"""Default namespace logic."""

from datetime import datetime as dt

from tokens_microservice.exceptions import InvalidServerToken, ServerTokenDoesNotExist
from tokens_microservice.models import ServerToken, db


def get_all_server_tokens():
    return ServerToken.query.all()


def create_server_token(server_name):
    new_server_token = ServerToken(server_name=server_name)
    db.session.add(new_server_token)
    db.session.commit()
    return new_server_token


def delete_server_token(server_token_id):
    server_token = ServerToken.query.filter(ServerToken.id == server_token_id).first()
    if server_token is None:
        raise ServerTokenDoesNotExist
    server_token.blocked = True
    server_token.blocked_at = dt.utcnow()
    db.session.merge(server_token)
    db.session.commit()


def validate_server_token(server_token):
    server_token = ServerToken.query.filter(
        (ServerToken.token == server_token)
        & (ServerToken.blocked == False)  # noqa: E712
    ).first()
    if server_token is None:
        raise InvalidServerToken
