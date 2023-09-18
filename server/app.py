from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt 
from models import User, VolunteerOpportunity, Organization, Opportunity
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required

from config import app, api, db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volunteer.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app) 

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'})

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            login_user(user)
            return jsonify({'message': 'Logged in successfully'})
        return jsonify({'message': 'Invalid credentials'}), 401
    # If GET request, render login page (if using templates)
    # return render_template('login.html')

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/organizations', methods=['POST'])
def add_organization():
    data = request.get_json()
    new_org = Organization(name=data['name'], description=data['description'])
    db.session.add(new_org)
    db.session.commit()
    return jsonify({'message': 'Organization added'})

@app.route('/api/organizations', methods=['GET'])
def get_organizations():
    orgs = Organization.query.all()
    return jsonify([{'id': org.id, 'name': org.name, 'description': org.description} for org in orgs])

@app.route('/api/opportunities', methods=['POST'])
def add_opportunity():
    data = request.get_json()
    new_opp = VolunteerOpportunity(title=data['title'], description=data['description'], organization_id=data['organization_id'])
    db.session.add(new_opp)
    db.session.commit()
    return jsonify({'message': 'Opportunity added'})

@app.route('/api/opportunities', methods=['GET'])
def get_opportunities():
    opps = VolunteerOpportunity.query.all()
    return jsonify([{'id': opp.id, 'title': opp.title, 'description': opp.description, 'organization_id': opp.organization_id} for opp in opps])

@app.route('/api/opportunities', methods=['PATCH'])
def update_opportunity(id):
    opportunity = Opportunity.query.get(id)
    data = request.get_json()
    opportunity.title = data['title']
    opportunity.description = data['description']
    db.session.commit()
    return jsonify(opportunity.serialize())

@app.route('/api/opportunities', methods=['DELETE'])
def delete_opportunity(id):
    opportunity = Opportunity.query.get(id)
    db.session.delete(opportunity)
    db.session.commit()
    return jsonify({'message': 'Opportunity deleted successfully'})

if __name__ == '__main__':
    app.run(debug = True, port=5555)
