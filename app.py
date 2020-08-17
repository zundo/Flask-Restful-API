from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# add config for firebase database, so tell him where to store it
basedir = os.path.abspath(os.path.dirname(__file__))
# add configuration variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site_area.db')


# initialize our db before using it
db = SQLAlchemy(app)
ma = Marshmallow(app)


# creation of the db
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


# destroy the db
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


# seeding with Flask CLI our db and testing
@app.cli.command('db_seed')
def db_seed():
    ory4 = Sites(whid_name='ORY4',
                 whid_type='FC',
                 whid_home='Bretigny',
                 whid_id=101879,
                 region='EMEA',
                 sub_region='SEU',
                 country='France',
                 site_lead='Stephane Taille',
                 proxy='Nicolas Pommier',
                 idf=14,
                 sme='Michael Sotelino',
                 area=10236
                 )
    xfrj = Sites(whid_name='XFRJ',
                 whid_type='AMXL',
                 whid_home='Savigny-le-Temple',
                 whid_id=10189,
                 region='EMEA',
                 sub_region='SEU',
                 country='France',
                 site_lead='Thibault Boullet',
                 proxy='Chloe Aubin',
                 idf=18,
                 sme='Romeo Zade ',
                 area=11560
                 )
    dif6 = Sites(whid_name='DIF6',
                 whid_type='AEN',
                 whid_home='Noisy-le-Grand',
                 whid_id=202879,
                 region='EMEA',
                 sub_region='SEU',
                 country='France',
                 site_lead='Jeremy CAQUELIN',
                 proxy='Jefferson',
                 idf=6,
                 sme='Jefferson',
                 area=9399
                 )

    db.session.add(ory4)
    db.session.add(dif6)
    db.session.add(xfrj)

    test_user = User(first_name='Jefferson',
                     last_name='Duerin',
                     email='duerinj@amazon.fr',
                     password='P@ssw0rd',
                     whid='ORY4',
                     role='IT Support Eng II'
                     )

    db.session.add(test_user)
    # without the commit the script run but nothing is save inside the db
    db.session.commit()
    print('Database Seeded!')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return 'Hello from Sitemon Planetary Restful API.'


@app.route('/json_test')
def json_test():
    return jsonify(whid='whid',
                   login='login',
                   message='Hello from Site Management Tool',
                   identifier="12345"), 200
    # 200 is by default no need to add it


# how to add status code to the responds, so add an endpoint to generate error
@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    whid = request.args.get('whid')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message='Sorry ' + name + ' you are not old enough.'), 401
    else:
        return jsonify(message="Welcome " + name + " from " + whid + " , you are old enough!")


@app.route('/url_variables/<string:name>/<string:whid>/<int:age>')
def url_variables(name: str, whid: str, age: int):
    if age < 18:
        return jsonify(message='Sorry ' + name + ' you are not old enough.'), 401
    else:
        return jsonify(message="Welcome " + name + " from " + whid + ", you are old enough!")


# this route is created to only respond to GET request
@app.route('/sites', methods=['GET'])
def sites():
    sites_list = Sites.query.all()
    result = sites_schema.dump(sites_list)
    return jsonify(result)


# Database MODELING
# start set up model for our db => db models
class User(db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    whid = Column(String)
    role = Column(String)


class Sites(db.Model):
    __tablename__ = 'Warehouse'
    whid_id = Column(Integer, primary_key=True, unique=True)
    whid_name = Column(String)
    whid_type = Column(String)
    whid_home = Column(String)
    country = Column(String)
    region = Column(String)
    sub_region = Column(String)
    site_lead = Column(String)
    sme = Column(String)
    proxy = Column(String)
    area = Column(Float)
    idf = Column(Integer)


# class for Marshmallow
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'whid', 'role')


class SitesSchema(ma.Schema):
    class Meta:
        fields = ('whid_id', 'whid_name', 'whid_type', 'whid_home', 'country', 'region', 'sub_region', 'site_lead',
                  'sme', 'proxy', 'area', 'idf')


# now we need to instanciate our Schemas in two different ways ## many=True is a deserializer
user_schema = UserSchema()
users_schema = UserSchema(many=True)

site_schema = SitesSchema()
sites_schema = SitesSchema(many=True)


if __name__ == '__main__':
    app.run()
