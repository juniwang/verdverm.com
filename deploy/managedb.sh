#!/bin/bash

args="$@"
db_url="127.0.0.1:5432"
db_user="super"
db_pass="password"
db_name="verdverm_com_dev"

cd ../site

docker run --rm -i -t --name verdverm.com-managedb \
	--link verdverm.com-psql:vvdb \
	-v $(pwd):/src \
	-e DATABASE_URL="postgresql://$db_user:$db_pass@vvdb/$db_name" \
	verdverm/verdverm.com-flask $args

