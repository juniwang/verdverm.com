#!/bin/bash

docker build $nocache -t verdverm/verdverm.com-flask flask

# nocache="--no-cache"

docker build $nocache -t verdverm/verdverm.com-postgresql postgresql
