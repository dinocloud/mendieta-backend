from flask_httpauth import HTTPBasicAuth
from model import User
from flask import request

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    headers = request.headers
    user = User.query.filter_by(username = username, tenant_uuid = headers.get("tenant_uuid", None)).first()
    if not user or not user.verify_password(password):
        return False
    return True
