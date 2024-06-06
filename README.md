# performance-hs-db
the objective of this repostory is to test the performance of database schema design & queries.

# requirements
- linux (WSL/debian/ubuntu)
    - https://learn.microsoft.com/en-us/windows/wsl/install#install-wsl-command
- docker / docker desktop
    - https://www.docker.com/products/docker-desktop/
- python
- IDE
    - https://code.visualstudio.com/Download
    - if you have vscode you can type `code .` in the terminal to open vscode in the current directory, this works great in WSL.

# Setup
1. Create fork of primary repo
2. Download a clone of the forked repo `git clone <your github repo path url>`
3. Open a terminal to your cloned repo
4. follow linux sections for further setup

## Linux
## Install make, venv, pip
in WSL or debian based distributions
```sh
sudo apt install make
sudo apt install python3-venv
sudo apt install python3-pip
```
###  What is Make
use the make command with an action when developing on linux. think of actions as a list of predefined commands to help simplify common development routines.
view avaiable actions
`make help` to see all avaiable actions
### What is python pip
pip is the package repository for python, and allows us to download (opensource) packages.
###  What is venv
venv or virtual environment allow us to create a virtual environment for python, this way we do not have conflicting packages with linux or other code running on your device.

## Repository structure
example structure
```sh
├── src
│   ├── __init__.py
│   ├── database.py
│   ├── datamodel.py
│   ├── interface.py
│   ├── example
│   │   ├── main.py
│   │   └── mysql
│   │       ├── Dockerfile
│   │       └── docker-entrypoint-initdb.d
│   │           ├── 00_init.sql
│   │           └── 01_custom.sql
├── tests/
│   ├──__init__.py
│   ├── conftest.py
│   ├──test_example.py
```
- in `src/` you'll find most of the code
- in `tests/` you'll find the code for the tests
- `src/database` you'll find the database, engine en session factory, used to connect to the database
- `src/datamodel` you'll find the datamodel that you will receive and are expected to return in the benchmark
- `src/interface` you'll find the abstract base class with the functions that you need to implement and that will be tested.
- `src/example/` this is an example benchmark implementation, here you'll find the code that you need to modify for your benchmark implementation.
- `src/example/main.py` this is an example benchmark implementation, of the interface.
- `src/example/mysql/` this is the directory with all the code for the mysql database used in your benchmark
- `src/example/mysql/Dockerfile` the dockerfile used in the example implementation, you should not change this
- `src/example/mysql/docker-entrypoint-initdb.d/` the init directory is run on initialization of the database, sql files will be run in order that you see in the directory
- `src/example/mysql/docker-entrypoint-initdb.d/00_init.sql` the first sql file that will be run during initialization of the database, this will create the database schema `playerdata` you should not change this.
- `src/example/mysql/docker-entrypoint-initdb.d/01_custom.sql`, the second sql file that will be run, please modify this file with a unique schema that you think is more performant.
### setting up your own benchmark implementation
1. copy the src/example to your desired contributions name `cp -r src/example src/<name>`
2. create your schema in `src/<>/mysql/01_custom.sql`
3. implement your schema with our interface `BenchmarkABC`
    - please consider only using the sqlalchemy query builder or raw sql with parameters.
3. battle for insert speed, query speed, database size


# running a benchmark
you'll have to change the paths for the docker compose & pytest file
```sh
docker compose -f src/example/docker-compose.yml down \
&& docker compose -f src/example/docker-compose.yml up -d \
&& pytest -s tests/test_example.py \
&& docker compose -f src/example/docker-compose.yml down
```