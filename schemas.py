'''Schemas common to all apps'''
from marshmallow import Schema, fields


class TenantSchema(Schema):
    id = fields.Integer()
    uuid = fields.String()
    name = fields.String()


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    password = fields.String()
    email = fields.String()
    name = fields.String()
    lastname = fields.String()
    tenant = fields.Nested(TenantSchema())