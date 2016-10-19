import utils
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from passlib.apps import custom_app_context as pwd_context


class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key = True)
    uuid = Column(String(20), unique=True, nullable=False)
    name = Column(String(20), unique=True, nullable=False)

    def __init__(self, name=None):
        self.uuid = utils.random_string(20)
        self.name = name if name is not None else "Unknown{0}".format(utils.random_string(5))

    def __repr__(self):
        return '<Tenant %r>' % (self.name)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(30), nullable=False)
    name = Column(String(15), nullable=False)
    lastname = Column(String(15), nullable=False)
    tenant_uuid = Column(String(20), ForeignKey('tenants.uuid'))
    tenant = relationship("Tenant", foreign_keys=[tenant_uuid])

    def __init__(self, username=None, password=None, email=None, name=None, lastname=None, tenant_uuid=None):
        self.username = username
        self.password = pwd_context.encrypt(password)
        self.email = email
        self.name = name
        self.lastname = lastname
        self.tenant_uuid = tenant_uuid

    def __repr__(self):
        return '<User {0}, {1}>'.format(self.lastname, self.name)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)