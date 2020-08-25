from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

team_ory4 = api.model('Lambda', {'TeamMember': fields.String('The Team Member.')})

ory4 = []
python = {'TeamMember': 'Pommiern'}
ory4.append(python)


@api.add('lambda', 'world')


@api.route('/lambda')
class Lambda(Resource):
    def get(self):
        return ory4

    def put(self):
        return team_ory4

    def post(self):
        return ory4


if __name__ == '__main__':
    app.run(debug=True)
