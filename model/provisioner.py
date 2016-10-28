from database import db

class Provisioner(db.Model):
    __tablename__ = 'provisioners'
    id = db.Column(db.Integer, primary_key=True)
    tenant_uuid = db.Column(db.String(20), db.ForeignKey('tenants.uuid'))
    tenant = db.relationship("Tenant", foreign_keys=[tenant_uuid], cascade="merge")
    fancy_name = db.Column(db.String(20), unique=False, nullable=False)
    provisioner_type_id = db.Column(db.Integer, db.ForeignKey('provisioner_types.id'))
    provisioner_type = db.relationship("ProvisionerType", foreign_keys=[provisioner_type_id], cascade="merge")
    provisioner_fields = db.relationship("ProvisionerField", uselist=True, backref=db.backref('provisioner'),
                                         cascade="save-update, merge, delete") #, lazy='dynamic'

    def __init__(self, fancy_name=None, tenant_uuid=None, provisioner_type=None, provisioner_fields=None):
        self.tenant_uuid = tenant_uuid
        self.fancy_name = fancy_name
        self.provisioner_type = provisioner_type
        self.provisioner_fields = provisioner_fields

    def __repr__(self):
        return '<Provisioner {0}>'.format(self.fancy_name)


class ProvisionerField(db.Model):
    __tablename__ = "provisioner_fields"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    value = db.Column(db.String(120), nullable=False)
    provisioner_id = db.Column(db.Integer, db.ForeignKey('provisioners.id'))
    tenant_uuid = db.Column(db.String(20), db.ForeignKey('tenants.uuid'))
    tenant = db.relationship("Tenant", foreign_keys=[tenant_uuid], cascade="merge")

    def __init__(self, name=None, value=None, provisioner_id=None, tenant_uuid=None):
        self.name = name
        self.value = value
        self.provisioner_id = provisioner_id
        self.tenant_uuid = tenant_uuid

    def __repr__(self):
        return '<Provisioner {0}, key: {1}, value: {2}>'.format(self.provisioner_id, self.name, self.value)


class ProvisionerRequiredField(db.Model):
    __tablename__ = 'provisioner_required_fields'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10), unique=True, nullable=False)
    provisioner_type_id = db.Column(db.Integer, db.ForeignKey('provisioner_types.id'))

    def __init__(self, description=None, provisioner_type_id=None):
        self.description = description
        self.provisioner_type_id = provisioner_type_id

    def __repr__(self):
        return '<Provisioner {0}, required field: {1}>'.format(self.provisioner_type.description, self.description)


class ProvisionerType(db.Model):
    __tablename__ = 'provisioner_types'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10), unique=True, nullable=False)
    provisioner_required_fields = db.relationship("ProvisionerRequiredField",
                                                  uselist=True, cascade="save-update, delete, merge") #, backref="provisioner_required_fields"

    def __init__(self, id=None, description=None):
        self.id = id
        self.description = description

    #def __init__(self, description=None):
     #   self.description = description

    def __repr__(self):
        return '<Provisioner type {0}>'.format(self.description)