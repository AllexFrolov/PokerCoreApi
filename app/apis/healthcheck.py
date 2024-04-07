from flask_restx import Namespace, Resource, fields

ROUTE = 'HealthCheck'

api = Namespace(ROUTE)

healthcheck = api.model(f'/{ROUTE}', {
    'status': fields.Boolean(readonly=True)
})

@api.route('/')
class HealthCheck(Resource):
    @api.marshal_with(healthcheck)
    def get(self):
        return {'status': True}
