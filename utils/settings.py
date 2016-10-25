
class DBSettings:
    DB_ENGINE = "mysql"
    DB_HOST = "127.0.0.1"
    DB_NAME = "mendieta"
    DB_PORT = "3306"
    DB_USER = "root"
    DB_PASSWORD = "armenia"
    SQLALCHEMY_DATABASE_URI = "{0}://{1}:{2}@{3}/{4}".format(DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)


TABLE_TENANT = "tenants"
TABLE_TENANT_FIELDS = ["id", "uuid", "name"]
