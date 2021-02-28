"""Custom exceptions."""


class ServerTokenDoesNotExist(Exception):
    pass


class InvalidServerToken(Exception):
    pass


class ServerAlreadyRegistered(Exception):
    pass
