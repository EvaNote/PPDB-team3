from flask_restful import Api

from src.api.users import RegisterApi, AuthApi

from src.api.drives import DrivesSearchAPI, DriveApi, DrivePassengerApi, DrivePassengerRequestApi, \
    DrivePassengerRequestUserApi

# setup API
api = Api(prefix="/api")
api.add_resource(RegisterApi, "/users/register")
api.add_resource(AuthApi, "/users/auth")
api.add_resource(DrivesApi, "/drives")
api.add_resource(DrivesSearchAPI, "/drives/search")
api.add_resource(DriveApi, "/drives/drive_id=<drive_id>")
api.add_resource(DrivePassengerApi, "/drives/drive_id=<drive_id>/passengers")
api.add_resource(DrivePassengerRequestApi, "/drives/drive_id=<drive_id>/passenger-request")
api.add_resource(DrivePassengerRequestUserApi, "/drives/drive_id=<drive_id>/passenger-request/user_id=<user_id>")
