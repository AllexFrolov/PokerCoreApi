from flask_restx import Api

from .healthcheck import api as hc


api = Api(
    title='PokerCoreAPI',
    version='1.0',
    description='',
    )

api.add_namespace(hc)
