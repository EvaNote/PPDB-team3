/*
type for fuel, 5 options (for now?)
*/
DROP TYPE IF EXISTS ride_role CASCADE;
CREATE TYPE ride_role AS ENUM (
    'driver',
    'passenger'
);


alter table review
add column author_role ride_role not null;