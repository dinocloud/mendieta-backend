import os
class DBSettings:
    DB_ENGINE = "mysql+pymysql"
    DB_HOST = os.getenv("RDS_HOSTNAME","127.0.0.1")
    DB_NAME = os.getenv("RDS_DB_NAME","mendietatest")
    DB_PORT = os.getenv("RDS_PORT","3306")
    DB_USER = os.getenv("RDS_USERNAME","root")
    DB_PASSWORD = os.getenv("RDS_PASSWORD","armenia")
    SQLALCHEMY_DATABASE_URI = "{0}://{1}:{2}@{3}/{4}".format(DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
