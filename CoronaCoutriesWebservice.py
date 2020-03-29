import csv
from flask_restful import Api, Resource
from flask import Flask

app = Flask(__name__)
api = Api(app)

countries_dict = {}
countries_list = {}



class Corona(Resource):
    def __init__(self):
        self.countries_list={}

    def get(self, country):
        self.getData()
        return self.countries_list.get(country, 'Not Available')

    def getData(self):
        with open('C:\\Users\\Owner\\Documents\\datasets\\CoronaCases.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            for num, line in enumerate(csv_reader):
                if num == 0:
                    header = line
                else:
                    countries_dict = {}
                    for idx, data in enumerate(line):
                        countries_dict[header[idx]] = data
                    self.countries_list[line[0].lower()] = countries_dict


api.add_resource(Corona, '/corona/<string:country>')

if __name__ == '__main__':
    app.run()
