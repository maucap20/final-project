from config import db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

registrations = db.Table('registrations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('opportunity_id', db.Integer, db.ForeignKey('volunteer_opportunities.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Organization(db.Model):
    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)


class VolunteerOpportunity(db.Model):
    __tablename__ = "volunteer_opportunities"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    organization = db.relationship('Organization', backref=db.backref('opportunities', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('opportunities', lazy=True))

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    opportunities = db.relationship('Opportunity', secondary='participations', back_populates='volunteers')

class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    volunteers = db.relationship('Volunteer', secondary='participations', back_populates='opportunities')

participations = db.Table(
    'participations',
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteers.id'), primary_key=True),
    db.Column('opportunity_id', db.Integer, db.ForeignKey('opportunities.id'), primary_key=True)
)

