CREATE USER '{username}'@'{db_host}' IDENTIFIED BY '{password}';
GRANT ALL PRIVILEGES ON *.* TO '{username}'@'{db_host}' WITH GRANT OPTION;
GRANT SELECT,INSERT,UPDATE,DELETE ON {db_name}.users_{tenant_id} TO '{username}'@'{db_host}';
GRANT SELECT,INSERT,UPDATE,DELETE ON {db_name}.provisioners_{tenant_id} TO '{username}'@'{db_host}';