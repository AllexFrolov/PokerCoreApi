from flask_restx import Namespace, Resource, fields

ROUTE = 'DecisionMaker'

api = Namespace(ROUTE, description='make action')

get_decision_exp = api.model(
    f'/{ROUTE}/get_decision/expect', {
        'hand': fields.List(fields.String(required=True, description='Hero hand'), min_items=2, max_items=2),
        'board': fields.List(fields.String, min_items=0, max_items=5),
        })

get_decision_resp = api.model(
    f'/{ROUTE}/get_decision/response', {
        'action': fields.String(required=True,description='Action', enum=['push', 'fold'], ),
        })


@api.route('/get_decision')
class PlayerStats(Resource):
    @api.doc('make action')
    @api.expect(get_decision_exp)
    @api.marshal_with(get_decision_resp, code=200)
    def get(self):
        return 'push', 200
