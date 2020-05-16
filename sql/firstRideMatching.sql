
/* start punt: Thomas More - Lesplaats Duffel (SNOR), coordinaten: 51.0953, 4.49607 */
insert into address  -- one address = id 1
values (default, 'Belgium', 'Antwerp', '2600', 'KwebbelStraat', '69', 51.0953, 4.49607);

insert into "user"  -- one user = id 1
values (default , 'Kabouter', 'Lui', 'lui@campuscarpool.com', 'password', '1999-04-04 01:12:11', 20, 'M', NULL, NULL, 1);

insert into "user"  -- one user = id 2
values (default , 'Kabouter', 'Plop', 'plop@campuscarpool.com', 'password', '1999-04-04 01:12:11', 20, 'M', NULL, NULL, 1);

insert into "user"  -- one user = id 3
values (default , 'Kabouter', 'Kwebbel', 'kwebbel@campuscarpool.com', 'password', '1999-04-04 01:12:11', 20, 'M', NULL, NULL, 1);

insert into "user"  -- one user = id 4
values (default , 'Kabouter', 'Smul', 'smul@campuscarpool.com', 'password', '1999-04-04 01:12:11', 20, 'M', NULL, NULL, 1);

insert into "user"  -- one user = id 5
values (default , 'Kabouter', 'Klus', 'klus@campuscarpool.com', 'password', '1999-04-04 01:12:11', 20, 'M', NULL, NULL, 1);

insert into "user"  -- one user = id 6
values (default , 'Kabouter', 'Smal', 'smal@campuscarpool.com', 'password', '1999-04-04 01:12:11', 20, 'M', NULL, NULL, 1);

insert into car  -- one car = id 1
values (default , '9999', 'Red', 'Toyota', 'asdf', 4, 1996, '4', 'ethanol', 1, NULL);

/* pickup 1 */
insert into pickup_point
values (default, 51.100562, 4.473305, '2020-04-14 13:03');

/* pickup 2 */
insert into pickup_point
values (default, 51.106853, 4.438677, '2020-04-14 13:05');

/* pickup 3 */
insert into pickup_point
values (default, 51.112011, 4.424566, '2020-04-14 13:08');

/* route 1:
        start punt: address 1
        eindpunt: UAntwerpen - Campus Middelheim (301)
 */
insert into ride
values (default , '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 4, 1, 2, 3, null, 301, 404, 301);

/* route 2:
        start punt: address 1
        eindpunt: UAntwerpen - Campus Groenenborger (300)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 3, 1, 2, 3, null, 300, 404, 300);

/* route 3:
        start punt: address 1
        eindpunt: Hoger Instituut voor Godsdienstwetenschappen (148)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 4, 1, 2, 3, null, 148, 404, 148);

/* route 4:
        start punt: address 1
        eindpunt: KdG Hogeschool - Campus Hoboken (248)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 5, 1, 2, 3, null, 248, 404, 248);

/* route 5:
        start punt: address 1
        eindpunt: APB - Campus Vesta (14)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 4, 1, 2, 3, null, 14, 404, 14);


insert into passenger_ride
values (2, 1);

insert into passenger_ride
values (3, 1);

insert into passenger_ride
values (2, 2);

insert into passenger_ride
values (3, 2);

insert into passenger_ride
values (6, 2);

insert into passenger_ride
values (5, 3);

insert into passenger_ride
values (6, 4);

insert into passenger_ride
values (3, 5);

insert into passenger_ride
values (5, 5);


/*
USAGE:
    - open kaart en zoek naar Duffel, waar startpunt Thomas More - Lesplaats Duffel (SNOR)
    - kies 1 van bovenstaande 5 campussen, of kies een punt op de kaart.
    - zet de tijd op 14 april 2020 13u00 (depart at) of 14u00 (arrive by)
    - verwachte resultaten:
        + UAntwerpen - Campus Middelheim (301) als eindpunt geeft 3 resultaten terug, campussen 301, 300 en 148
        + UAntwerpen - Campus Groenenborger (300) als eindpunt geeft 3 resultaten terug, campussen 301, 300 en 148
        + Hoger Instituut voor Godsdienstwetenschappen (148) als eindpunt geeft 3 resultaten terug, campussen 301, 300, 148 en 248
        + KdG Hogeschool - Campus Hoboken (248) als eindpunt geeft 2 resultaten terug, campussen 148 en 248
        + APB - Campus Vesta (14) ligt heel ver van de andere campussen verwijdert, dus 1 resultaat: campus zelf (14)
 */