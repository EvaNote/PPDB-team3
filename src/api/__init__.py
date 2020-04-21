from flask_restful import Api

from src.api.users import RegisterApi, AuthApi
from src.api.drives import DrivesApi, DriveApi, DrivePassengerApi

# setup API
api = Api(prefix="/api")
api.add_resource(RegisterApi, "/users/register")
api.add_resource(AuthApi, "/users/auth")
api.add_resource(DrivesApi, "/drives")
api.add_resource(DriveApi, "/drives/drive_id=<drive_id>")
api.add_resource(DrivePassengerApi, "/drives/drive_id=<drive_id>/passengers")
