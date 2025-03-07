"""Services namespace module."""

from flask_restx import Namespace, Resource

from tokens_microservice.utils import validate_admin_request

from .controller import get_all_services
from .models import services_model
from .parsers import admin_parser

ns = Namespace("Services", description="Services operations.")

ns.models[services_model.name] = services_model


@ns.route('')
class ServiceDiscovery(Resource):
    @ns.marshal_with(services_model)
    @ns.expect(admin_parser)
    @ns.response(403, "Unauthorized")
    @ns.response(200, "Ok")
    def get(self):
        """Get all services."""
        args = admin_parser.parse_args()
        if not validate_admin_request(args.Authorization):
            return {"message": "Unauthorized"}, 403
        return {"services": get_all_services()}, 200
