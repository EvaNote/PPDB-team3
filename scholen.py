class school:
    def __init__(self):
        self.__title = None
        self.__stad = None
        self.__postcode = None
        self.__straat = None
        self.__nummer = None


input_file = open('scholen.txt', 'r')
output_file = open('output.txt', 'w')

line = input_file.readline()
while line:
    # line.replace(' ', '')
    # line.replace('\t', '')
    line = "".join(line.split())
    line = "".join(line.split('&nbsp'))
    line = "".join(line.split(':'))
    line = "".join(line.split(';;'))
    line = "".join(line.split('<brclass=\"only-mobile\">'))
    line = "".join(line.split('</a><br>'))
    if line.startswith('<ahref=\"hoger_instellingen_detail.php'):
        i = 0
        while line[i] != '>':
            i += 1
        i += 1
        line = line[i:len(line)]
    if line.startswith('<divstyle'):
        pass
    elif line.startswith('<ahref=\"mailto'):
        pass
    elif line.startswith('<ahref=\"http'):
        pass
    elif line.startswith('0'):
        line = '#############'
    elif len(line) > 0:
        line += '\n'
        output_file.write(line)
    line = input_file.readline()

input_file.close()
output_file.close()
