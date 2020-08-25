from flask import Flask, jsonify, request
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)
todo = {}


@api.route('/welcome')
class WelcomPage(Resource):
    def get(self):
        return 'Hello SiteMonV2 Lambda is ready'


@api.route('/<string:task>')
class SimpleTask(Resource):
    def get(self, task):
        return {task: todo[task]}

    def put(self, task):
        todo[task] = request.form['data']
        return {task: todo[task]}

    def post(self, task):
        todo[task]


if __name__ == '__main__':
    app.run(debug=True)
