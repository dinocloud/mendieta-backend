from flask import jsonify, request, render_template
from database import db, create_app, init_base_data
from views import *
import os
#Setup general objects
app = create_app()

@app.errorhandler(404)
@app.errorhandler(403)
@app.errorhandler(400)
@app.errorhandler(500)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


@app.route("/")
def home():
    return render_template('index.html', orm="SQLAlchemy")

#Register views
api_prefix = "/api/v1/"
TenantsView.register(app, route_prefix=api_prefix)
UsersView.register(app, route_prefix=api_prefix)
ProvisionerTypeView.register(app, route_prefix=api_prefix)
ProvisionerView.register(app, route_prefix=api_prefix)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_base_data()
    app.run(port=int(os.getenv("APP_PORT", 5000)), debug=True)

