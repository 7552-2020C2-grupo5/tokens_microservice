"""Helper functions for the project."""
import uuid

import requests

from tokens_microservice.cfg import config
from tokens_microservice.constants import ADMIN_VALIDATION_URL, SELF_TOKEN


def uuid_str() -> str:
    return str(uuid.uuid4())


def validate_admin_request(admin_token):
    r = requests.get(
        config.admin_validation_url(default=ADMIN_VALIDATION_URL),
        headers={
            "Authorization": admin_token,
            "BookBNBAuthorization": config.self_token(default=SELF_TOKEN),
        },
    )
    return r.ok


class FilterParam:
    """Filter a query based on an op and param"""

    def __init__(
        self,
        name,
        op,
        _in="query",
        schema="int",
        transform=None,
        format_=None,
        attribute=None,
        default=None,
    ):
        """Filter by operation.

        Parameters
        ----------
        name: Name for the filter.
        op: Operation to filter with.
        _in: Where the parameter is located.
        schema: The type for swagger documentation.
        transform: Pre-transform val.
        format_: Format for swagger.
        attribute: If none, uses name. The attribute to filter on.
        default: Default value.
        """

        self.name = name
        self.op = op
        self.val = None
        self.attribute = attribute or self.name
        self.__schema__ = {"name": name, "in": _in, "type": schema, "format": format_}
        self.transform = transform
        self.default = default

    def identity(self, x):
        return x

    def __call__(self, val=None):
        if not self.default and not val:
            raise ValueError("Should provide val or default value")
        self.val = (self.transform or self.identity)(val or self.default)
        return self

    def apply(self, query, model):
        if "." in self.attribute:
            child_class, child_attr = self.attribute.split(".")
            child_class_ = model.__mapper__.relationships[child_class].mapper.class_
            return query.filter(
                getattr(model, child_class).any(
                    self.op(getattr(child_class_, child_attr), self.val)
                )
            )
        try:
            return query.filter(self.op(getattr(model, self.attribute), self.val))
        except NotImplementedError:  # hack for contains
            return query.filter(
                getattr(getattr(model, self.attribute), self.op.__name__)(self.val)
            )

    def __repr__(self):
        return f"filter {self.name} by {self.op}"

    def __str__(self):
        return self.__repr__()
