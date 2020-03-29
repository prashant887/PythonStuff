import csv

countries_dict = {}
countries_list = []
with open('C:\\Users\\Owner\\Documents\\datasets\\CoronaCases.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    for num, line in enumerate(csv_reader):
        if num == 0:
            header = line
        else:
            countries_dict = {line[0]: {}}
            for idx, data in enumerate(line):
                countries_dict[line[0]][header[idx]] = data
            countries_list.append(countries_dict)

for values in countries_list:
    print(values)