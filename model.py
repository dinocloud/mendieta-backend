import utils
from database import db
from passlib.apps import custom_app_context as pwd_context


class Provisioner(db.Model):
    __tablename__ = 'provisioners'
    id = db.Column(db.Integer, primary_key=True)
    tenant_uuid = db.Column(db.String(20), db.ForeignKey('tenants.uuid'))
    tenant = db.relationship("Tenant", foreign_keys=[tenant_uuid])
    fancy_name = db.Column(db.String(20), unique=False, nullable=False)
    provisioner_type_id = db.Column(db.Integer, db.ForeignKey('provisioner_types.id'))
    provisioner_type = db.relationship("ProvisionerType", foreign_keys=[provisioner_type_id])
    provisioner_fields = db.relationship("ProvisionerField")

    def __init__(self, fancy_name=None, tenant_uuid=None, provisioner_type_id=None):
        self.tenant_uuid = tenant_uuid
        self.fancy_name = fancy_name
        self.provisioner_type_id = provisioner_type_id

    def __repr__(self):
        return '<Provisioner {0}>'.format(self.fancy_name)


class ProvisionerField(db.Model):
    __tablename__ = "provisioner_fields"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(20), nullable=False)
    value = db.Column(db.String(120), nullable=False)
    provisioner_id = db.Column(db.Integer, db.ForeignKey('provisioners.id'))
    tenant_uuid = db.Column(db.String(20), db.ForeignKey('tenants.uuid'))
    tenant = db.relationship("Tenant", foreign_keys=[tenant_uuid])

    def __init__(self, key=None, value=None, provisioner_id=None, tenant_uuid=None):
        self.key = key
        self.value = value
        self.provisioner_id = provisioner_id
        self.tenant_uuid = tenant_uuid

    def __repr__(self):
        return '<Provisioner {0}, key: {1}, value: {2}>'.format(self.provisioner_id, self.key, self.value)


class ProvisionerRequiredField(db.Model):
    __tablename__ = 'provisioner_required_fields'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10), unique=True, nullable=False)
    provisioner_type_id = db.Column(db.Integer, db.ForeignKey('provisioner_types.id'))

    def __init__(self):
        pass

    def __init__(self, id=None, description=None, provisioner_type_id=None):
        self.id = id
        self.description = description
        self.provisioner_type_id = provisioner_type_id

    def __init__(self, description=None, provisioner_type_id=None):
        self.description = description
        self.provisioner_type_id = provisioner_type_id

    def __repr__(self):
        return '<Provisioner {0}, required field: {1}>'.format(self.provisioner_type.description, self.description)


class ProvisionerType(db.Model):
    __tablename__ = 'provisioner_types'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10), unique=True, nullable=False)
    provisioner_required_fields = db.relationship("ProvisionerRequiredField") #, backref="provisioner_required_fields"

    def __init__(self):
        pass

    def __init__(self, description=None):
        self.description = description

    def __repr__(self):
        return '<Provisioner type {0}>'.format(self.description)


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
    email = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15), nullable=False)
    tenant_uuid = db.Column(db.String(20), db.ForeignKey('tenants.uuid'))
    tenant = db.relationship("Tenant", foreign_keys=[tenant_uuid])

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
