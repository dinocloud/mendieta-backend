import json
from collections import OrderedDict
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import utils
from utils.settings import DBSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, create_session

INIT_DATA_FILE = 'database/init_data.json'
SQL_CREATE_VIEWS_FILE = 'sql/create_views.sql'
SQL_CREATE_ADMIN_USER_FILE = 'sql/create_admin_user.sql'
db = SQLAlchemy()

def get_scoped_session(uri):
    init_engine(uri)
    return scoped_session(lambda: create_session(bind=engine))


def init_engine(uri, **kwargs):
    global engine
    engine = create_engine(uri, **kwargs)
    return engine

def create_app():
    application = Flask(__name__)
    application.config.from_object(DBSettings)
    init_engine(application.config['SQLALCHEMY_DATABASE_URI'])
    db = SQLAlchemy()
    db.init_app(application)
    return application


def init_base_data():
    with open(INIT_DATA_FILE, 'r') as file:
        config = json.load(file, object_pairs_hook=OrderedDict)
    for class_name, list_objects in config.items():
        for list_attributes in list_objects:
            Object = utils.get_class(class_name)
            object = Object()
            for object_key, object_value in list_attributes.items():
                setattr(object, object_key, object_value)
            old_object = Object.query.get(object.id)
            if old_object:
                old_object = object
                db.session.merge(old_object)
            else:
                db.session.add(object)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise


def create_tenant_admin_user(username, password, tenant_id):
    params = {}
    params["db_host"] = DBSettings.DB_HOST
    params["db_name"] = DBSettings.DB_NAME
    params["username"] = username
    params["password"] = password
    params["tenant_id"] = tenant_id
    __execute_sql_script(SQL_CREATE_ADMIN_USER_FILE, params)


def create_tenant_views(tenant_id, tenant_uuid):
    params = {}
    params[tenant_id]  = tenant_id
    params[tenant_uuid] = tenant_uuid
    __execute_sql_script(INIT_DATA_FILE, params)


def __execute_sql_script(script_name, params):
    with open(script_name, 'r') as file:
        sql_query = file.read().replace('\n', ' ').format(**params)
    db.engine.execute(sql_query)