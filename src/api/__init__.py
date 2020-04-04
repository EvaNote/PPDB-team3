from flask_restful import Api

from src.api.users import RegisterApi, AuthApi

# setup API
api = Api(prefix="/api")
api.add_resource(RegisterApi, "/users/register")
api.add_resource(AuthApi, "/users/auth")
