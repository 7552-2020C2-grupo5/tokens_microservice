"""Constant values and defaults used in multiple modules."""

import enum

from tokens_microservice.cfg import config


class Services(enum.Enum):
    Bookings = "bookings"
    Middleware = "middleware"
    Notifications = "notifications"
    Publications = "publications"
    Reviews = "reviews"
    Users = "users"
    Recommendations = "recommendations"


DEFAULT_BOOKINGS_URL = "https://bookbnb5-bookings.herokuapp.com/v1/token"
DEFAULT_MIDDLEWARE_URL = "https://bookbnb5-middleware.herokuapp.com/v1/token"
DEFAULT_NOTIFICATIONS_URL = "https://bookbnb5-notifications.herokuapp.com/v1/token"
DEFAULT_PUBLICATIONS_URL = "https://bookbnb5-publications.herokuapp.com/v1/token"
DEFAULT_REVIEWS_URL = "https://bookbnb5-reviews.herokuapp.com/v1/token"
DEFAULT_USERS_URL = "https://bookbnb5-users-microservice.herokuapp.com/v1/token"
DEFAULT_RECOMMENDATIONS_URL = (
    "https://recommendations-microservice.herokuapp.com/v1/token"
)


SERVICES_REGISTER = {
    Services.Bookings: config.bookings.url(default=DEFAULT_BOOKINGS_URL),
    Services.Middleware: config.bookings.url(default=DEFAULT_MIDDLEWARE_URL),
    Services.Notifications: config.bookings.url(default=DEFAULT_NOTIFICATIONS_URL),
    Services.Publications: config.bookings.url(default=DEFAULT_PUBLICATIONS_URL),
    Services.Reviews: config.bookings.url(default=DEFAULT_REVIEWS_URL),
    Services.Users: config.bookings.url(default=DEFAULT_USERS_URL),
    Services.Recommendations: config.bookings.url(default=DEFAULT_RECOMMENDATIONS_URL),
}

SELF_TOKEN = "589adbb5-900c-4dc8-9b84-7ac359af7114"

ADMIN_VALIDATION_URL = (
    "https://bookbnb5-users-microservice.herokuapp.com/v1/admins/validate_token"
)
