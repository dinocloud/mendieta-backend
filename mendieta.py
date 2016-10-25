from flask import jsonify, request, render_template, g
from flask_httpauth import HTTPBasicAuth
from database.database import db, create_app, init_base_data
from model import *
from views import *

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

