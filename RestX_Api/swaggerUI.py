#  Same as ory4.py but this time using Swagger UI

from flask import Flask
from flask_restx import Resource, Api, fields

app = Flask(__name__)
api = Api(app)

# Setting my models here
fc_model = api.model('Warehouse', {'site': fields.String('The Warehouse.')})  # 'id': fields.Integer('ID')
warehouse = api.model()
sites = [[], [], []]
fc_house = {'site': 'KGB1', 'id': 1}  # 'region': 'EU', 'subregion': 'WEU'
sites.append(fc_house)


@api.route('/site')
class Warehouse(Resource):

    @api.marshal_with(fc_model, envelope='All_Warehouses')
    def get(self):
        return sites

    @api.expect(fc_model)
    def post(self):
        new_site = api.payload
        new_site['id'] = len(sites) + 1
        sites.append(new_site)
        return {'result': 'Site added'}, 201

    @api.expect(warehouse)
    def put(self):
        new_site = api.payload
        new_sme = api.payload
        proxy = api.payload
        sites.append(proxy, new_sme, new_site)
        return {'result': 'Data perfectly Added'}


if __name__ == '__main__':
    app.run(debug=True)
