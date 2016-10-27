from flask import jsonify, request, render_template
from database import db, create_app, init_base_data
from utils import DBSettings
from views import *
import os
#Setup general objects
application = create_app()

@application.errorhandler(404)
@application.errorhandler(403)
@application.errorhandler(400)
@application.errorhandler(500)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


@application.route("/")
def home():
    return "Hello World!: URI: {0}".format(DBSettings.SQLALCHEMY_DATABASE_URI)


#Register views
api_prefix = "/api/v1/"
TenantsView.register(application, route_prefix=api_prefix)
UsersView.register(application, route_prefix=api_prefix)
ProvisionerTypeView.register(application, route_prefix=api_prefix)
ProvisionerView.register(application, route_prefix=api_prefix)


if __name__ == '__main__':
    with application.app_context():
        from model import *
        db.create_all()
        init_base_data()
        application.run(port=int(os.getenv("APP_PORT", 5000)), debug=True)

