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
        self.pickup_2 = p2
        self.pickup_3 = p3

    def get_id(self):
        return self.id

    def to_dict(self):
        return {'id': self.id, 'departure_time': self.departure_time, 'arrival_time': self.arrival_time,
                'user_id': self.user_id, 'address_1': self.address_1, 'campus': self.campus,
                'to_campus': self.to_campus, 'car_id': self.car_id, 'passengers': self.passengers,
                'pickup_1': self.pickup_1, 'pickup_2': self.pickup_2, 'pickup_3': self.pickup_3}


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

    def get_on_address_to(self, address_to):
        found = self.get_on('address_to', address_to)
        if len(found) > 0:
            return found[0]
        else:
            return None

    def get_on_address_from(self, address_from):
        found = self.get_on('address_from', address_from)
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

    # def match_rides_with_passenger(self, p_from, p_to, p_time_option, p_datetime):
    #     """
    #     Check if:
    #         1) driver destination is close enough to passenger destination
    #         2) driver departure/arrival time is close enough to passenger departure/arrival time
    #         3) driver departure is close enough to passenger departure, OR
    #         4) driver pickup point(s) are close enough to passenger departure
    #
    #     :param p_from:
    #     :param p_to:
    #     :param p_time_option:
    #     :param p_datetime:
    #     :return:
    #     """
    #     cursor = self.dbconnect.get_cursor()
    #     if p_time_option == "Arrive by":
    #         cursor.execute("""
    #         SELECT r.id, r.departure_time, r.arrival_time, r.user_id, r.address_to, r.address_from, r.car_id
    #         FROM ride as r,
    #              pickup_point_ride as pr,
    #              address as dep, -- departure address
    #              address as dest -- destination address
    #         WHERE r.address_to = dest.id AND
    #               r.address_from = dep.id AND
    #               r.id = pr.ride_id AND
    #               distance_difference(dest.latitude, dest.longitude, %s, %s) <= 3000 AND -- 1)
    #               (time_difference(%s, r.arrival_time) BETWEEN 0 AND 6000) AND -- 2)
    #               (
    #                           distance_difference(dep.latitude, dep.longitude, %s, %s) <= 3000 OR -- 3)
    #                           EXISTS(
    #                                   FOR p2 IN (SELECT r.pickup_point_1 r.pickup_point_2 r.pickup_point_3  FROM r) LOOP
    #                                       IF p2 is not null
    #                                           SELECT *
    #                                           FROM p2
    #                                           WHERE distance_difference(p2.latitude, p2.longitude, %s, %s) <= 3000 -- 4)
    #                                       ENDIF;
    #                                   END LOOP;
    #                               )
    #                   )""", (
    #         p_from['lat'], p_from['lng'], p_datetime, p_to['lat'], p_to['lng'], p_from['lat'], p_from['lng']))
    #     else:
    #         cursor.execute("""
    #         SELECT r.id, r.departure_time, r.arrival_time, r.user_id, r.address_to, r.address_from, r.car_id
    #         FROM ride as r,
    #              pickup_point_ride as pr,
    #              address as dep, -- departure address
    #              address as dest -- destination address
    #         WHERE r.address_to = dest.id AND
    #               r.address_from = dep.id AND
    #               r.id = pr.ride_id AND
    #               distance_difference(dest.latitude, dest.longitude, %s, %s) <= 3000 AND -- 1)
    #               (time_difference(%s, r.departure_time) BETWEEN 0 AND 6000) AND -- 2)
    #               (
    #                           distance_difference(dep.latitude, dep.longitude, %s, %s) <= 3000 OR -- 3)
    #                           EXISTS(
    #                                 SELECT *
    #                                 FROM pickup_point as p2
    #                                 WHERE distance_difference(p2.latitude, p2.longitude, %s, %s) <= 3000 -- 4)
    #                               )
    #                   )""", (
    #         p_from['lat'], p_from['lng'], p_datetime, p_to['lat'], p_to['lng'], p_from['lat'], p_from['lng']))
    #     rides = list()
    #     for row in cursor:
    #         ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    #         rides.append(ride)
    #     return rides

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

        from src.utils import campus_access
        if isinstance(p_from, int):  # p_from is campus
            campus = campus_access.get_on_id(p_from).to_dict()
            lat_from = campus['lat']
            lng_from = campus['lng']
        else:
            lat_from = p_from['lat']
            lng_from = p_from['lng']
        if isinstance(p_to, int):  # p_to is campus
            campus = campus_access.get_on_id(p_to).to_dict()
            lat_to = campus['lat']
            lng_to = campus['lng']
        else:
            lat_to = p_to['lat']
            lng_to = p_to['lng']

        print('--' + str(lat_from))
        print('--' + str(lat_to))
        print('--' + str(lng_from))
        print('--' + str(lng_to))

        cursor = self.dbconnect.get_cursor()
        if p_time_option == "Arrive by":
            cursor.execute("""
                        SELECT r.id, r.departure_time, r.arrival_time, r.user_id, r.address_1, r.campus, r.car_id
                        FROM ride r join campus c on r.campus = c.id join address a on r.address_1 = a.id
                        WHERE distance_difference(c.latitude, c.longitude, %s, %s) <= 3000 AND -- 1)
                              (time_difference(%s, r.arrival_time) BETWEEN 0 AND 600) AND -- 2)
                              (
                                           distance_difference(a.latitude, a.longitude, %s, %s) <= 3000 OR -- 3)
                                          (
                                          select count(p.id) from pickup_point p where p.id in (r.pickup_point_1, r.pickup_point_2, r.pickup_point_3)
                                          and distance_difference(p.latitude, p.longitude, %s, %s) <= 3000
                                          ) > 0

                                  )""", (
                lat_from, lng_from, p_datetime, lat_to, lng_to, lat_from, lat_to))
        else:
            cursor.execute("""
                        SELECT r.id, r.departure_time, r.arrival_time, r.user_id, r.address_1, r.campus, r.car_id
                        FROM ride r join campus c on r.campus = c.id join address a on r.address_1 = a.id
                        WHERE distance_difference(c.latitude, c.longitude, %s, %s) <= 3000 AND -- 1)
                              (time_difference(%s, r.departure_time) BETWEEN 0 AND 600) AND -- 2)
                              (
                                           distance_difference(a.latitude, a.longitude, %s, %s) <= 3000 OR -- 3)
                                          (
                                          select count(p.id) from pickup_point p where p.id in (r.pickup_point_1, r.pickup_point_2, r.pickup_point_3)
                                          and distance_difference(p.latitude, p.longitude, %s, %s) <= 3000
                                          ) > 0

                      )""", (
                lat_from, lng_from, p_datetime, lat_to, lng_to, lat_from, lat_to))
        rides = list()
        for row in cursor:
            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            rides.append(ride)
        return rides
