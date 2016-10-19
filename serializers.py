'''Serializers common to all apps'''
from marshmallow import Schema, fields

class TenantSchema(Schema):
    id = fields.Integer()
    uuid = fields.String()
    name = fields.String()