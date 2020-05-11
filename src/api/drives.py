from flask import request, make_response, jsonify
from flask_restful import Resource, abort
from geopy import distance
from datetime import datetime, timedelta

from src.utils import user_access, ride_access, campus_access, address_access, car_access
from src.dbmodels.User import User
from src.dbmodels.Address import Address
from src.dbmodels.Ride import Ride


class DrivesApi(Resource):  # /api/drives
    def post(self):  # TODO make it work properly
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]
        if token is None:
            return abort(401)
        user_id = User.verify_auth_token(token)
        if user_id is None:
            return abort(401, message=str(user_id))
        # if logged in, continue
        data = request.json
        from_a = data.get("from")
        to_a = data.get("to")
        nr_seats = data.get("passenger-places")
        arrive_by = data.get("arrive-by")
        # check if from or to is a campus
        from_campus_id = campus_access.is_campus(from_a[0], from_a[1])
        to_campus_id = campus_access.is_campus(to_a[0], to_a[1])
        valid = False
        if from_campus_id is not None:
            campus_from = from_campus_id
            address_from = None
            valid = True
        else:
            campus_from = None
            address_from = Address(None, None, None, None, None, None, None, from_a[0], from_a[1])
            address_access.add_address(address_from)
            address_from = address_from.fetch_id()
        if to_campus_id is not None:
            campus_to = to_campus_id
            address_to = None
            valid = True
        else:
            campus_to = None
            address_to = Address(None, None, None, None, None, None, None, to_a[0], to_a[1])
            address_access.add_address(address_to)
            address_to = address_to.fetch_id()
        if not valid:
            return abort(400, message="This is Campus Carpool, so at least one of the addresses "
                                      "(departure or destination) has to be a campus.")
        fmt = '%Y-%m-%dT%H:%M:%S'
        dist = distance.distance((from_a[0], from_a[1]), (to_a[0], to_a[1])).km
        arr = datetime.strptime(arrive_by, fmt)
        time_diff_sec = timedelta(seconds=(dist / 0.01))
        depart_estimate = (arr - time_diff_sec).strftime(fmt).split('.')[0]
        cars = car_access.get_on_user_id(user_id)
        if len(cars) == 0:
            car = None
        else:
            car = cars[0].id
        new_ride = Ride(None, depart_estimate, arrive_by, user_id, car, nr_seats, None, None, None, campus_from,
                        campus_to, address_from, address_to)
        ride_access.add_ride(new_ride)
        ride_id = new_ride.fetch_id()
        resp = make_response({"id": ride_id, "driver_id": user_id, "passenger-ids": [], "passenger-places": nr_seats,
                              "from": from_a, "to": to_a, "arrive-by": arrive_by}, 201)
        resp.headers["Location"] = "/drives/" + str(ride_id)
        return resp


class DriveApi(Resource):  # /api/drives/{drive_id}
    def get(self, drive_id):
        if drive_id is None:
            return abort(400)
        ride = ride_access.get_on_id(drive_id)
        if ride is None or not drive_id.isdigit():
            return abort(400)
        rd = ride.to_dict()
        data = ride_access.get_data_for_api(drive_id)
        passengers = ride_access.get_passenger_ids(drive_id)
        result = {"id": rd["id"],
                  "driver_id": rd["user_id"],
                  "passenger-ids": passengers,
                  "passenger-places": data["passenger-places"],
                  "from": data["from"],
                  "to": data["to"],
                  "arrive-by": rd["arrival_time"].strftime("%Y/%m/%dT%H:%M:%S")
                  }
        return result, 200


class DrivePassengerApi(Resource):
    def get(self, drive_id):
        if drive_id is None or not drive_id.isdigit():
            return abort(400)
        passengers = ride_access.get_passenger_ids_names(drive_id)
        result = []
        for p in passengers:
            email = p['email']
            i = email.find('@')
            uname = email[0:i]
            result.append({
                "id": p['id'],
                "username": uname
            })
        return result, 200


class DrivePassengerRequestApi(Resource):
    def get(self, drive_id):
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]
        if token is None:
            return abort(401)
        user_id = user_access.get_user(User.verify_auth_token(token)).id
        if user_id is None or not user_id.isdigit():
            return abort(401)
        # we do not have passenger requests, so return empty list
        return [], 200

    def post(self, drive_id):
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]
        if token is None:
            return abort(401)
        user_id = user_access.get_user(User.verify_auth_token(token)).id
        if user_id is None or not isinstance(user_id, int) or not drive_id.isdigit():
            return abort(401)
        # 1) check if passenger is already subscribed for the given ride
        passengers = ride_access.get_passenger_ids(drive_id)
        if user_id in passengers:
            return {'status': 'rejected', 'reason': 'duplicate_request'}, 200
        # 2) check if car is fully occupied
        ride = ride_access.get_on_id(drive_id)
        if not passengers:
            ride_access.register_passenger(user_id, drive_id)
            return {'status': 'success'}, 201
        elif len(passengers) >= ride.passengers:
            return {'status': 'rejected', 'reason': 'car fully occupied'}, 200
        # 3) else: subscribe for the ride (= add to passenger_ride)
        else:
            ride_access.register_passenger(user_id, drive_id)
            return {'status': 'success'}, 201


class DrivePassengerRequestUserApi(Resource):
    def post(self, drive_id, user_id):
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]
        if token is None:
            return abort(401)
        current_user_id = user_access.get_user(User.verify_auth_token(token)).id
        if current_user_id is None or not user_id.isdigit() or not drive_id.isdigit() or not isinstance(current_user_id,
                                                                                                        int):
            return abort(401)
        # strategy: if user_id in passengers: return "accepted", else return "rejected"
        passengers = ride_access.get_passenger_ids(drive_id)
        for p in passengers:
            if int(p) == int(user_id):
                return {'status': 'accepted'}, 200
        return {'status': 'rejected'}, 200


class DrivesSearchAPI(Resource):
    def get(self):
        args = request.args
        # parse available arguments
        dict = {'fLat': None, 'fLng': None, 'tLat': None, 'tLng': None, 'arrive_by': None, 'limit': 5}
        for i in args:
            if i == 'from':
                dict['fLat'] = float(args[i].split(",")[0])
                dict['fLng'] = float(args[i].split(",")[1])
            elif i == 'to':
                dict['tLat'] = float(args[i].split(",")[0])
                dict['tLng'] = float(args[i].split(",")[1])
            else:
                dict[i] = args[i]
        if dict['fLat'] and dict['tLat']:
            rides = ride_access.api_match_rides_with_passenger(
                {'lat': dict['fLat'], 'lng': dict['fLng']},
                {'lat': dict['tLat'], 'lng': dict['tLng']},
                'Arrive by',
                dict['arrive_by'],
                dict['limit'])
        elif dict['fLat']:
            rides = ride_access.match_rides_with_passenger_missing_to(
                {'lat': dict['fLat'], 'lng': dict['fLng']},
                'Arrive by',
                dict['arrive_by'],
                dict['limit'])
        elif dict['tLat']:
            rides = ride_access.match_rides_with_passenger_missing_from(
                {'lat': dict['tLat'], 'lng': dict['tLng']},
                'Arrive by',
                dict['arrive_by'],
                dict['limit'])
        else:
            rides = ride_access.match_rides_with_passenger_missing_end_points(
                'Arrive by',
                dict['arrive_by'],
                dict['limit'])
        return rides, 200
