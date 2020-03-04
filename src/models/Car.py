class Car:
    def __init__(self, id, number_plate, color, brand, model, nr_seats, construction_year, fuel_consumption, fuel, user_id, picture):
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

    def get(cursor, id):
        cursor.execute("SELECT number_plate,color,brand,model,nr_seats,construction_year,fuel_consumption,fuel,user_id,picture FROM car WHERE id = %s", (id,))
        number_plate,color,brand,model,nr_seats,construction_year,fuel_consumption,fuel,user_id,picture = cursor.fetchone()
        return Car(number_plate,color,brand,model,nr_seats,construction_year,fuel_consumption,fuel,user_id,picture)

    def to_dict(self):
        return {'id': self.id, 'number_plate': self.number_plate, 'color': self.color, 'brand': self.brand, 'model': self.model,
        'nr_seats': self.nr_seats, 'construction_year': self.construction_year, 'fuel_consumption': self.fuel_consumption, 'fuel': self.fuel,
        'user_id': self.user_id, 'picture': self.picture}
