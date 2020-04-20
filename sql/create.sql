/*
Function for calculating distance difference (in metres) between two coordinates
 */
DROP FUNCTION IF EXISTS distance_difference;
CREATE FUNCTION distance_difference(lat1 float8, lng1 float8, lat2 float8, lng2 float8) RETURNS float8 AS
$$
BEGIN
    RETURN 6371000 * (2 * atan2(sqrt(sin(radians(lat2 - lat1) / 2) * sin(radians(lat2 - lat1) / 2) +
                                     cos(radians(lat1)) * cos(radians(lat2)) * sin(radians(lng2 - lng1) / 2) *
                                     sin(radians(lng2 - lng1) / 2)), sqrt(1 -
                                                                          (sin(radians(lat2 - lat1) / 2) * sin(radians(lat2 - lat1) / 2) +
                                                                           cos(radians(lat1)) * cos(radians(lat2)) *
                                                                           sin(radians(lng2 - lng1) / 2) *
                                                                           sin(radians(lng2 - lng1) / 2)))));
END;
$$
    LANGUAGE PLPGSQL;


/*
Function for calculating time difference (in seconds) between two timestamps
 */
DROP FUNCTION IF EXISTS time_difference;
CREATE FUNCTION time_difference(time1 timestamp, time2 timestamp) RETURNS integer AS
$$
BEGIN
     IF time2 is not null
     THEN
        RETURN EXTRACT(EPOCH FROM time1-time2);
     ELSE
        RETURN -1;
     END IF;
END;
$$
    LANGUAGE PLPGSQL;

/*
address table, doesn't need a "user" in case the address is
a destination. all fields are required
*/
DROP TABLE IF EXISTS address CASCADE;
CREATE TABLE address (
    id SERIAL PRIMARY KEY,
    country VARCHAR(256) NOT NULL,
    city VARCHAR(256) NOT NULL,
    postal_code VARCHAR(256) NOT NULL,
    street VARCHAR(256) NOT NULL,
    nr VARCHAR(256) NOT NULL,
    latitude float8 NOT NULL,
    longitude float8 NOT NULL
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
picture table for profile picture ("user") and picture of car
(not required for either -> doesn't go in "user"/car tables)
filename is path to file
*/
DROP TABLE IF EXISTS picture CASCADE;
CREATE TABLE picture (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(256) NOT NULL
);

/*
"user" table, last name & age are required
gender either M or F from gender_type
*/
DROP TABLE IF EXISTS "user" CASCADE;
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(256),
    last_name VARCHAR(256) NOT NULL,
    email VARCHAR(256) NOT NULL,
    password varchar not null,
    joined_on timestamp not null,
    age INTEGER,
    gender gender_type,
    phone_number VARCHAR(20),
    picture int REFERENCES picture(id),
    address int REFERENCES address(id)
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
    'LPG', /* = liquefied petroleum gas */
    'ethanol',
    'bio-diesel'
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
    brand VARCHAR(30) NOT NULL,
    model VARCHAR(256) NOT NULL,
    nr_seats INTEGER NOT NULL,
    construction_year INTEGER,
    fuel_consumption VARCHAR(30),
    fuel fuel_type,
    user_id int REFERENCES "user"(id) NOT NULL,
    picture int REFERENCES picture(id)
);

/*
ride table, belongs to a "user"
has a departure time (date + time) that's required
arrival time is not required
*/
DROP TABLE IF EXISTS ride CASCADE;
CREATE TABLE ride (
    id SERIAL PRIMARY KEY,
    departure_time timestamp NOT NULL,
    arrival_time timestamp NOT NULL,
    user_id int REFERENCES "user"(id) NOT NULL,
    address_1 int REFERENCES address(id) NOT NULL,
    campus int REFERENCES campus(id) NOT NULL,
    to_campus bool default true,
    car_id int REFERENCES car(id),
    passengers int NOT NULL,
    pickup_point_1 int REFERENCES pickup_point(id),
    pickup_point_2 int REFERENCES pickup_point(id),
    pickup_point_3 int REFERENCES pickup_point(id)
);
-- insert into ride
-- values (1, '2020-04-14 00:00', '2020-04-15 02:00', 1, 1, 1, 1);

/*
pickup point table keeps track of all the pickup points used in a ride.
*/
DROP TABLE IF EXISTS pickup_point CASCADE;
CREATE TABLE pickup_point (
    id SERIAL PRIMARY KEY,
    latitude float8 NOT NULL,
    longitude float8 NOT NULL,
    estimated_time timestamp NOT NULL
);

/*
review table for a review, is connected to 2 people: the writer and the reviewed person
also holds an amount of stars, the title of the review and the text
title and text can be empty, it's possible to only leave the star review
*/

DROP TABLE IF EXISTS review CASCADE;
CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    user_for int REFERENCES "user"(id) NOT NULL,
    user_from int REFERENCES "user"(id) NOT NULL,
    amount_of_stars INTEGER NOT NULL,
    title VARCHAR(256),
    review_text VARCHAR(1000),
    creation date default now()
);
