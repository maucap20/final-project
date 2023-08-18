from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volunteer.db'
db = SQLAlchemy(app)
CORS(app)  # Allow cross-origin requests (for development purposes)

# Define your User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # Add other fields as needed

# Set up your registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Process and validate registration data
    # Create a new user in the database (sample code)
    new_user = User(email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'})

if __name__ == '__main__':
    app.run(debug=True)
