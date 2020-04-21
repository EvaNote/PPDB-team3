# DROP TABLE IF EXISTS "user" CASCADE;
# CREATE TABLE "user" (
#     id SERIAL PRIMARY KEY,
#     first_name VARCHAR(256),
#     last_name VARCHAR(256) NOT NULL,
#     email VARCHAR(256) NOT NULL,
#     password varchar not null,
#     joined_on timestamp not null,
#     age INTEGER,
#     gender gender_type,
#     phone_number VARCHAR(20),
#     picture int REFERENCES picture(id),
#     address int REFERENCES address(id)
# );


# generate 100 users
file = open('names.txt', 'r')
output = open('names2.txt')
line = file.readline()
while line:
    line_arr = line.split()
    username = line_arr[0].lower() + '@campuscarpool.com'
    line = line_arr[0] + ' ' + line_arr[1] + ' ' + username + '\n'
    line = file.readline()
output.close()
file.close()
