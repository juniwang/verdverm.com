verdverm.com
============

my homepage


### Setup

```
git clone https://github.com/verdverm/verdverm.com

cd verdverm.com
mkdir -p tmp/postgresql

cd deploy/docker
./build.sh

cd ..
./runlocal.sh

./managedb.sh db init
./managedb.sh db migrate
./managedb.sh db upgrade
./managedb.sh dbfill
```

You can now open `localhost:5000`
