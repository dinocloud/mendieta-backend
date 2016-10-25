import json
from collections import OrderedDict

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import utils
from utils.settings import DBSettings

INIT_DATA_FILE = 'database/init_data.json'
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DBSettings)
    db = SQLAlchemy()
    db.init_app(app)
    return app


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
    db.session.commit()