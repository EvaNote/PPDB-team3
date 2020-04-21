from flask import request, make_response
from flask_restful import Resource, abort
from geopy import distance
from datetime import datetime, timedelta

from src.utils import user_access, ride_access, campus_access, address_access, geolocator
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
        if from_campus_id is not None:
            to_campus = False
            campus = from_campus_id
            address = to_a
        elif to_campus_id is not None:
            to_campus = True
            campus = to_campus_id
            address = from_a
        else:
            return abort(400, message="This is Campus Carpool, so at least one of the addresses "
                                      "(departure or destination) has to be a campus.")
        # make new address
        location = geolocator.reverse(str(address[0]) + ", " + str(address[1]))
        try:
            housenr = location.raw['address']['house_number']
        except Exception as e:
            housenr = ''
        try:
            road = location.raw['address']['road']
        except Exception as e:
            road = ''
            housenr = ''  # no road = no housenumber
        try:
            town = location.raw['address']['town']
        except Exception as e:
            try:
                town = location.raw['address']['city_district']
            except Exception as e:
                town = ''
        try:
            postcode = location.raw['address']['postcode']
        except Exception as e:
            postcode = ''
        fmt = '%Y-%m-%dT%H:%M:%S.%f'
        dist = distance.distance((from_a[0], from_a[1]), (to_a[0], to_a[1])).km
        arr = datetime.strptime(arrive_by, fmt)
        time_diff_sec = timedelta(seconds=(dist / 0.01))
        depart_estimate = (arr - time_diff_sec).strftime(fmt).split('.')[0]
        address_access.add_address(Address(None, "Belgium", town, postcode, road, housenr, address[0], address[1]))
        addr_id = address_access.get_id("Belgium", town, postcode, road, housenr)
        new_ride = Ride(None, depart_estimate, arrive_by, user_id, addr_id, campus, to_campus, None, nr_seats, None, None, None)
        ride_access.add_ride(new_ride)
        ride_id = ride_access.get_id_on_all(depart_estimate, arrive_by, user_id, addr_id, campus)
        resp = make_response({"id": ride_id, "driver_id": user_id, "passenger-ids": [], "passenger-places": nr_seats,
                              "from": from_a, "to": to_a, "arrive-by": arrive_by}, 201)
        resp.headers["Location"] = "/drives/" + str(ride_id)
        return resp


class DriveApi(Resource):  # /api/drives/{drive_id}
    def get(self, drive_id):
        if drive_id is None:
            return abort(400)
        ride = ride_access.get_on_id(drive_id)
        if ride is None:
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
        if drive_id is None:
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
