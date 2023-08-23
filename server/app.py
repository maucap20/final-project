from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt 
from models import User, VolunteerOpportunity, Organization, registrations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volunteer.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app) 


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful', 'user_id': user.id})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Login required!"'})


@app.route('/organizations', methods=['POST'])
def add_organization():
    data = request.get_json()
    new_org = Organization(name=data['name'], description=data['description'])
    db.session.add(new_org)
    db.session.commit()
    return jsonify({'message': 'Organization added'})

@app.route('/organizations', methods=['GET'])
def get_organizations():
    orgs = Organization.query.all()
    return jsonify([{'id': org.id, 'name': org.name, 'description': org.description} for org in orgs])

@app.route('/opportunities', methods=['POST'])
def add_opportunity():
    data = request.get_json()
    new_opp = VolunteerOpportunity(title=data['title'], description=data['description'], organization_id=data['organization_id'])
    db.session.add(new_opp)
    db.session.commit()
    return jsonify({'message': 'Opportunity added'})

@app.route('/opportunities', methods=['GET'])
def get_opportunities():
    opps = VolunteerOpportunity.query.all()
    return jsonify([{'id': opp.id, 'title': opp.title, 'description': opp.description, 'organization_id': opp.organization_id} for opp in opps])


if __name__ == '__main__':
    app.run(debug = True)
