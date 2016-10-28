CREATE VIEW users_{tenant_id} AS SELECT id, username, password, email, name, lastname FROM users
WHERE users.tenant_uuid = '{tenant_uuid}';

CREATE VIEW provisioners_{tenant_id} AS SELECT id, fancy_name, provisioner_type_id FROM provisioners
WHERE provisioners.tenant_uuid = '{tenant_uuid}';

CREATE VIEW provisioner_fields_{tenant_id} AS SELECT id, name, value, provisioner_id FROM provisioner_fields
WHERE provisioner_fields.tenant_uuid = '{tenant_uuid}';