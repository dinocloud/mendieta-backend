from flask import Flask, jsonify, request, render_template, abort, app, g
from flask_classy import FlaskView
from model import *
from schemas import *
from flask_httpauth import HTTPBasicAuth
from werkzeug.exceptions import *
from database import db, create_app, init_base_data

#Setup general objects
auth = HTTPBasicAuth()
app = create_app()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@app.errorhandler(404)
@app.errorhandler(403)
@app.errorhandler(400)
@app.errorhandler(500)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


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
        db.session.commit()
        return jsonify(self.tenantSchema.dump(tenant).data), 201

    def delete(self, id):
        '''Delete a tenant'''
        tenant = Tenant.query.get_or_404(int(id))
        db.session.delete(tenant)
        db.session.commit()
        return jsonify({"message" : "Successfully deleted item.", "id" : tenant.id}), 200

    def put(self, id):
        '''Update a tenant'''
        tenant = Tenant.query.get_or_404(int(id))
        tenant.name = request.json.get("name", tenant.name)
        db.session.add(tenant)
        db.session.commit()
        return jsonify({"message": "Successfully updated item.",
                        "item": self.tenantSchema.dump(tenant).data})


class UsersView(FlaskView):
    route_base = "/users/"
    userSchema = UserSchema()

    def index(self):
        '''Get all users'''
        all_users = User.query.order_by(User.username.desc())\
            .filter(User.tenant_uuid==request.headers.get("tenant_uuid", None))
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
        if not username or not password or not email or not name or not lastname or not tenant_uuid:
            abort(400, "Missing attributes for user object.")
        user = User(username=username, password=password, email=email, name=name, lastname=lastname,
                    tenant_uuid=tenant_uuid)
        db.session.add(user)
        db.session.commit()
        return jsonify(self.userSchema.dump(user).data), 201

    def delete(self, id):
        '''Delete a user'''
        user = User.query.get_or_404(int(id))
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message" : "Successfully deleted item.", "id" : user.id}), 200

    def put(self, id):
        '''Update a user'''
        user = User.query.get_or_404(int(id))
        user.name = request.json.get("name", user.name)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Successfully updated item.",
                        "item": self.userSchema.dump(user).data})

@app.route("/")
def home():
    return render_template('index.html', orm="SQLAlchemy")

#Register views
api_prefix = "/api/v1/"
TenantsView.register(app, route_prefix=api_prefix)
UsersView.register(app, route_prefix=api_prefix)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_base_data()
    app.run(port=5000, debug=True)

