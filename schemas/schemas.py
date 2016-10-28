'''Schemas common to all apps'''
from marshmallow import Schema, fields

class TenantSchema(Schema):
    id = fields.Integer()
    uuid = fields.String()
    name = fields.String()

class ProvisionerFieldSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    value = fields.String()
    tenant = fields.Nested(TenantSchema())

class ProvisionerRequiredFieldSchema(Schema):
    id = fields.Integer()
    description = fields.String()

class ProvisionerTypeSchema(Schema):
    id = fields.Integer()
    description = fields.String()
    provisioner_required_fields = fields.List(fields.Nested(ProvisionerRequiredFieldSchema()))

class ProvisionerSchema(Schema):
    id = fields.Integer()
    tenant = fields.Nested(TenantSchema())
    fancy_name = fields.String()
    provisioner_type = fields.Nested(ProvisionerTypeSchema())
    provisioner_fields = fields.List(fields.Nested(ProvisionerFieldSchema()))

class UserRoleSchema(Schema):
    id = fields.Integer()
    description = fields.String()

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    password = fields.String()
    email = fields.String()
    name = fields.String()
    lastname = fields.String()
    tenant = fields.Nested(TenantSchema())
    role = fields.Nested(UserRoleSchema())

