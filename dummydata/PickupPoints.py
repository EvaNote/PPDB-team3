file = open('pickup.txt', 'r')
output = open('pickup_output.txt', 'w')

line = file.readline()
while line:
    if line.startswith('<name>Naamloze kaart</name>') or line.startswith('<name>Naamloze laag</name>'):
        pass
    elif line.startswith('<name'):
        line = line.replace('<name>', '')
        line = line.replace('</name>', '')
        line = line.replace('\n', '#')
        output.write(line)
    elif line.startswith('<'):
        pass
    else:
        line = line.replace(',', '#')
        line = line.replace('#0', '')
        output.write(line)
    line = file.readline()

file.close()
output.close()

output_file = open('pickup_points.sql', 'w')
input_file = open('pickup_output.txt', 'r')
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
    end_of_line = line.find('\n')
    value2 = float(line[hashtag2 + 1:end_of_line])
    if value1 > 10.0:
        latitude = value1
        longitude = value2
    else:
        latitude = value2
        longitude = value1
    output_file.write('insert into pickup_point\nvalues (default, ' + str(latitude) + ', ' + str(longitude) + ');\n\n')
    line = input_file.readline()
input_file.close()
output_file.close()

# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="specify_your_app_name_here")
# location = geolocator.geocode("51.23037, 4.41603")
# print(location.latitude, location.longitude)
# print(location.raw)
