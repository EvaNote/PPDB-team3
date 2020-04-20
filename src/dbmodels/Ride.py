class Ride:
    def __init__(self, id, departure_time, arrival_time, user_id, address_1, campus, to_campus, car_id, passengers, p1, p2, p3):
        # address_to & address_from are id's pointing to addresses
        self.id = id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.user_id = user_id
        self.address_1 = address_1
        self.campus = campus
        self.to_campus = to_campus
        self.car_id = car_id
        self.passengers = passengers
        self.pickup_1 = p1
        self.pickup_1_lat = None
        self.pickup_1_lng = None
        self.pickup_2 = p2
        self.pickup_2_lat = None
        self.pickup_2_lng = None
        self.pickup_3 = p3
        self.pickup_3_lat = None
        self.pickup_3_lng = None
        self.from_lat = None
        self.from_lng = None
        self.to_lat = None
        self.to_lng = None
        self.shortest_dist = 0
        self.closest_lat = self.from_lat
        self.closest_lng = self.from_lng

    def add_pickup(self, p, dist=0.0):
        if not self.closest_lat:
            self.closest_lat = self.from_lat
            self.closest_lng = self.from_lng
        if dist < self.shortest_dist:
            self.shortest_dist = dist
            self.closest_lat = p.latitude
            self.closest_lng = p.longitude
        if not self.pickup_1_lat:
            self.pickup_1_lat = p.latitude
            self.pickup_1_lng = p.longitude
        elif not self.pickup_2_lat:
            self.pickup_2_lat = p.latitude
            self.pickup_2_lng = p.longitude
        else:
            self.pickup_3_lat = p.latitude
            self.pickup_3_lng = p.longitude

    def get_id(self):
        return self.id

    def to_dict(self):
        if self.to_campus:
            from src.utils import campus_access
            c = campus_access.get_on_id(self.campus)
            alias_to = c.name
            # check if other is campus too
            alias_from = campus_access.get_name_if_exists(self.from_lat, self.from_lng)

        else:
            from src.utils import campus_access
            c = campus_access.get_on_id(self.campus)
            alias_from = c.name
            # other is not campus because else wouldn't be executed
            alias_to = ''

        return {
            'id': self.id,
            'departure_time': self.departure_time,
            'arrival_time': self.arrival_time,
            'lat_from': self.from_lat,
            'lng_from': self.from_lng,
            'alias_from': alias_from,
            'lat_to': self.to_lat,
            'lng_to': self.to_lng,
            'alias_to': alias_to,
            'pickup_1': self.pickup_1,
            'pickup_1_lat': self.pickup_1_lat,
            'pickup_1_lng': self.pickup_1_lng,
            'pickup_2': self.pickup_2,
            'pickup_2_lat': self.pickup_2_lat,
            'pickup_2_lng': self.pickup_2_lng,
            'pickup_3': self.pickup_3,
            'pickup_3_lat': self.pickup_3_lat,
            'pickup_3_lng': self.pickup_3_lng,
            'closest_lat': self.closest_lat,
            'closest_lng': self.closest_lng,
            'car_id': self.car_id,
            'passengers': self.passengers,
            'user_id': self.user_id
        }

class Rides:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, departure_time, arrival_time, user_id, address_1, campus, to_campus, car_id, passengers, pickup_point_1, pickup_point_2, pickup_point_3 FROM ride WHERE %s=%s",
            (on, val))
        rides = list()
        for row in cursor:
            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
            rides.append(ride)
        return rides

    def get_id_on_all(self, departure_time, arrival_time, user_id, address_1, campus):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id FROM ride WHERE departure_time=%s AND arrival_time=%s AND user_id=%s AND address_1=%s AND campus=%s",
            (departure_time, arrival_time, user_id, address_1, campus))
        row = cursor.fetchone()
        ride_id = row[0]
        return ride_id

    def get_on_id(self, id):
        found = self.get_on('id', id)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_user_id(self, user_id):
        found = self.get_on('user_id', user_id)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_car_id(self, car_id):
        found = self.get_on('car_id', car_id)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_departure_time(self, departure_time):
        found = self.get_on('departure_time', departure_time)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_arrival_time(self, arrival_time):
        found = self.get_on('arrival_time', arrival_time)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_address_1(self, address_1):
        found = self.get_on('address_1', address_1)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_campus(self, campus):
        found = self.get_on('campus', campus)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_all(self, dbconnect):
        cursor = dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, departure_time, arrival_time, user_id, address_1, campus, to_campus, car_id, passengers, pickup_point_1, pickup_point_2, pickup_point_3 FROM ride")
        rides = list()
        for row in cursor:
            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
            rides.append(ride)
        return rides

    def add_ride(self, ride):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "ride" VALUES(default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (ride.departure_time, ride.arrival_time, ride.user_id, ride.address_1, ride.campus,
                            ride.to_campus,
                            ride.car_id, ride.passengers, ride.pickup_1, ride.pickup_2, ride.pickup_3))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add ride')

    def match_rides_with_passenger(self, p_from, p_to, p_time_option, p_datetime):
        """
        Check if:
            1) driver destination is close enough to passenger destination
            2) driver departure/arrival time is close enough to passenger departure/arrival time
            3) driver departure is close enough to passenger departure, OR
            4) driver pickup point(s) are close enough to passenger departure

        :param p_from:
        :param p_to:
        :param p_time_option:
        :param p_datetime:
        :return:
        """

        # p_datetime = '2020-04-14 13:00'
        campus = 0

        from src.utils import campus_access
        if isinstance(p_from, int):  # p_from is campus
            campus = campus_access.get_on_id(p_from).to_dict()
            lat_from = campus['lat']
            lng_from = campus['lng']
            campus = 1
        else:
            lat_from = p_from['lat']
            lng_from = p_from['lng']
        if isinstance(p_to, int):  # p_to is campus
            campus = campus_access.get_on_id(p_to).to_dict()
            lat_to = campus['lat']
            lng_to = campus['lng']
            if campus == 0:
                campus = 2
        else:
            lat_to = p_to['lat']
            lng_to = p_to['lng']

        cursor = self.dbconnect.get_cursor()

        if p_time_option == 'Arrive by':
            p_time_option = 'r.arrival_time'
            print(p_time_option)
        else:
            p_time_option = 'r.departure_time'
        if campus == 1:  # riding FROM campus
            cursor.execute("""
                                    SELECT r.id, r.departure_time, r.arrival_time, r.user_id, r.address_1, r.campus, 
                                    r.to_campus, r.car_id, r.passengers, r.pickup_point_1, r.pickup_point_2, r.pickup_point_3,
                                    c.latitude, c.longitude, a.latitude, a.longitude
                                    FROM ride r join campus c on r.campus = c.id join address a on r.address_1 = a.id
                                    WHERE ((distance_difference(a.latitude, a.longitude, %s, %s) <= 3000) AND -- 1)
                                          (time_difference(%s, """ + p_time_option + """) between 0 and 600) AND -- 2)
                                          (
                                                       distance_difference(c.latitude, c.longitude, %s, %s) <= 3000 OR -- 3)
                                                      (
                                                      select count(p.id) from pickup_point p where p.id in (r.pickup_point_1, r.pickup_point_2, r.pickup_point_3)
                                                      and distance_difference(p.latitude, p.longitude, %s, %s) <= 3000
                                                      ) > 0

                                              ))""", (
                lat_to, lng_to, p_datetime, lat_from, lng_from, lat_from, lng_from))
        else:  # riding TO campus
            cursor.execute("""
                                    SELECT r.id, r.departure_time, r.arrival_time, r.user_id, r.address_1, r.campus, 
                                    r.to_campus, r.car_id, r.passengers, r.pickup_point_1, r.pickup_point_2, r.pickup_point_3,
                                    a.latitude, a.longitude, c.latitude, c.longitude
                                    FROM ride r join campus c on r.campus = c.id join address a on r.address_1 = a.id
                                    WHERE ((distance_difference(c.latitude, c.longitude, %s, %s) <= 3000) AND -- 1)
                                          (time_difference(%s, """ + p_time_option + """) BETWEEN 0 AND 600) AND -- 2)
                                          (
                                                       distance_difference(a.latitude, a.longitude, %s, %s) <= 3000 OR -- 3)
                                                      (
                                                      select count(p.id) from pickup_point p where p.id in (r.pickup_point_1, r.pickup_point_2, r.pickup_point_3)
                                                      and distance_difference(p.latitude, p.longitude, %s, %s) <= 3000
                                                      ) > 0

                                              ))""", (
                lat_to, lng_to, p_datetime, lat_from, lng_from, lat_from, lng_from))
        rides = list()
        for row in cursor:
            print(row)
            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
            ride.from_lat = row[12]
            ride.from_lng = row[13]
            ride.to_lat = row[14]
            ride.to_lng = row[15]

            from src.utils import pickup_point_access
            from math import atan2, sqrt, sin, radians, cos
            lat1 = lat_from
            lng1 = lng_from
            lat2 = ride.from_lat
            lng2 = ride.from_lng
            dist = 6371000 * (2 * atan2(sqrt(sin(radians(lat2 - lat1) / 2) * sin(radians(lat2 - lat1) / 2) +
                                             cos(radians(lat1)) * cos(radians(lat2)) * sin(radians(lng2 - lng1) / 2) *
                                             sin(radians(lng2 - lng1) / 2)), sqrt(1 -
                                                                                  (sin(radians(lat2 - lat1) / 2) * sin(
                                                                                      radians(lat2 - lat1) / 2) +
                                                                                   cos(radians(lat1)) * cos(
                                                                                              radians(lat2)) *
                                                                                   sin(radians(lng2 - lng1) / 2) *
                                                                                   sin(radians(lng2 - lng1) / 2)))))
            ride.shortest_dist = dist
            print(dist)

            for i in range(8, 11):
                print(row[i])
                if not row[i]:
                    break
                pp = pickup_point_access.get_on_id(row[i])
                print(pp.to_dict())
                lat1 = lat_from
                lng1 = lng_from
                lat2 = pp.latitude
                lng2 = pp.longitude
                dist = 6371000 * (2 * atan2(sqrt(sin(radians(lat2 - lat1) / 2) * sin(radians(lat2 - lat1) / 2) +
                                                 cos(radians(lat1)) * cos(radians(lat2)) * sin(
                    radians(lng2 - lng1) / 2) *
                                                 sin(radians(lng2 - lng1) / 2)), sqrt(1 -
                                                                                      (sin(radians(
                                                                                          lat2 - lat1) / 2) * sin(
                                                                                          radians(lat2 - lat1) / 2) +
                                                                                       cos(radians(lat1)) * cos(
                                                                                                  radians(lat2)) *
                                                                                       sin(radians(lng2 - lng1) / 2) *
                                                                                       sin(radians(lng2 - lng1) / 2)))))
                ride.add_pickup(pp, dist)
            rides.append(ride)
        return rides
