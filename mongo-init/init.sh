#!/bin/bash
set -e

mongoimport --host mongodb --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --db trackerDb --collection trackerConfig --type json --file /docker-entrypoint-initdb.d/init.json --jsonArray
