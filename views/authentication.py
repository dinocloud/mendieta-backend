from flask_httpauth import HTTPBasicAuth
from model import User, Tenant
from functools import wraps
from flask import request, Response

ADMIN_TENANT_ID = 1

auth = HTTPBasicAuth()

# def verify_password(username, password, tenant_uuid):
#     headers = request.headers
#     user = User.query.filter_by(username = username, tenant_uuid = headers.get("tenant_uuid", None)).first()
#     if not user or not user.verify_password(password):
#         return False
#     return True

def verify_password(username, password, tenant_uuid):
    headers = request.headers
    user = User.query.filter_by(username = username, tenant_uuid = headers.get("tenant_uuid", None)).first()
    if not user or not user.verify_password(password):
        return False
    return True

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        tenant_uuid = request.headers.get("tenant_uuid", None)
        if not auth or not tenant_uuid or not verify_password(auth.username, auth.password, tenant_uuid):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def requires_admin_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        tenant_uuid = request.headers.get("tenant_uuid", None)
        admin_tenant = Tenant.query.get_or_404(ADMIN_TENANT_ID)
        if not auth or not tenant_uuid or not tenant_uuid == admin_tenant.uuid \
                or not verify_password(auth.username, auth.password, tenant_uuid):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


