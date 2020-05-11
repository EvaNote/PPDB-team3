class Car:
    def __init__(self, id, number_plate, color, brand, model, nr_seats, construction_year, fuel_consumption, fuel,
                 user_id, picture):
        self.id = id
        self.number_plate = number_plate
        self.color = color
        self.brand = brand
        self.model = model
        self.nr_seats = nr_seats
        self.construction_year = construction_year
        self.fuel_consumption = fuel_consumption
        self.fuel = fuel
        self.user_id = user_id
        self.picture = picture

    def to_dict(self):
        return {'id': self.id, 'number_plate': self.number_plate, 'color': self.color, 'brand': self.brand,
                'model': self.model,
                'nr_seats': self.nr_seats, 'construction_year': self.construction_year,
                'fuel_consumption': self.fuel_consumption, 'fuel': self.fuel,
                'user_id': self.user_id, 'picture': self.picture}

class Cars:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,number_plate,color,brand,model,nr_seats,construction_year,fuel_consumption,fuel,"
                       "user_id,picture FROM car WHERE %s=%s",
                       (on, val))
        cars = list()
        for row in cursor:
            car = Car(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            cars.append(car)
        return cars

    def get_on_id(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT id,number_plate,color,brand,model,nr_seats,construction_year,fuel_consumption,fuel,'
                       'user_id,picture FROM car WHERE id=%s',
                       (id,))
        car = cursor.fetchone()
        if car == None:
            return None
        car_obj = Car(car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7], car[8], car[9], car[10])
        return car_obj

    def get_on_user_id(self, user_id):
        #found = self.get_on('user_id', user_id)
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,number_plate,color,brand,model,nr_seats,construction_year,fuel_consumption,fuel,"
                       "user_id,picture FROM car WHERE user_id=%s",
                       (user_id,))
        cars = list()
        for row in cursor:
            car = Car(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            cars.append(car)

        if len(cars) > 0:
            return cars
        else:
            return []

    def get_all(self, dbconnect):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id,number_plate,color,brand,model,nr_seats,construction_year,fuel_consumption,fuel,"
                       "user_id,picture FROM car")
        cars = list()
        for row in cursor:
            car = Car(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            cars.append(car)
        return cars

    def add_car(self, car):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "car" VALUES(default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (
                           car.number_plate,car.color,car.brand,car.model,car.nr_seats,car.construction_year,car.fuel_consumption,car.fuel,car.user_id,car.picture))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to add car')

    def edit_car(self, car_id, brand, model, color, plateNumber, seats, constructionYear, consumption, fuelType, picture):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE "car" SET brand=%s, model=%s, color=%s, number_plate=%s, nr_seats=%s, '
                           'construction_year=%s, fuel_consumption=%s, fuel=%s, picture=%s WHERE id=%s',
            (brand, model, color, plateNumber, seats, constructionYear, consumption, fuelType, picture, car_id))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to edit car')

    def delete_car(self, car_id):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM "car" WHERE id=%s',(car_id,))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to delete car')
