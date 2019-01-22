# Docker

This is just a naive docker-compose setup that currently only contains a postgres service and a dummy python environment.

To run the docker container, you need to [install Docker](https://docs.docker.com/install/) (including docker-compose) and start the Docker daemon. Then, open this folder in the command line run the following command:

```{sh}
docker-compose up -d
```

Alternatively, it can be started without docker-compose using ```docker stack```:

```{sh}
docker stack up -c docker-compose.yml poi
```

The default credentials are admin/admin. The postgres database is exposed at port 5433.

More info about the postgres Docker image including further documentation can be found [here](https://hub.docker.com/_/postgres/).

As we use docker-compose, this setup can be easily be extended with further services. An exemplary setup with Django can be found [here](https://docs.docker.com/compose/django/), alongside [further sample applications](https://docs.docker.com/samples/#sample-applications).

To connect to PostgreSQL from the command line inside the docker:

```{sh}
psql -h localhost -p 5433 -U admin -W
```

## Connecting to Postgres from Python environment

First install the ```psycopg2``` package (e.g. by executing ```pip install psycopg2```). Then the following code can be executed from within the python container.

```py
import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=admin user=admin password=admin host=db") # db = name of the postgres image in docker-compose.yml

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

# Query the database and obtain data as Python objects
cur.execute("SELECT * FROM test;")
cur.fetchone()
(1, 100, "abc'def")

# Make the changes to the database persistent
>>> conn.commit()

# Close communication with the database
>>> cur.close()
>>> conn.close()
```

Also see the [psycopg2 documentation](http://initd.org/psycopg/docs/usage.html).
