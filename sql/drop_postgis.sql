alter table campus
    drop column latitude;

alter table campus
    drop column longitude;

alter table pickup_point
    drop column latitude;

alter table pickup_point
    drop column longitude;

alter table address
    drop column latitude;

alter table address
    drop column longitude;

alter table ride
    drop column address_1;

alter table ride
    drop column campus;

alter table ride
    drop column to_campus;