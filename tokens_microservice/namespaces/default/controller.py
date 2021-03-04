"""Default namespace logic."""

from datetime import datetime as dt

import requests

from tokens_microservice.cfg import config
from tokens_microservice.constants import SELF_TOKEN, SERVICES_REGISTER, Services
from tokens_microservice.exceptions import InvalidServerToken, ServerTokenDoesNotExist
from tokens_microservice.models import ServerToken, db


def get_all_server_tokens():
    return ServerToken.query.all()


def create_server_token(server_name):
    new_server_token = ServerToken(server_name=server_name)
    db.session.add(new_server_token)
    db.session.commit()
    url = SERVICES_REGISTER[Services(server_name)]
    r = requests.post(
        url,
        json={"token": new_server_token.token},
        headers={"BookBNBAuthorization": config.self_token(default=SELF_TOKEN)},
    )
    r.raise_for_status()
    return new_server_token


def delete_server_token(server_token_id):
    server_token = ServerToken.query.filter(ServerToken.id == server_token_id).first()
    if server_token is None:
        raise ServerTokenDoesNotExist
    server_token.blocked = True
    server_token.blocked_at = dt.utcnow()
    db.session.merge(server_token)
    db.session.commit()
    url = SERVICES_REGISTER[Services(server_token.server_name)]
    r = requests.delete(
        url, headers={"BookBNBAuthorization": config.self_token(default=SELF_TOKEN)}
    )
    r.raise_for_status()


def validate_server_token(server_token):
    if server_token == config.self_token(default=SELF_TOKEN):
        return
    server_token = ServerToken.query.filter(
        (ServerToken.token == server_token)
        & (ServerToken.blocked == False)  # noqa: E712
    ).first()
    if server_token is None:
        raise InvalidServerToken
