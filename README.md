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
2. implement the interface.py, with sqlalchemy
3. battle for insert speed, query speed, database size

# running
```sh
docker-compose -f src/example/docker-compose.yml down \
&& docker-compose -f src/example/docker-compose.yml up -d \
&& pytest -s tests/test_example.py \
&& docker-compose -f src/example/docker-compose.yml down
```