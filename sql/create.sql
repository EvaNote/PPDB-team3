/*
address table, doesn't need a user in case the address is
a destination. all fields are required
*/
DROP TABLE IF EXISTS address CASCADE;
CREATE TABLE address (
    id SERIAL PRIMARY KEY,
    country VARCHAR(256) NOT NULL,
    city VARCHAR(256) NOT NULL,
    postal_code INTEGER NOT NULL,
    street VARCHAR(256) NOT NULL,
    nr VARCHAR(256) NOT NULL
);

/*
type for gender, 2 options
*/
DROP TYPE IF EXISTS gender_type CASCADE;
CREATE TYPE gender_type AS ENUM (
    'M',
    'F'
);

/*
user table, last name & age are required
gender either M or F from gender_type
*/
DROP TABLE IF EXISTS user CASCADE;
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(256) NOT NULL,
    first_name VARCHAR(256),
    last_name VARCHAR(256) NOT NULL,
    age INTEGER NOT NULL,
    gender gender_type NOT NULL,
    active_since DATE,
    picture REFERENCES picture(id),
    address REFERENCES address(id)
);

/*
type for fuel, 5 options (for now?)
*/
DROP TYPE IF EXISTS fuel_type CASCADE;
CREATE TYPE fuel_type AS ENUM (
    'benzine', /* = gasoline = petrol */
    'diesel',
    'electricity',
    'CNG', /* = compressed natural gas */
    'LPG' /* = liquefied petroleum gas */
);

/*
car table, color/brand/model is optional
optional picture
fuel from 5 fuel options (fuel_type)
*/
DROP TABLE IF EXISTS car CASCADE;
CREATE TABLE car (
    id SERIAL PRIMARY KEY,
    number_plate VARCHAR(10) NOT NULL,
    color VARCHAR(30),
    brand VARCHAR(30),
    model VARCHAR(256),
    nr_seats INTEGER NOT NULL,
    construction_year INTEGER,
    fuel_consumption INTEGER,
    fuel fuel_type,
    user_id REFERENCES user(id) NOT NULL,
    picture REFERENCES picture(id)
);

/*
ride table, belongs to a user
has a departure time (date + time) that's required
arrival time is not required
*/
DROP TABLE IF EXISTS ride CASCADE;
CREATE TABLE ride (
    id SERIAL PRIMARY KEY,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME,
    user_id REFERENCES user(id) NOT NULL,
    address_to REFERENCES address(id) NOT NULL,
    address_from REFERENCES address(id) NOT NULL,
    car_id REFERENCES car(id) NOT NULL
);

/*
picture table for profile picture (user) and picture of car
(not required for either -> doesn't go in user/car tables)
filename is path to file
*/
DROP TABLE IF EXISTS picture CASCADE;
CREATE TABLE picture (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(256) NOT NULL
);
