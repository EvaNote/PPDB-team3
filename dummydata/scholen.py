output_file = open('toSql.sql', 'w')
output_file.write('drop table if exists campus;\n\n')
output_file.write('create table campus(\n')
output_file.write('\t id serial primary key,\n')
output_file.write('\t name varchar(255),\n')
output_file.write('\t category varchar(25),\n')
output_file.write('\t latitude float8,\n')
output_file.write('\t longitude float8\n')
output_file.write(');\n\n')

input_file = open('result.txt', 'r')
line = input_file.readline()
c = 0
name = ''
longitude = 0.0
latitude = 0.0
while line:
    hashtag1 = line.find('#')
    title = line[0:hashtag1]
    hashtag2 = line.find('#', hashtag1 + 1)
    value1 = float(line[hashtag1 + 1:hashtag2])
    hashtag3 = line.find('#', hashtag2 + 1)
    if hashtag3 != -1:
        category = 'university'
        value2 = float(line[hashtag2 + 1:hashtag3])
    else:
        category = 'college'
        end_of_line = line.find('\n')
        value2 = float(line[hashtag2 + 1:end_of_line])
    if value1 > 10.0:
        latitude = value1
        longitude = value2
    else:
        latitude = value2
        longitude = value1
    output_file.write('insert into campus\nvalues (default, \'' + str(title) + '\', \'' + str(category) + '\', ' + str(
        latitude) + ', ' + str(longitude) + ');\n\n')
    line = input_file.readline()
input_file.close()
output_file.close()

# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="specify_your_app_name_here")
# location = geolocator.geocode("51.23037, 4.41603")
# print(location.latitude, location.longitude)
# print(location.raw)
