"""Services namespace controller."""
from tokens_microservice.constants import Services


def get_all_services():
    return [x.value for x in Services]
