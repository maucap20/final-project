from flask import Flask, request, make_response, jsonify, session
from flask_cors import CORS
from models import User, Organization, UserOrganization
from flask_login import login_user, logout_user, login_required
from flask_restful import Resource
from config import app, api, db
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError  # This is for handling unique constraint violations

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return '<h1>Welcome to Service Center</h1>'

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return make_response({'error': 'Username and password are required.'}, 400)

    user = User.query.filter_by(username=username).first()
    if not user:
        return make_response({'error': 'User not found'}, 422)

    if not user.authenticate(password):
        return make_response({'error': 'Incorrect password'}, 401)

    session['user_id'] = user.id
    return make_response(user.to_dict())


class Users(Resource):
    def post(self):
        data = request.get_json()
        try:
            newUser = User(
                name = data["name"],
                username = data["username"],
                password_hash = data["password"]
            )
            db.session.add(newUser)
            db.session.commit()
            session['user_id'] = newUser.id

        except ValueError as v_error:
            return make_response({'error' : [str(v_error)]}, 422)

        return make_response(newUser.to_dict(), 201)
api.add_resource(Users, '/users')

@app.route('/logout', methods=['DELETE'])
def logout():
    session['user_id'] = None
    return make_response('', 204)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    try:
        new_user = User(name=data['name'], username=data['username'], password_hash=data['password'])
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
    except IntegrityError:
        return jsonify({'success': False, 'error': 'Username already exists'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
    return make_response(new_user.to_dict(), 201)



@app.route('/api/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            login_user(user)
            return jsonify({'message': 'Logged in successfully'})
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/logout')
@login_required
def logout_route():
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
def get_organizations_route():
    orgs = Organization.query.all()
    return jsonify([{'id': org.id, 'name': org.name, 'description': org.description} for org in orgs])

@app.route('/api/opportunities', methods=['POST'])
def add_opportunity_route():
    data = request.get_json()
    new_opp = Opportunity(
        title=data['title'],
        description=data['description'],
        organization_id=data['organization_id']
    )
    db.session.add(new_opp)
    db.session.commit()
    return jsonify({'message': 'Opportunity added'})

@app.route('/api/opportunities', methods=['GET'])
def get_opportunities_route():
    opps = Opportunity.query.all()
    return jsonify([{'id': opp.id, 'title': opp.title, 'description': opp.description, 'organization_id': opp.organization_id} for opp in opps])

@app.route('/api/opportunities/<int:id>', methods=['PATCH'])
def update_opportunity_route(id):
    opportunity = Opportunity.query.get(id)
    data = request.get_json()
    opportunity.title = data['title']
    opportunity.description = data['description']
    db.session.commit()
    return jsonify(opportunity.serialize())

@app.route('/api/opportunities/<int:id>', methods=['DELETE'])
def delete_opportunity_route(id):
    opportunity = Opportunity.query.get(id)
    db.session.delete(opportunity)
    db.session.commit()
    return jsonify({'message': 'Opportunity deleted successfully'})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
