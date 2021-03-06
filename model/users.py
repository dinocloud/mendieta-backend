from passlib.apps import custom_app_context as pwd_context

import utils
from database.database import db


class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key = True)
    uuid = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, name=None):
        self.uuid = utils.random_string(20)
        self.name = name if name is not None else "Unknown{0}".format(utils.random_string(5))

    def __repr__(self):
        return '<Tenant %r>' % (self.name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15), nullable=False)
    tenant_uuid = db.Column(db.String(20), db.ForeignKey('tenants.uuid'))
    tenant = db.relationship("Tenant", foreign_keys=[tenant_uuid], cascade="merge")
    role_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'))
    role = db.relationship("UserRole", foreign_keys=[role_id], cascade="merge")

    def __init__(self, username=None, password='', email=None, name=None, lastname=None,
                 tenant_uuid=None, role_id=None):
        self.username = username
        self.password = pwd_context.encrypt(password)
        self.email = email
        self.name = name
        self.lastname = lastname
        self.tenant_uuid = tenant_uuid
        self.role_id = role_id

    def __repr__(self):
        return '<User {0}, {1}>'.format(self.lastname, self.name)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


class UserRole(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, description=None):
        self.description = description

    def __repr__(self):
        return '<User Role {0}>'.format(self.description)