"""Default namespace models module."""

from flask_restx import Model, fields

from tokens_microservice.constants import Services

register_model = Model(
    "New server",
    {
        "server_name": fields.String(
            required=True,
            description="The service to register",
            enum=[e.value for e in Services],
        )
    },
)

created_model = Model(
    "Created server",
    {
        "server_name": fields.String(
            required=True,
            description="The service to register",
            enum=[e.value for e in Services],
        ),
        "token": fields.String(description="The token"),
    },
)

token_model = Model(
    "Server token",
    {
        "id": fields.Integer(description="Id", required=True),
        "server_name": fields.String(
            required=True,
            description="The service to register",
            enum=[e.value for e in Services],
        ),
        "blocked": fields.Boolean(description="Is the token blocked?"),
        "created_at": fields.DateTime(description="Creation date"),
        "blocked_at": fields.DateTime(description="Blocking date"),
    },
)

verification_model = Model(
    "Server token verification",
    {"token": fields.String(description="The token to validate")},
)
