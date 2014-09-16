#!/bin/bash



# startup psql docker
cd ..
mkdir -p tmp/postgresql

db_url="0.0.0.0:5432"
db_user="super"
db_pass="password"
db_name="verdverm_com_dev"

docker run -d --name verdverm.com-psql \
	-p $db_url:5432 \
	-v $(pwd)/tmp/postgresql:/data \
	-e USER="$db_user" \
	-e PASS="$db_pass" \
	-e DB="$db_name" \
	verdverm/verdverm.com-postgresql



cd site

docker run -d --name verdverm.com-flask \
	--link verdverm.com-psql:vvdb \
	-v $(pwd):/src \
	-p 5000:5000 \
	-e DATABASE_URL="postgresql://$db_user:$db_pass@vvdb/$db_name" \
	verdverm/verdverm.com-flask

