from flask import request
from flask_restful import Resource, abort
from src.utils import user_access, ride_access, car_access
from src.dbmodels.User import User


class DrivesApi(Resource):
    def get(self):  # TODO make it work properly
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]
        if token is None:
            return abort(401)
        user = user_access.get_user(User.verify_auth_token(token))
        if user is not None:
            return {"user_id": user.id}, 201
        abort(401)


class DriveApi(Resource):
    def get(self, drive_id):
        if drive_id is None:
            return abort(400)
        ride = ride_access.get_on_id(drive_id)
        if ride is None:
            return abort(400)
        rd = ride.to_dict()
        data = ride_access.get_data_for_api(drive_id)
        return {"id": rd["id"], "driver_id": rd["user_id"], "passenger-ids": [], "passenger-places": data["passenger-places"],
                "from": data["from"], "to": data["to"], "arrive-by": rd["arrival_time"]}, 200
