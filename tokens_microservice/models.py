"""SQLAlchemy models."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import validates

from tokens_microservice.exceptions import ServerAlreadyRegistered
from tokens_microservice.utils import uuid_str

db = SQLAlchemy()


class ServerToken(db.Model):  # type:ignore
    """Server token model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    server_name = db.Column(db.String, unique=False, nullable=False)
    token = db.Column(db.String, unique=True, nullable=False, default=uuid_str)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    blocked_at = db.Column(db.DateTime, nullable=True)
    blocked = db.Column(db.Boolean, nullable=False, default=False)

    @validates("server_name")
    def validate_server_name(self, _key, server_name):
        server_token = ServerToken.query.filter(
            (ServerToken.server_name == server_name)
            & (ServerToken.blocked == False)  # noqa: E712
        ).first()
        if server_token is not None and server_token.id != self.id:
            raise ServerAlreadyRegistered
        return server_name
