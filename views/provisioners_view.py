from flask import jsonify, request
from flask_classy import FlaskView, route
from werkzeug.exceptions import *
from database import db
from model import *
from schemas import *
from authentication import requires_auth


class ProvisionerView(FlaskView):
    route_base = "/provisioner/"
    provisionerSchema = ProvisionerSchema()
    provisionerTypeSchema = ProvisionerTypeSchema()
    provisionerFieldSchema = ProvisionerFieldSchema()

    @requires_auth
    def index(self):
        all_provisioners = Provisioner.query\
            .filter(Provisioner.tenant_uuid == request.headers.get("tenant_uuid", None))
        data = self.provisionerSchema.dump(all_provisioners, many=True).data
        return jsonify({"provisioners" : data})

    @requires_auth
    def get(self, id):
        provisioner = Provisioner.query.get_or_404(int(id)).filter(Provisioner.tenant_uuid
                                                                   == request.headers.get("tenant_uuid", None))
        return jsonify(self.provisionerSchema.dump(provisioner).data)

    @requires_auth
    def post(self):
        data = request.json
        headers = request.headers
        tenant_uuid = headers.get("tenant_uuid", None)
        fancy_name = data.get("fancy_name", None)

        provisioner_fields = []
        for field in data.get("provisioner_fields", None):
            key = field.get("name", None)
            value = field.get("value", None)
            provisioner_field = ProvisionerField(name=key, value=value, tenant_uuid=tenant_uuid)
            provisioner_fields.append(provisioner_field)

        provisioner_type = ProvisionerType.query.get_or_404(int(data.get("provisioner_type_id", None)))

        if not tenant_uuid or not fancy_name:
            abort(400, "Missing attributes for provisioner object")
        provisioner = Provisioner(fancy_name=fancy_name, tenant_uuid=tenant_uuid, provisioner_type=provisioner_type,
                                  provisioner_fields=provisioner_fields)
        db.session.add(provisioner)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify(self.provisionerSchema.dump(provisioner).data), 201

    @requires_auth
    def delete(self, id):
        provisioner = Provisioner.query.get_or_404(int(id))
        db.session.delete(provisioner)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify({"message": "Successfully deleted item.", "id": provisioner.id}), 200

    @requires_auth
    def put(self, id):
        provisioner = Provisioner.query.get_or_404(int(id))\
            .filter(Provisioner.tenant_uuid==request.headers.get("tenant_uuid", None))
        data = request.json
        provisioner.fancy_name = data.get("fancy_name", None)
        provisioner.provisioner_type = data.get("provisioner_type", None)
        provisioner.provisioner_fields = data.get("provisioner_fields", None)
        if  not provisioner.fancy_name or not provisioner.provisioner_type or not provisioner.provisioner_fields:
            abort(400, "Missing attributes for provisioner object")
        db.session.merge(provisioner)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify({"message": "Successfully updated item.",
                        "item": self.provisionerSchema.dump(provisioner).data})


class ProvisionerTypeView(FlaskView):
    route_base = "/provisioner/types/"
    provisionerTypeSchema = ProvisionerTypeSchema()

    def index(self):
        '''Get all provisioner types'''
        all_prov_types = ProvisionerType.query.order_by(ProvisionerType.description.desc()).all()
        data = self.provisionerTypeSchema.dump(all_prov_types, many=True).data
        return jsonify({"provisioner_types" : data})

    def get(self, id):
        '''Get a provisioner type'''
        prov_type = ProvisionerType.query.get_or_404(int(id))
        return jsonify(self.provisionerTypeSchema.dump(prov_type).data)

