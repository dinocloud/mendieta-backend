#!/bin/bash
eb init -p python2.7 mendieta
eb create mendieta-env -v -r us-west-2 -i t2.micro -s -db.engine mysql -db.user root -db.pass armenia1234 -db.size 5 --envvars APP_PORT=80