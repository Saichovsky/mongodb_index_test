# mongodb_index_test
Testing TTL indices on MongoDB
___
With services running, docker exec into the shell (`mongosh -u <username> -p [<password>]`) to connect to the MongoDB instance and add the TTL index to existing collections thus:

```JS
use testdb;
db.your_collection.createIndex(
  { registered_at: 1 },
  { expireAfterSeconds: 3600 } // expires items whose registered_at is older than 1 hour
)
```

[seed_script.py#L38](https://github.com/Saichovsky/mongodb_index_test/blob/d07be6830d73fc762897997635b95ef95752cb5a/seed_script.py#L38) does this same thing for new data so that it has a TTL by default.
___
The environment variable `SEEDER_COLLECTIONS_TTL_SEC` can be used to set the TTL for all collections created by the script and has the highest priority over the `--ttl` option. A value of 0 for this variable disables the TTL. If neither the variable nor the option is set, the default TTL is 1 year. Same applies to the `SEEDER_COLLECTIONS_NUM_RECORDS` variable.
___
Access the frontend at http://localhost:8081
