#!/bin/sh

psql -c 'CREATE DATABASE dbcarpool_test OWNER app;'

echo 'Voeg in /etc/postgresql/<version>/main/pg_hba.conf volgende lijn toe onder de dbcarpool lijn:'
echo 'local	dbcarpool_test	app					trust'

echo 'Hit enter when you are done to complete the script.'

read varname

sudo systemctl restart postgresql
psql dbcarpool_test -U app -f sql/create.sql
psql dbcarpool_test -U app -f sql/campussen.sql
psql dbcarpool_test -U app -f testdata/firstRideMatching.sql