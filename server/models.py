from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask_bcrypt import bcrypt
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String)

    memberships = db.relationship('UserOrganization', back_populates='user', cascade='all, delete-orphan')
    organizations = association_proxy('memberships', 'organization')

    @property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, new_password):
        if isinstance(new_password, str) and 1 <= len(new_password) <= 15:
            secret = new_password.encode('utf-8')
            supersecret = bcrypt.generate_password_hash(secret)
            new_password_hash = supersecret.decode('utf-8')
            self._password_hash = new_password_hash
        else:
            raise ValueError('Password must be between 1-15 characters!')
        
    def authenticate(self, test_string):
        return bcrypt.check_password_hash(self.password_hash, test_string.encode('utf-8'))

    @validates('name')
    def validates_name(self, key, new_name):
        if isinstance(new_name, str) and 1 <= len(new_name) <= 20:
            return new_name
        else:
            raise ValueError('Name must be between 1-20 characters!')

    serialize_rules = ('-memberships', '-organizations', )

    def __repr__(self):
        return f'<User {self.id}: {self.name} : {self.username}>'

class UserOrganization(db.Model, SerializerMixin):
    __tablename__ = 'user_organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    user = db.relationship('User', back_populates='memberships')
    organization = db.relationship('Organization', back_populates='memberships')

    def __repr__(self):
        return f'<UserOrganization {self.id}>'

class Organization(db.Model, SerializerMixin):
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    motto = db.Column(db.String)

    memberships = db.relationship('UserOrganization', back_populates='organization')
    users = association_proxy('memberships', 'user')

    serialize_rules = ('-memberships', '-users')

    def __repr__(self):
        return f'<Organization {self.id}: {self.name}: {self.motto}>'

class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    co_mingle = db.Column(db.Boolean)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    def __repr__(self):
        return f'<Event {self.id}: {self.title}:{self.description} : {self.co_mingle}>'
