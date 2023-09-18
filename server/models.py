from config import db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates

registrations = db.Table('registrations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('opportunity_id', db.Integer, db.ForeignKey('opportunities.id'), primary_key=True)
)




class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    opportunities = db.relationship('Opportunity', secondary=registrations, back_populates='users')
    
    @validates("password")
    def validates_password(self, key, new_password):
        if not new_password:
            raise ValueError("Please set a password")
        
        has_letter = any(char.isalpha() for char in new_password)
        has_number = any(char.isdigit() for char in new_password)

        if not (has_letter and has_number):
            raise ValueError("Password must contain at least one letter AND at least one number")
        
        return generate_password_hash(new_password).decode('utf-8')

class Organization(db.Model):
    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    opportunities = db.relationship('Opportunity', backref='organization', lazy=True)

class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    users = db.relationship('User', secondary=registrations, back_populates='opportunities')
