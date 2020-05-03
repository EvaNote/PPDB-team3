from postgis import *
from postgis.psycopg import register
from shapely import geometry, wkb


class Ride:
    def __init__(self, id, departure_time, arrival_time, user_id, address_1, campus, to_campus, car_id, passengers, p1,
                 p2, p3, campus_from, campus_to, address_from, address_to):
        from src.utils import campus_access, address_access, pickup_point_access
        # address_to & address_from are id's pointing to addresses
        self.id = id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.user_id = user_id
        self.car_id = car_id
        self.passengers = passengers
        self.pickup_1 = pickup_point_access.get_on_id(p1)
        self.pickup_2 = pickup_point_access.get_on_id(p2)
        self.pickup_3 = pickup_point_access.get_on_id(p3)
        self.shortest_dist = 0
        self.closest = 0
        self.campus_from = campus_access.get_on_id(campus_from)
        if campus_from:
            self.address_from = self.campus_from.address
        else:
            self.address_from = address_access.get_on_id(address_from)
        self.campus_to = campus_access.get_on_id(campus_to)
        if campus_to:
            self.address_to = self.campus_to.address
        else:
            self.address_to = address_access.get_on_id(address_to)

    def get_id(self):
        return self.id

    def to_dict(self):
        way_points = dict()

        if self.campus_from:
            temp = self.address_from
            way_points[0] = {
                'addr': temp.addr_to_string(),
                'lat': temp.latitude,
                'lng': temp.longitude,
                'type': 'campus',
                'alias': self.campus_from.name,
            }
        else:
            temp = self.address_from
            way_points[0] = {
                'addr': temp.addr_to_string(),
                'lat': temp.latitude,
                'lng': temp.longitude,
                'type': 'address',
                'alias': ''
            }

        i = 1
        if self.pickup_1:
            temp = self.pickup_1.address
            way_points[i] = {
                'addr': temp.addr_to_string(),
                'lat': temp.latitude,
                'lng': temp.longitude,
                'type': 'pickup_point',
                'alias': 'pickup_1'
            }
            i += 1

        if self.pickup_2:
            temp = self.pickup_2.address
            way_points[i] = {
                'addr': temp.addr_to_string(),
                'lat': temp.latitude,
                'lng': temp.longitude,
                'type': 'pickup_point',
                'alias': 'pickup_2'
            }
            i += 1

        if self.pickup_3:
            temp = self.pickup_3.address
            way_points[i] = {
                'addr': temp.addr_to_string(),
                'lat': temp.latitude,
                'lng': temp.longitude,
                'type': 'pickup_point',
                'alias': 'pickup_3'
            }
            i += 1

        if self.campus_to:
            temp = self.address_to
            way_points[i] = {
                'addr': temp.addr_to_string(),
                'lat': temp.latitude,
                'lng': temp.longitude,
                'type': 'campus',
                'alias': self.campus_to.name,
            }
        else:
            temp = self.address_to
            way_points[i] = {
                'addr': temp.addr_to_string(),
                'lat': temp.latitude,
                'lng': temp.longitude,
                'type': 'address',
                'alias': ''
            }

        return {
            'id': self.id,
            'departure_time': self.departure_time,
            'arrival_time': self.arrival_time,
            'closest': self.closest,
            'len': i + 1,
            'car_id': self.car_id,
            'passengers': self.passengers,
            'user_id': self.user_id,
            'waypoints': way_points
        }


class Rides:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, "
            "departure_time, "
            "arrival_time, "
            "user_id, "
            "address_1, "
            "campus, "
            "to_campus, "
            "car_id, "
            "passengers, "
            "pickup_point_1, "
            "pickup_point_2, "
            "pickup_point_3, "
            "address_from, "
            "address_to, "
            "campus_from, "
            "campus_to "
            "FROM ride WHERE %s=%s",
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
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, "
            "departure_time, "
            "arrival_time, "
            "user_id, "
            "address_1, "
            "campus, "
            "to_campus, "
            "car_id, "
            "passengers, "
            "pickup_point_1, "
            "pickup_point_2, "
            "pickup_point_3, "
            "address_from, "
            "address_to, "
            "campus_from, "
            "campus_to "
            "FROM ride WHERE id=%s",
            (id,))
        ride = cursor.fetchone()
        if ride is None:
            return None
        ride_obj = Ride(ride[0], ride[1], ride[2], ride[3], ride[4], ride[5], ride[6], ride[7], ride[8], ride[9], ride[10], ride[11])
        return ride_obj

    def get_data_for_api(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            """
            SELECT car.nr_seats, a.longitude, a.latitude, c.longitude, c.latitude, r.arrival_time, r.to_campus
            FROM car, address as a, campus as c, ride as r
            WHERE r.id = %s AND
                  r.car_id = car.id AND
                  r.address_1 = a.id AND
                  r.campus = c.id
            """, (id,))
        result = {}
        temp = cursor.fetchone()
        if temp[6]:
            result = {"passenger-places": temp[0], "from": [temp[1], temp[2]], "to": [temp[3], temp[4]],
                      "arrival_time": temp[5]}
        else:
            result = {"passenger-places": temp[0], "from": [temp[3], temp[4]], "to": [temp[1], temp[2]],
                      "arrival_time": temp[5]}
        return result

    def get_passenger_ids(self, ride_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT p.user_id FROM passenger_ride as p WHERE p.ride_id = %s", (ride_id,))
        results = list()
        for row in cursor:
            results.append(row[0])
        return results

    def get_passenger_ids_names(self, ride_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            'SELECT p.user_id, u.email FROM passenger_ride p join "user" u on p.user_id = u.id  WHERE p.ride_id = %s',
            (ride_id,))
        results = list()
        for row in cursor:
            results.append({"id": row[0], "email": row[1]})
        return results

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

    def get_all(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id, "
            "departure_time, "
            "arrival_time, "
            "user_id, "
            "address_1, "
            "campus, "
            "to_campus, "
            "car_id, "
            "passengers, "
            "pickup_point_1, "
            "pickup_point_2, "
            "pickup_point_3, "
            "address_from, "
            "address_to, "
            "campus_from, "
            "campus_to "
            "FROM ride")
        rides = list()
        for row in cursor:
            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
            rides.append(ride)
        return rides

    def add_ride(self, ride):
        cursor = self.dbconnect.get_cursor()

        cursor.execute('INSERT INTO "ride" VALUES(default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (ride.departure_time, ride.arrival_time, ride.user_id, ride.address_1, ride.campus,
                            ride.to_campus,
                            ride.car_id, ride.passengers, ride.pickup_1, ride.pickup_2, ride.pickup_3))
        self.dbconnect.commit()

    def delete_ride(self, ride_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('DELETE FROM "ride" WHERE id=%s', (ride_id,))
        self.dbconnect.commit()

    def match_rides_with_passenger2(self, p_from, p_to, p_time_option, p_datetime, limit=20):
        from time import time
        start = time()
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

        from src.utils import campus_access

        if isinstance(p_from, int):
            p_from = campus_access.get_on_id(p_from).address.to_dict()
            from_loc = 'ST_MakePoint(' + str(p_from['lng']) + ', ' + str(p_from['lat']) + ')'
        else:
            from_loc = 'ST_MakePoint(' + str(p_from['lng']) + ', ' + str(p_from['lat']) + ')'
        if isinstance(p_to, int):
            p_to = campus_access.get_on_id(p_to).address.to_dict()
            to_loc = 'ST_MakePoint(' + str(p_to['lng']) + ', ' + str(p_to['lat']) + ')'
        else:
            to_loc = 'ST_MakePoint(' + str(p_to['lng']) + ', ' + str(p_to['lat']) + ')'

        try:
            p_time_value = "'" + p_datetime + "'"
        except Exception as e:
            p_time_value = ''
        if p_time_option == 'Arrive by':
            p_time_option = 'r.arrival_time'
            p_pickup_time_value = p_time_option
        else:
            p_time_option = 'r.departure_time'
            p_pickup_time_value = p_time_value
        if not p_datetime:
            p_datetime = p_time_option
            p_time_value = p_datetime
            p_pickup_time_value = p_time_option

        cursor = self.dbconnect.get_cursor()
        cursor.execute("""
            select r.id, r.departure_time, r.arrival_time, r.user_id, r.address_1, r.campus, r.to_campus, r.car_id, 
            r.passengers, r.pickup_point_1, r.pickup_point_2, r.pickup_point_3,
            campus_from, campus_to, address_from, address_to
            from ride r
            join address a_from on r.address_from = a_from.id
            join address a_to on r.address_to = a_to.id
            
            where (
                -- driver destination is close enough to passenger destination
                (ST_Distance(a_to.coordinates, """ + to_loc + """) < 3000)
                and
                -- driver departure/arrival time is close enough to passenger departure/arrival time    
                (time_difference(""" + p_time_value + """, """ + p_time_option + """) between 0 and 600)
                and
                (
                -- driver departure is close enough to passenger departure
                (ST_Distance(a_from.coordinates, """ + from_loc + """) < 3000)
                or
                -- driver pickup point(s) are close enough to passenger departure
                (select count(p.id)
                from pickup_point p
                where (
                (p.id in (r.pickup_point_1, r.pickup_point_2, r.pickup_point_3))
                and 
                (ST_Distance(p.coordinates, """ + from_loc + """) < 3000)
                and
                (time_difference(""" + p_pickup_time_value + """, """ + p_time_option + """) between 0 and 600)
                )
                ) > 0
                )
            )
            limit %s
        """, (limit,))


        rides = list()
        for row in cursor:
            # 0: r.id               5: r.campus         10: r.pickup_point_2    15: r.address_to
            # 1: r.departure_time   6: r.to_campus      11: r.pickup_point_3
            # 2: r.arrival_time     7: r.car_id         12: r.campus_from
            # 3: r.user_id          8: r.passengers     13: r.campus_to
            # 4: r.address_1        9: r.pickup_point_1 14: r.address_from

            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                        row[11], row[12], row[13], row[14], row[15])

            from src.utils import pickup_point_access, address_access
            print('1')
            dist = address_access.get_distance(p_from['lat'], p_from['lng'], row[14])
            print('2')
            shortest_dist = dist
            print('3')
            what = 0
            print('4')

            for i in range(9, 12):
                print('5')
                if not row[i]:
                    continue
                pp = pickup_point_access.get_on_id(row[i])
                dist = pickup_point_access.get_distance(p_from['lat'], p_from['lng'], pp.address.id)
                if dist < shortest_dist:
                    shortest_dist = dist
                    what = i - 8
            ride.shortest_dist = shortest_dist
            ride.closest = what
            rides.append(ride)
        stop = time()
        print('---------------------------------------------------------------------', stop - start)
        return rides

    def api_match_rides_with_passenger(self, p_from, p_to, p_time_option, p_datetime,
                                       limit=20):  # less information needed
        from time import time
        start = time()

        from_loc = 'ST_MakePoint(' + str(p_from['lng']) + ', ' + str(p_from['lat']) + ')'
        to_loc = 'ST_MakePoint(' + str(p_to['lng']) + ', ' + str(p_to['lat']) + ')'

        try:
            p_time_value = "'" + p_datetime + "'"
        except Exception as e:
            p_time_value = ''
        if p_time_option == 'Arrive by':
            p_time_option = 'r.arrival_time'
            p_pickup_time_value = p_time_option
        else:
            p_time_option = 'r.departure_time'
            p_pickup_time_value = p_time_value
        if not p_datetime:
            p_datetime = p_time_option
            p_time_value = p_datetime
            p_pickup_time_value = p_time_option

        cursor = self.dbconnect.get_cursor()
        cursor.execute("""
            select r.id, r.departure_time, r.arrival_time, r.user_id, r.passengers, r.address_from, r.address_to
            from ride r
            join address a_from on r.address_from = a_from.id
            join address a_to on r.address_to = a_to.id

            where (
                -- driver destination is close enough to passenger destination
                (ST_Distance(a_to.coordinates, """ + to_loc + """) < 3000)
                and
                -- driver departure/arrival time is close enough to passenger departure/arrival time    
                (time_difference(""" + p_time_value + """, """ + p_time_option + """) between 0 and 600)
                and
                (
                -- driver departure is close enough to passenger departure
                (ST_Distance(a_from.coordinates, """ + from_loc + """) < 3000)
                or
                -- driver pickup point(s) are close enough to passenger departure
                (select count(p.id)
                from pickup_point p
                where (
                (p.id in (r.pickup_point_1, r.pickup_point_2, r.pickup_point_3))
                and 
                (ST_Distance(p.coordinates, """ + from_loc + """) < 3000)
                and
                (time_difference(""" + p_pickup_time_value + """, """ + p_time_option + """) between 0 and 600)
                )
                ) > 0
                )
            )
            limit %s
        """, (limit,))

        rides = list()
        from src.utils import address_access, ride_access
        for row in cursor:
            ride = {
                'id': row[0],
                'driver-id': row[3],
                'passenger-ids': ride_access.findRidePassengers(row[0]),
                'passenger-places': row[4],
                'from': address_access.get_on_id(row[5]).lat_lng(),
                'to': address_access.get_on_id(row[6]).lat_lng(),
                'depart-at': row[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'arrive-by': row[2].strftime("%Y-%m-%dT%H:%M:%S")
            }
            rides.append(ride)
        stop = time()
        print('---------------------------------------------------------------------', stop - start)
        return rides

    def match_rides_with_passenger_missing_from(self, p_to, p_time_option, p_datetime, limit=20):
        from time import time
        start = time()

        from src.utils import campus_access

        to_loc = 'ST_MakePoint(' + str(p_to['lng']) + ', ' + str(p_to['lat']) + ')'

        try:
            p_time_value = "'" + p_datetime + "'"
        except Exception as e:
            p_time_value = ''
        if p_time_option == 'Arrive by':
            p_time_option = 'r.arrival_time'
        else:
            p_time_option = 'r.departure_time'
        if not p_datetime:
            p_time_value = p_time_option

        cursor = self.dbconnect.get_cursor()
        cursor.execute("""
                    select r.id, r.departure_time, r.arrival_time, r.user_id, r.passengers, address_from, address_to
                    from ride r
                    join address a_to on r.address_to = a_to.id

                    where (
                        -- driver destination is close enough to passenger destination
                        (ST_Distance(a_to.coordinates, """ + to_loc + """) < 3000)
                        and
                        -- driver departure/arrival time is close enough to passenger departure/arrival time    
                        (time_difference(""" + p_time_value + """, """ + p_time_option + """) between 0 and 600)
                    )
                    limit %s
                """, (limit,))

        rides = list()
        from src.utils import address_access, ride_access
        for row in cursor:
            ride = {
                'id': row[0],
                'driver-id': row[3],
                'passenger-ids': ride_access.findRidePassengers(row[0]),
                'passenger-places': row[4],
                'from': address_access.get_on_id(row[5]).lat_lng(),
                'to': address_access.get_on_id(row[6]).lat_lng(),
                'depart-at': row[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'arrive-by': row[2].strftime("%Y-%m-%dT%H:%M:%S")
            }
            rides.append(ride)
        stop = time()
        print('---------------------------------------------------------------------', stop - start)
        return rides

    def match_rides_with_passenger_missing_to(self, p_from, p_time_option, p_datetime, limit=20):
        from time import time
        start = time()

        from_loc = 'ST_MakePoint(' + str(p_from['lng']) + ', ' + str(p_from['lat']) + ')'

        try:
            p_time_value = "'" + p_datetime + "'"
        except Exception as e:
            p_time_value = ''
        if p_time_option == 'Arrive by':
            p_time_option = 'r.arrival_time'
            p_pickup_time_value = p_time_option
        else:
            p_time_option = 'r.departure_time'
            p_pickup_time_value = p_time_value
        if not p_datetime:
            p_datetime = p_time_option
            p_time_value = p_datetime
            p_pickup_time_value = p_time_option

        cursor = self.dbconnect.get_cursor()
        cursor.execute("""
                    select r.id, r.departure_time, r.arrival_time, r.user_id, r.passengers, r.address_from, r.address_to
                    from ride r
                    join address a_from on r.address_from = a_from.id

                    where (
                        -- driver departure/arrival time is close enough to passenger departure/arrival time    
                        (time_difference(""" + p_time_value + """, """ + p_time_option + """) between 0 and 600)
                        and
                        (
                        -- driver departure is close enough to passenger departure
                        (ST_Distance(a_from.coordinates, """ + from_loc + """) < 3000)
                        or
                        -- driver pickup point(s) are close enough to passenger departure
                        (select count(p.id)
                        from pickup_point p
                        where (
                        (p.id in (r.pickup_point_1, r.pickup_point_2, r.pickup_point_3))
                        and 
                        (ST_Distance(p.coordinates, """ + from_loc + """) < 3000)
                        and
                        (time_difference(""" + p_pickup_time_value + """, """ + p_time_option + """) between 0 and 600)
                        )
                        ) > 0
                        )
                    )
                    limit %s
                """, (limit,))

        rides = list()
        from src.utils import address_access, ride_access
        for row in cursor:
            ride = {
                'id': row[0],
                'driver-id': row[3],
                'passenger-ids': ride_access.findRidePassengers(row[0]),
                'passenger-places': row[4],
                'from': address_access.get_on_id(row[5]).lat_lng(),
                'to': address_access.get_on_id(row[6]).lat_lng(),
                'depart-at': row[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'arrive-by': row[2].strftime("%Y-%m-%dT%H:%M:%S"),
            }
            rides.append(ride)
        stop = time()
        print('---------------------------------------------------------------------', stop - start)
        return rides

    def match_rides_with_passenger_missing_end_points(self, p_time_option, p_datetime, limit=20):
        from time import time
        start = time()

        from src.utils import campus_access

        try:
            p_time_value = "'" + p_datetime + "'"
        except Exception as e:
            p_time_value = ''
        if p_time_option == 'Arrive by':
            p_time_option = 'r.arrival_time'
        else:
            p_time_option = 'r.departure_time'
        if not p_datetime:
            p_datetime = p_time_option
            p_time_value = p_datetime

        cursor = self.dbconnect.get_cursor()

        cursor.execute("""
                    select r.id, r.departure_time, r.arrival_time, r.user_id, r.passengers, address_from, address_to
                    from ride r
                    join address a_from on r.address_from = a_from.id
                    join address a_to on r.address_from = a_to.id

                    where (
                        -- driver departure/arrival time is close enough to passenger departure/arrival time    
                        (time_difference(""" + p_time_value + """, """ + p_time_option + """) between 0 and 600)
                    )
                    limit %s
                """, (limit,))

        rides = list()
        from src.utils import address_access, ride_access
        for row in cursor:
            ride = {
                'id': row[0],
                'driver-id': row[3],
                'passenger-ids': ride_access.findRidePassengers(row[0]),
                'passenger-places': row[4],
                'from': address_access.get_on_id(row[5]).lat_lng(),
                'to': address_access.get_on_id(row[6]).lat_lng(),
                'depart-at': row[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'arrive-by': row[2].strftime("%Y-%m-%dT%H:%M:%S")
            }
            rides.append(ride)
        stop = time()
        print('---------------------------------------------------------------------', stop - start)
        return rides


    def match_rides_with_passenger(self, p_from, p_to, p_time_option, p_datetime):
        from time import time
        start = time()
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
        campus = False

        from src.utils import campus_access
        if isinstance(p_from, int):  # p_from is campus
            campus = campus_access.get_on_id(p_from).to_dict()
            lat_from = campus['lat']
            lng_from = campus['lng']
            from_coords = 'c.latitude, c.longitude'
            campus = True
        elif p_from['lat']:
            lat_from = p_from['lat']
            lng_from = p_from['lng']
            from_coords = 'a.latitude, a.longitude'
            campus = True
        else:
            from_coords = None
        if isinstance(p_to, int):  # p_to is campus
            campus = campus_access.get_on_id(p_to).to_dict()
            lat_to = campus['lat']
            lng_to = campus['lng']
            if from_coords == 'c.latitude, c.longitude':
                to_coords = 'a.latitude, a.longitude'
            elif from_coords:
                to_coords = 'c.latitude, c.longitude'
            else:
                from_coords = 'a.latitude, a.longitude'
                lat_from = 'a.latitude'
                lng_from = 'a.longitude'
                to_coords = 'c.latitude, c.longitude'
        elif p_to['lat']:
            if not from_coords:
                from_coords = 'a.latitude, a.longitude'
                lat_from = 'a.latitude'
                lng_from = 'a.longitude'
            lat_to = p_to['lat']
            lng_to = p_to['lng']
            to_coords = 'c.latitude, c.longitude'
        else:
            if from_coords == 'c.latitude, c.longitude':
                to_coords = 'a.latitude, a.longitude'
                lat_to = 'a.latitude'
                lng_to = 'a.longitude'
            elif from_coords:
                to_coords = 'c.latitude, c.longitude'
                lat_to = 'c.latitude'
                lng_to = 'c.longitude'
            else:
                from_coords = 'a.latitude, a.longitude'
                to_coords = 'c.latitude, c.longitude'
                lat_from = 'a.latitude'
                lng_from = 'a.longitude'
                lat_to = 'c.latitude'
                lng_to = 'c.longitude'

        cursor = self.dbconnect.get_cursor()

        if p_time_option == 'Arrive by':
            p_time_option = 'r.arrival_time'
            pickup_time_check = False
        else:
            p_time_option = 'r.departure_time'
            pickup_time_check = True

        if not p_from:
            p_from = from_coords
        else:
            p_from = str(lat_from) + ',' + str(lng_from)  # latitude, longitude
        if not p_to:
            p_to = to_coords
        else:
            p_to = str(lat_to) + ',' + str(lng_to)  # latitude, longitude
        if not p_time_option:
            p_time_value = p_time_option
        elif not p_datetime:
            p_time_value = p_time_option
        else:
            p_time_value = "'" + p_datetime + "'"

        cursor.execute("""
                        SELECT r.id, r.departure_time, r.arrival_time, r.user_id, r.address_1, r.campus, 
                        r.to_campus, r.car_id, r.passengers, r.pickup_point_1, r.pickup_point_2, r.pickup_point_3,
                        a.latitude, a.longitude, c.latitude, c.longitude
                        FROM ride r join campus c on r.campus = c.id join address a on r.address_1 = a.id
                        WHERE ((distance_difference(c.latitude, c.longitude, """ + p_to + """) <= 3000) AND -- 1)
                              (time_difference(""" + p_time_value + """, """ + p_time_option + """) BETWEEN 0 AND 600) AND -- 2)
                              (
                                           distance_difference(a.latitude, a.longitude, """ + p_from + """) <= 3000 OR -- 3)
                                          (
                                          select count(p.id) from pickup_point p where p.id in (r.pickup_point_1, r.pickup_point_2, r.pickup_point_3)
                                          and distance_difference(p.latitude, p.longitude, """ + p_from + """) <= 3000
                                          and (((time_difference(""" + p_time_value + """, p.estimated_time) between 0 and 600) and %s = true)
                                            or (%s = false))
                                          ) > 0

                                  ) and r.to_campus)
                                  or
                                  ((distance_difference(a.latitude, a.longitude, """ + p_to + """) <= 3000) AND -- 1)
                                  (time_difference(""" + p_time_value + """, """ + p_time_option + """) BETWEEN 0 AND 600) AND -- 2)
                                  (
                                               distance_difference(c.latitude, c.longitude, """ + p_from + """) <= 3000 OR -- 3)
                                              (
                                              select count(p.id) from pickup_point p where p.id in (r.pickup_point_1, r.pickup_point_2, r.pickup_point_3)
                                              and distance_difference(p.latitude, p.longitude, """ + p_from + """) <= 3000
                                              and (((time_difference(""" + p_time_value + """, p.estimated_time) between 0 and 600) and %s = true)
                                                or (%s = false))
                                              ) > 0
    
                                ) and not r.to_campus)
                                  """, (pickup_time_check, pickup_time_check, pickup_time_check, pickup_time_check))

        rides = list()
        for row in cursor:
            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
            ride.from_lat = row[12]
            ride.from_lng = row[13]
            ride.to_lat = row[14]
            ride.to_lng = row[15]

            ride.string_addr_from = self.__helper_function_get_address(row[12], row[13])
            ride.string_addr_to = self.__helper_function_get_address(row[14], row[15])

            from src.utils import pickup_point_access
            lat1 = lat_from
            lng1 = lng_from
            lat2 = ride.from_lat
            lng2 = ride.from_lng
            dist = self.__helper_function_dist(lat1, lng1, lat2, lng2)
            ride.shortest_dist = dist

            for i in range(9, 12):
                if not row[i]:
                    break
                pp = pickup_point_access.get_on_id(row[i])
                lat1 = lat_from
                lng1 = lng_from
                lat2 = pp.latitude
                lng2 = pp.longitude
                dist = self.__helper_function_dist(lat1, lng1, lat2, lng2)
                addr = self.__helper_function_get_address(lat2, lng2)
                ride.add_pickup(pp, dist, addr)
            rides.append(ride)

        stop = time()
        print('---------------------------------------------------------------------', stop - start)
        return rides

    def __helper_function_dist(self, lat1, lng1, lat2, lng2):
        if not isinstance(lat1, float) or not isinstance(lng1, float) or not isinstance(lat2, float) or not isinstance(
                lng2, float):
            return 0.0

        from src.utils import pickup_point_access
        from math import atan2, sqrt, sin, radians, cos
        return 6371000 * (2 * atan2(sqrt(sin(radians(lat2 - lat1) / 2) * sin(radians(lat2 - lat1) / 2) +
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

    def __helper_function_get_address(self, lat, lng):
        # straat, huisnr, postocde, stad
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="campus_carpool")
        location = geolocator.reverse(str(lat) + ', ' + str(lng), True, timeout=300)
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
        return road + ' ' + str(housenr) + ', ' + str(postcode) + ' ' + town

    def checkPassengerRegistered(self, p_id, r_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("select count(*) from passenger_ride WHERE passenger_ride.ride_id=%s AND passenger_ride.user_id=%s", (r_id, p_id))
        result = cursor.fetchone()
        if result[0] == 0:
            return False
        return True

    def registerPassenger(self, p_id, r_id):
        if not self.checkPassengerRegistered(p_id, r_id):
            cursor = self.dbconnect.get_cursor()
            cursor.execute("insert into passenger_ride VALUES (%s, %s)", (p_id, r_id))
            self.dbconnect.commit()
            return True
        return False

    def findRidePassengers(self, r_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("select user_id from passenger_ride where passenger_ride.ride_id=%s", (r_id,))
        passengers = list()
        for passenger in cursor:
            passengers.append(passenger[0])
        return passengers

    def getRidesFromPassenger(self, p_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT ride_id FROM passenger_ride WHERE user_id=%s", (p_id,))
        rides = []
        for row in cursor:
            ride_id = row[0]
            ride = self.get_on_id(ride_id)
            rides.append(ride)
        return rides

    def deletePassenger(self, p_id, r_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('DELETE FROM passenger_ride WHERE user_id=%s AND ride_id=%s', (p_id,r_id))
        self.dbconnect.commit()

    def deleteFromPassengerRide(self, r_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('DELETE FROM passenger_ride WHERE ride_id=%s', (r_id,))
        self.dbconnect.commit()

    # #TODO: bij users aanpassen
    # def delete_ride(self, ride_id):
    #     cursor = self.dbconnect.get_cursor()
    #     try:
    #         cursor.execute('DELETE FROM "ride" WHERE id=%s',(ride_id,))
    #         self.dbconnect.commit()
    #     except:
    #         raise Exception('Unable to delete ride')
    #
    # #TODO: meer bewerken
    # def edit_ride(self, ride_id, departure_time,  ):
    #     cursor = self.dbconnect.get_cursor()
    #     ride = self.get_on_id(ride_id)
    #     #user_id = user.id
    #
    #     try:
    #         cursor.execute('UPDATE "ride" SET departure_time=%s,  WHERE id=%s',
    #         (departure_time,ride_id))
    #         self.dbconnect.commit()
    #     except:
    #         raise Exception('Unable to edit user')
