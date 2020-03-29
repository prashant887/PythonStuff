from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class HelloWord(Resource):
    def __init__(self):
        pass

    def get(self):
        return {
            "Hello": "Word"
        }


data = []


class People(Resource):
    def __init__(self):
        pass

    def post(self, name):
        temp = {'data': name}
        data.append(temp)
        return temp

    def delete(self, name):
        for i,x in enumerate(data):
            if x['data']==name:
                data.pop(i)


    def get(self, name):
        for x in data:
            if x['data'] == name:
                return x
        return {'data': '404'}


api.add_resource(HelloWord, "/")
api.add_resource(People, '/people/<string:name>')
if __name__ == '__main__':
    app.run(debug=True)
