from postgis import *
from postgis.psycopg import register
from shapely import geometry, wkb
import requests


class Ride:
    def __init__(self, id, departure_time, arrival_time, user_id, passengers, p1,
                 p2, p3, campus_from, campus_to, address_from, address_to):
        from src.utils import campus_access, address_access, pickup_point_access
        # address_to & address_from are id's pointing to addresses
        self.id = id
        self.dont_store_in_db = False
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.user_id = user_id
        self.passengers = passengers
        self.pickup_1 = pickup_point_access.get_on_id(p1)
        self.pickup_2 = pickup_point_access.get_on_id(p2)
        self.pickup_3 = pickup_point_access.get_on_id(p3)
        self.shortest_dist = 0
        self.closest = 0
        self.campus_from = campus_access.get_on_id(campus_from)
        from src.dbmodels.Address import Address
        if campus_from:
            self.address_from = self.campus_from.address
        else:
            if isinstance(address_from, Address):
                self.address_from = address_from
            else:
                self.address_from = address_access.get_on_id(address_from)
        self.campus_to = campus_access.get_on_id(campus_to)
        if campus_to:
            self.address_to = self.campus_to.address
        else:
            if isinstance(address_to, Address):
                self.address_to = address_to
            else:
                self.address_to = address_access.get_on_id(address_to)
        if self.dont_store_in_db:
            self.address_from.dont_store_in_db = True
            self.address_to.dont_store_in_db = True

    def get_id(self):
        return self.id

    def campus_from_id(self):
        if self.campus_from:
            return self.campus_from.id
        else:
            return None

    def campus_to_id(self):
        if self.campus_to:
            return self.campus_to.id
        else:
            return None

    def pickup_id(self, num):
        if num == 1 and self.pickup_1 is not None:
            return self.pickup_1.id
        elif num == 2 and self.pickup_2 is not None:
            return self.pickup_2.id
        elif self.pickup_3 is not None:
            return self.pickup_3.id

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
            'passengers': self.passengers,
            'user_id': self.user_id,
            'waypoints': way_points
        }

    def fetch_id(self):
        if self.id is not None:
            return self.id
        else:
            from src.utils import ride_access
            self.id = ride_access.get_id_on_all(self.departure_time, self.arrival_time, self.user_id, self.address_from,
                                            self.address_to)
            return self.id


class Rides:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT "
            "id, "  # 0
            "departure_time, "  # 1
            "arrival_time, "  # 2
            "user_id, "  # 3
            "passengers, "  # 4
            "pickup_point_1, "  # 5
            "pickup_point_2, "  # 6
            "pickup_point_3, "  # 7
            "campus_from, "  # 8
            "campus_to, "  # 9
            "address_from, "  # 10
            "address_to "  # 11
            "FROM ride WHERE " + on + "=%s",
            (val,))
        rides = list()
        for row in cursor:
            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                        row[11])
            rides.append(ride)
        return rides

    def get_id_on_all(self, departure_time, arrival_time, user_id, address_from, address_to):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id FROM ride WHERE departure_time=%s AND arrival_time=%s AND user_id=%s AND address_from=%s "
            "AND address_to=%s",
            (departure_time, arrival_time, user_id, address_from.id, address_to.id))
        row = cursor.fetchone()
        ride_id = row[0]
        return ride_id

    def get_on_id(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT "
            "id, "  # 0
            "departure_time, "  # 1
            "arrival_time, "  # 2
            "user_id, "  # 3
            "passengers, "  # 4
            "pickup_point_1, "  # 5
            "pickup_point_2, "  # 6
            "pickup_point_3, "  # 7
            "campus_from, "  # 8
            "campus_to, "  # 9
            "address_from, "  # 10
            "address_to "  # 11
            "FROM ride WHERE id=%s",
            (id,))
        ride = cursor.fetchone()
        if ride is None:
            return None
        ride_obj = Ride(ride[0], ride[1], ride[2], ride[3], ride[4], ride[5], ride[6], ride[7], ride[8], ride[9],
                        ride[10], ride[11])
        return ride_obj

    def get_data_for_api(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            """
            SELECT a_from.id, a_to.id, r.arrival_time
            FROM address as a_from, address as a_to, ride as r
            WHERE r.id = %s AND
                  r.address_from = a_from.id AND
                  r.address_to = a_to.id
            """, (id,))
        temp = cursor.fetchone()
        from src.utils import address_access
        return {"passenger-places": temp[0],
                "from": address_access.get_on_id(temp[1]).lat_lng(),
                "to": address_access.get_on_id(temp[2]).lat_lng(),
                "arrival_time": temp[3]}

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
            results.append(
                {"id": row[0],
                 "email": row[1]})
        return results

    def get_on_user_id(self, user_id):
        found = self.get_on('user_id', user_id)
        if len(found) > 0:
            return found
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

    def get_all(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT "
            "id, "  # 0
            "departure_time, "  # 1
            "arrival_time, "  # 2
            "user_id, "  # 3
            "passengers, "  # 4
            "pickup_point_1, "  # 5
            "pickup_point_2, "  # 6
            "pickup_point_3, "  # 7
            "campus_from, "  # 8
            "campus_to, "  # 9
            "address_from, "  # 10
            "address_to "  # 11
            "FROM ride")
        rides = list()
        for row in cursor:
            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                        row[11])
            rides.append(ride)
        return rides

    def add_ride(self, ride: Ride):
        if ride.dont_store_in_db:
            return
        cursor = self.dbconnect.get_cursor()

        print(ride.departure_time, ride.arrival_time)

        cursor.execute('INSERT INTO "ride" VALUES(default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (ride.departure_time, ride.arrival_time, ride.user_id, ride.passengers,
                        ride.pickup_id(1), ride.pickup_id(2), ride.pickup_id(3), ride.campus_from_id(), ride.campus_to_id(),
                        ride.address_from.id, ride.address_to.id))
        self.dbconnect.commit()

    def delete_ride(self, ride_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('DELETE FROM "ride" WHERE id=%s', (ride_id,))
        self.dbconnect.commit()

    def match_rides_with_passenger(self, p_from, p_to, p_time_option, p_datetime, limit=20):
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

        url = 'http://team1.ppdb.me/api/drives/search?'
        from_formatted = 'from={}%2C%20{}'.format(p_from['lat'], p_from['lng'])
        to_formatted = 'to={}%2C%20{}'.format(p_to['lat'], p_to['lng'])
        if p_time_option == 'r.departure_time':
            time = 'depart_by=' + str(p_datetime.replace(' ', 'T'))
        else:
            time = 'arrive_by=' + str(p_datetime.replace(' ', 'T'))

        url += from_formatted + '&' + to_formatted + '&' + time + '&' \
               + 'from_distance=3000&to_distance=3000&departure_delta=10&arrival_delta=10'


        # url = 'http://team1.ppdb.me/api/drives/search?'
        

        print(url)
        r = requests.get(url)
        data = r.json()
        print(data)

        partner_rides = list()
        from src.utils import campus_access, address_access
        from src.dbmodels.Address import Address
        for ride in data:
            print(ride)
            campus_from = campus_access.is_campus(ride['from'][0], ride['from'][1])
            campus_to = campus_access.is_campus(ride['to'][0], ride['to'][1])
            address_from = Address(None, None, None, None, None, None, None, ride['from'][0], ride['from'][1])
            address_to = Address(None, None, None, None, None, None, None, ride['to'][0], ride['to'][1])
            ride = Ride(ride['id'], None, ride['arrive-by'], None, None, None, None, None, campus_from,
                                      campus_to, address_from, address_to)
            ride.dont_store_in_db = True
            partner_rides.append(ride.to_dict())

        cursor = self.dbconnect.get_cursor()
        cursor.execute("""
            SELECT 
            r.id,   
            departure_time,  
            arrival_time,  
            user_id,   
            passengers,  
            pickup_point_1,  
            pickup_point_2,   
            pickup_point_3,   
            campus_from,   
            campus_to,   
            address_from,   
            address_to   
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
            # 0: r.id               5: r.pickup_point_1     10: r.address_from
            # 1: r.departure_time   6: r.pickup_point_2     11: r.address_to
            # 2: r.arrival_time     7: r.pickup_point_3
            # 3: r.user_id          8: r.campus_from
            # 4: r.passengers       9: r.campus_to

            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                        row[11])

            from src.utils import pickup_point_access, address_access
            dist = address_access.get_distance(p_from['lat'], p_from['lng'], row[11])
            shortest_dist = dist
            what = 0

            for i in range(5, 8):
                if not row[i]:
                    continue
                pp = pickup_point_access.get_on_id(row[i])
                dist = pickup_point_access.get_distance(p_from['lat'], p_from['lng'], pp.address.id)
                if dist < shortest_dist:
                    shortest_dist = dist
                    what = i - 5
            ride.shortest_dist = shortest_dist
            ride.closest = what
            rides.append(ride)
        return rides, partner_rides

    def api_match_rides_with_passenger(self, p_from, p_to, p_time_option, p_datetime, limit=20):
        # less information needed
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
                'passenger-ids': ride_access.find_ride_passengers(row[0]),
                'passenger-places': row[4],
                'from': address_access.get_on_id(row[5]).lat_lng(),
                'to': address_access.get_on_id(row[6]).lat_lng(),
                'depart-at': row[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'arrive-by': row[2].strftime("%Y-%m-%dT%H:%M:%S")
            }
            rides.append(ride)
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
                'passenger-ids': ride_access.find_ride_passengers(row[0]),
                'passenger-places': row[4],
                'from': address_access.get_on_id(row[5]).lat_lng(),
                'to': address_access.get_on_id(row[6]).lat_lng(),
                'depart-at': row[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'arrive-by': row[2].strftime("%Y-%m-%dT%H:%M:%S")
            }
            rides.append(ride)
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
                'passenger-ids': ride_access.find_ride_passengers(row[0]),
                'passenger-places': row[4],
                'from': address_access.get_on_id(row[5]).lat_lng(),
                'to': address_access.get_on_id(row[6]).lat_lng(),
                'depart-at': row[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'arrive-by': row[2].strftime("%Y-%m-%dT%H:%M:%S"),
            }
            rides.append(ride)
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
                'passenger-ids': ride_access.find_ride_passengers(row[0]),
                'passenger-places': row[4],
                'from': address_access.get_on_id(row[5]).lat_lng(),
                'to': address_access.get_on_id(row[6]).lat_lng(),
                'depart-at': row[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'arrive-by': row[2].strftime("%Y-%m-%dT%H:%M:%S")
            }
            rides.append(ride)
        return rides

    def check_passenger_registered(self, p_id, r_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "select count(*) from passenger_ride WHERE passenger_ride.ride_id=%s AND passenger_ride.user_id=%s",
            (r_id, p_id))
        result = cursor.fetchone()
        if result[0] == 0:
            return False
        return True

    def check_amount_passengers(self, r_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("select count(*) from passenger_ride WHERE passenger_ride.ride_id=%s", (r_id,))
        result = cursor.fetchone()
        return result[0]

    def register_passenger(self, p_id, r_id):
        if not self.check_passenger_registered(p_id, r_id):
            cursor = self.dbconnect.get_cursor()
            cursor.execute("insert into passenger_ride VALUES (%s, %s)", (p_id, r_id))
            self.dbconnect.commit()
            return True
        return False

    def find_ride_passengers(self, r_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("select user_id from passenger_ride where passenger_ride.ride_id=%s", (r_id,))
        passengers = list()
        for passenger in cursor:
            passengers.append(passenger[0])
        return passengers

    def get_rides_from_passenger(self, p_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT ride_id FROM passenger_ride WHERE user_id=%s", (p_id,))
        rides = []
        for row in cursor:
            ride_id = row[0]
            ride = self.get_on_id(ride_id)
            rides.append(ride)
        return rides

    def delete_passenger(self, p_id, r_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('DELETE FROM passenger_ride WHERE user_id=%s AND ride_id=%s', (p_id, r_id))
        self.dbconnect.commit()

    def delete_all_passenger_rides(self, p_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('DELETE FROM passenger_ride WHERE user_id=%s', (p_id,))
        self.dbconnect.commit()

    def delete_from_passenger_ride(self, r_id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('DELETE FROM passenger_ride WHERE ride_id=%s', (r_id,))
        self.dbconnect.commit()

