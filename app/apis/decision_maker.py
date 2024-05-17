#pylint: disable=missing-docstring
from flask_restx import Namespace, Resource, fields
from core.model import make_action
from schemas import Actions, PokerStage, PossibleCombs, PlayerTypes
from .examples.decision_maker_defaults import example

ROUTE = 'DecisionMaker'

api = Namespace(ROUTE, description='compute action')
pl_types = [name for name, _ in PlayerTypes.__members__.items()]
stages = [name for name, _ in PokerStage.__members__.items()]

player_stats_model = api.model('PlayerStats', {
    'stack': fields.Float(required=True, description='Player stack'),
    'bet': fields.Float(required=True, description='Player bet'),
    'call_size': fields.Float(required=True, description='Player call size'),
    'active': fields.Boolean(required=True, description='Is player active'),
    'dealer': fields.Boolean(required=True, description='Is player a dealer'),
    'all_in': fields.Boolean(required=True, description='Is player all-in'),
    'sit_out': fields.Boolean(required=True, description='Is player sitting out'),
})

players_stats_model = api.model("PlayersStats", {player_type: fields.Nested(player_stats_model) for player_type in pl_types})

get_decision_exp = api.model(
    f'/{ROUTE}/make_decision/expect', {
        'hand': fields.List(fields.String(required=True, description='Hero hand'),
                            default=example['hand'], min_items=2, max_items=2),
        'board': fields.List(fields.String, default=example['board'], min_items=0, max_items=5),
        'pot': fields.Float(required=True, default=example['pot'], description='Pot'),
        'stage': fields.String(required=True, default=example['stage'], description='Stage', enum=stages),
        'positions': fields.List(
            fields.String, 
            default=example['positions'], 
            enum=pl_types, 
            min_items=1, 
            max_items=9,
            description="""Queue of players in a hand. 
            Example: ["OPP_1", "OPP_2", "HERO"] 0 index (OPP_1) - SB, 1 (OPP_2) - BB, last index (HERO) - BTN.
            All players are needed, even if they have folded.
            """
            ),
        'action_sequence': fields.List(
            fields.String, 
            default=example['action_sequence'], 
            enum=pl_types, 
            min_items=1, 
            max_items=9,
            description='Who will play after the hero if he plays passively. Do not include folded players'),
        'players_stats': fields.Nested(players_stats_model, default=example['players_stats'])
        })


get_decision_resp = api.model(
    f'/{ROUTE}/make_decision/response', {
        'action': fields.String(required=True, description='Action', enum=[name for name, _ in Actions.__members__.items()]),
        'win_rate': fields.Float(required=True, description='Win rate'),
        'bet_size': fields.Float(required=True, description='Bet size'),
        'expectation': fields.Float(required=True, description='math expectation'),
        'opp_possible_combs': PossibleCombs
        })


@api.route('/get_decision')
class PlayerStats(Resource):
    @api.doc('make action')
    @api.expect(get_decision_exp)
    @api.marshal_with(get_decision_resp, code=200)
    def get(self):
        return make_action(**api.payload), 200
