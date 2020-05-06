/* !!IMPORTANT!!
   Do not execute this file if the execution of postgis.sql isn't completed successfully. Executing this file while the
   tables aren't adjusted correctly will cause problems that can only be restored by recreation of the tables. This
   means data loss that could be avoided!
*/

/* Longitude and latitude of campus are no longer needed */
alter table campus
    drop column latitude;

alter table campus
    drop column longitude;

/* Longitude and latitude of pickup_point are no longer needed */
alter table pickup_point
    drop column latitude;

alter table pickup_point
    drop column longitude;

/* Longitude and latitude of address are no longer needed */
alter table address
    drop column latitude;

alter table address
    drop column longitude;

/* Address_1, campus and to_campus of ride are no longer needed, since campus_from, campus_to, address_from, address_to
   do the job right now. */
alter table ride
    drop column address_1;

alter table ride
    drop column campus;

alter table ride
    drop column to_campus;