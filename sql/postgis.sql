-- drop extension if exists postgis;
-- create extension postgis;
--
-- alter table address
-- add column coordinates geography(POINT);

-- update address
-- set coordinates = ST_MakePoint(longitude, latitude);

-- SELECT ST_AsText(address.coordinates), ST_X(address.coordinates::geometry), ST_Y(address.coordinates::geometry)
-- FROM address;

-- alter table pickup_point
-- add column coordinates geography(POINT);

-- update pickup_point
-- set coordinates = ST_MakePoint(longitude, latitude);

-- alter table campus
-- add column coordinates geography(POINT);

-- update campus
-- set coordinates = ST_MakePoint(longitude, latitude);