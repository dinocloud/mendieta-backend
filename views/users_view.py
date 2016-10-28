from flask import jsonify, request
from flask_classy import FlaskView
from werkzeug.exceptions import *
from database import db, create_tenant_views, create_tenant_admin_user
from model import *
from schemas import *


class TenantsView(FlaskView):
    route_base = "/tenants/"
    tenantSchema = TenantSchema()

    def index(self):
        '''Get all tenants'''
        all_tenants = Tenant.query.order_by(Tenant.name.desc()).all()
        data = self.tenantSchema.dump(all_tenants, many=True).data
        return jsonify({"tenants" : data})

    def get(self, id):
        '''Get a tenant'''
        tenant = Tenant.query.get_or_404(int(id))
        return jsonify(self.tenantSchema.dump(tenant).data)

    def post(self):
        '''Insert a tenant'''
        data = request.json
        name = data.get("name", None)
        if not name:
            abort(400)
        tenant = Tenant(name=name)
        db.session.add(tenant)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

        #Create the views for the database
        try:
            create_tenant_views(tenant.id, tenant.uuid)
        except:
            self.delete(tenant.id)
            raise
        return jsonify(self.tenantSchema.dump(tenant).data), 201

    def delete(self, id):
        '''Delete a tenant'''
        tenant = Tenant.query.get_or_404(int(id))
        db.session.delete(tenant)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify({"message" : "Successfully deleted item.", "id" : tenant.id}), 200


class UsersView(FlaskView):
    route_base = "/users/"
    userSchema = UserSchema()
    userRoleSchema = UserRoleSchema()
    ADMIN_ROLE_ID = 1

    def index(self):
        '''Get all users'''
        all_users = User.query.order_by(User.username.desc())\
            .filter(User.tenant_uuid == request.headers.get("tenant_uuid", None))
        data = self.userSchema.dump(all_users, many=True).data
        return jsonify({"users" : data})

    def get(self, id):
        '''Get a user'''
        user = User.query.get_or_404(int(id)).filter(User.tenant_uuid==request.headers.get("tenant_uuid", None))
        return jsonify(self.userSchema.dump(user).data)

    def post(self):
        '''Insert a user'''
        data = request.json
        headers = request.headers
        username = data.get("username", None)
        password = data.get("password", None)
        email = data.get("email", None)
        name = data.get("name", None)
        lastname = data.get("lastname", None)
        tenant_uuid = headers.get("tenant_uuid", None)
        role = int(data.get("role_id", None))

        if not username or not password or not email or not name or not lastname or not tenant_uuid:
            abort(400, "Missing attributes for user object.")
        user = User(username=username, password=password, email=email, name=name, lastname=lastname,
                    tenant_uuid=tenant_uuid, role_id=role)
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

        if role == self.ADMIN_ROLE_ID:
            #In the password we use the original. The user's one is already encrypted for saving
            try:
                create_tenant_admin_user(user.username, password, user.tenant.id)
            except:
                self.delete(user.id)
                raise
        return jsonify(self.userSchema.dump(user).data), 201

    def delete(self, id):
        '''Delete a user'''
        user = User.query.get_or_404(int(id))
        db.session.delete(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify({"message" : "Successfully deleted item.", "id" : user.id}), 200

    def put(self, id):
        '''Update a user'''
        user = User.query.get_or_404(int(id)).filter(User.tenant_uuid==request.headers.get("tenant_uuid", None))
        data = request.json
        user.username = data.get("username", None)
        user.password = data.get("password", None)
        user.email = data.get("email", None)
        user.name = data.get("name", None)
        user.lastname = data.get("lastname", None)
        if not user.username or not user.password or not user.email or not user.name \
                or not user.lastname:
            abort(400, "Missing attributes for user object.")
        db.session.merge(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify({"message": "Successfully updated item.",
                        "item": self.userSchema.dump(user).data})
