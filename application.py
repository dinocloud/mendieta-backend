from database import db_session
from flask import Flask, jsonify, request, render_template, abort, app
from flask_sqlalchemy import SQLAlchemy
from flask_classy import FlaskView
from settings import DBSettings
from model import *
from serializers import *


#@app.appcontext_tearing_down
#def shutdown_session(exception=None):
#    db_session.remove()

#Setup general objects
app = Flask(__name__)
app.config.from_object(DBSettings)
db = SQLAlchemy()
db.init_app(app)

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
        return jsonify(TenantSchema.dump(tenant).data)

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

@app.route("/")
def home():
    return render_template('index.html', orm="SQLAlchemy")

#Register views
api_prefix = "/api/v1/"
TenantsView.register(app, route_prefix=api_prefix)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)

