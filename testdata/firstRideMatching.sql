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

DROP TABLE IF EXISTS ride CASCADE;
CREATE TABLE ride (
    id SERIAL PRIMARY KEY,
    departure_time timestamp NOT NULL,
    arrival_time timestamp NOT NULL,
    user_id int REFERENCES "user"(id) NOT NULL,
    address_1 int REFERENCES address(id) NOT NULL,
    campus int REFERENCES campus(id) NOT NULL,
    to_campus bool default true,
    car_id int REFERENCES car(id) NOT NULL,
    pickup_point_1 int REFERENCES pickup_point(id),
    pickup_point_2 int REFERENCES pickup_point(id),
    pickup_point_3 int REFERENCES pickup_point(id)
);

/* start punt: Thomas More - Lesplaats Duffel (SNOR), coordinaten: 51.0953, 4.49607 */
insert into address  -- one address = id 1
values (default, 'Belgium', 'Antwerp', '2600', 'KwebbelStraat', '69', 51.0953, 4.49607);

insert into "user"  -- one user = id 1
values (default , 'Kabouter', 'Lui', 'admin@blog.com', 'password', '1999-04-04 01:12:11', 20, 'M', NULL, NULL, 1);

insert into car  -- one car = id 1
values (default , '9999', 'Red', 'Toyota', 'asdf', 4, 1996, '4', 'ethanol', 1, NULL);

/* route 1:
        start punt: address 1
        eindpunt: UAntwerpen - Campus Middelheim (301)
 */
insert into ride
values (default , '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 301, true, 1, null, null, null);

/* route 2:
        start punt: address 1
        eindpunt: UAntwerpen - Campus Groenenborger (300)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 300, true, 1, null, null, null);

/* route 3:
        start punt: address 1
        eindpunt: Hoger Instituut voor Godsdienstwetenschappen (148)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 148, true, 1, null, null, null);

/* route 4:
        start punt: address 1
        eindpunt: KdG Hogeschool - Campus Hoboken (248)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 248, true, 1, null, null, null);

/* route 5:
        start punt: address 1
        eindpunt: APB - Campus Vesta (14)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 14, true, 1, null, null, null);

/*
USAGE:
    - open kaart en zoek naar Duffel, waar startpunt Thomas More - Lesplaats Duffel (SNOR)
    - kies 1 van bovenstaande 5 campussen, of kies een punt op de kaart.
    - verwachte resultaten:
        + UAntwerpen - Campus Middelheim (301) als eindpunt geeft 3 resultaten terug, campussen 301, 300 en 148
        + UAntwerpen - Campus Groenenborger (300) als eindpunt geeft 3 resultaten terug, campussen 301, 300 en 148
        + Hoger Instituut voor Godsdienstwetenschappen (148) als eindpunt geeft 3 resultaten terug, campussen 301, 300, 148 en 248
        + KdG Hogeschool - Campus Hoboken (248) als eindpunt geeft 2 resultaten terug, campussen 148 en 248
        + APB - Campus Vesta (14) ligt heel ver van de andere campussen verwijdert, dus 1 resultaat: campus zelf (14)
 */