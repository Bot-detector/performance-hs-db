# performance-hs-db
the objective of this repostory is to test the performance of database schema design & queries.

## way of working
example structure
```sh
├── src
│   ├── __init__.py
│   ├── datamodel.py
│   ├── interface.py
│   ├── example
│   │   ├── main.py
│   │   └── mysql
│   │       ├── Dockerfile
│   │       └── docker-entrypoint-initdb.d
│   │           ├── 00_init.sql
│   │           └── 01_custom.sql
```
1. copy the src/example to your desired contributions name `cp -r src/example src/<name>`
2. create your schema in `src/<>/mysql/01_custom.sql`
3. implement your schema with our interface `BenchmarkABC`
    - please consider only using the sqlalchemy query builder or raw sql with parameters.
3. battle for insert speed, query speed, database size


# running a benchmark
you'll have to change the paths for the docker compose & pytest file
```sh
docker-compose -f src/example/docker-compose.yml down \
&& docker-compose -f src/example/docker-compose.yml up -d \
&& pytest -s tests/test_example.py \
&& docker-compose -f src/example/docker-compose.yml down
```