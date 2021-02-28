"""Services namespace module."""

from flask_restx import Namespace, Resource

from .controller import get_all_services
from .models import services_model

ns = Namespace("Services", description="Services operations.")

ns.models[services_model.name] = services_model


@ns.route('/services')
class ServiceDiscovery(Resource):
    @ns.marshal_with(services_model)
    def get(self):
        """Get all services."""
        return {"services": get_all_services()}
