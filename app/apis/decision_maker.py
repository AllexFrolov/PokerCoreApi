from flask_restx import Namespace, Resource, fields
from schemas import Actions
from core.model import make_action

ROUTE = 'DecisionMaker'

api = Namespace(ROUTE, description='make action')

get_decision_exp = api.model(
    f'/{ROUTE}/get_decision/expect', {
        'hand': fields.List(fields.String(required=True, description='Hero hand'), default=['7d', '2h'], min_items=2, max_items=2),
        'board': fields.List(fields.String, min_items=0, max_items=5),
        'pot': fields.Float(required=True, description='Pot'),
        'stage': fields.String(required=True, description='Stage', enum=['preflop', 'flop', 'turn', 'river']),
        })

get_decision_resp = api.model(
    f'/{ROUTE}/get_decision/response', {
        'action': fields.String(required=True, description='Action', enum=['push', 'fold']),
        'win_rate': fields.Float(required=True, description='Win rate'),
        })


@api.route('/get_decision')
class PlayerStats(Resource):
    @api.doc('make action')
    @api.expect(get_decision_exp)
    @api.marshal_with(get_decision_resp, code=200)
    def post(self):
        hand = api.payload['hand']
        board = api.payload['board']
        return make_action(hand, board), 200
