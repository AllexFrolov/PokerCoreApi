#pylint: disable=missing-docstring
from flask_restx import Namespace, Resource, fields
from core.model import make_action
from schemas import Actions, PokerStage

ROUTE = 'DecisionMaker'

api = Namespace(ROUTE, description='make action')

get_decision_exp = api.model(
    f'/{ROUTE}/get_decision/expect', {
        'hand': fields.List(fields.String(required=True, description='Hero hand'),
                            default=['7d', '2h'], min_items=2, max_items=2),
        'board': fields.List(fields.String, default=[], min_items=0, max_items=5),
        'pot': fields.Float(required=True, default=1.5, description='Pot'),
        'stage': fields.String(required=True, description='Stage',
                               enum=[name for name, _ in PokerStage.__members__.items()]),
        'positions': fields.List(fields.Integer, default=[0], min_items=1, max_items=9),
        'action_sequence': fields.List(fields.Integer, default=[0], min_items=1, max_items=9),
        'players_stats': fields.Raw(required=True)
        })

get_decision_resp = api.model(
    f'/{ROUTE}/get_decision/response', {
        'action': fields.String(required=True, description='Action', enum=[name for name, _ in Actions.__members__.items()]),
        'win_rate': fields.Float(required=True, description='Win rate'),
        'bet_size': fields.Float(required=True, description='Bet size'),
        'expectation': fields.Float(required=True, description='math expectation'),
        'opp_possible_combs': fields.List(fields.Integer),
        })


@api.route('/get_decision')
class PlayerStats(Resource):
    @api.doc('make action')
    @api.expect(get_decision_exp)
    @api.marshal_with(get_decision_resp, code=200)
    def post(self):
        return make_action(**api.payload), 200
