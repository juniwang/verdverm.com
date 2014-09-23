verdverm.com
============

my homepage


### Setup

```
git clone https://github.com/verdverm/verdverm.com

cd verdverm.com/deploy/dockers
./build.sh

cd ..
./runlocal.sh

./managedb.sh db init
./managedb.sh db migrate
./managedb.sh db upgrade
./managedb.sh dbfill
./managedb.sh assets build
```

You can now open `localhost:5000`

### While developing

Run `./managedb.sh assets watch` to keep the css/js up-to-date.


### Destroy EVERYTHING

If you need or want to remove everything

```
# stop the dockers
./stoplocal.sh

# remove the migrations
cd verdverm.com/site
sudo rm -rf migrations

# remove the local database files
cd verdverm.com
sudo rm -rf storage

```
