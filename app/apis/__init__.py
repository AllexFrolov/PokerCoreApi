from flask_restx import Api

from .healthcheck import api as hc
from .decision_maker import api as dm


api = Api(
    title='PokerCoreAPI',
    version='1.0',
    description='',
    )

api.add_namespace(hc)
api.add_namespace(dm)
