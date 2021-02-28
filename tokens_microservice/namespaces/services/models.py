"""Services namespace models module."""

from flask_restx import Model, fields

services_model = Model(
    "Services",
    {
        "services": fields.List(
            fields.String("The service name"), description="All valid services."
        )
    },
)
