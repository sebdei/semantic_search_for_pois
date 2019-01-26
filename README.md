# Semantic Recommendations for Points of Interests

This is a docker-compose setup that currently contains a Postgres service and a Python environment.

To run the docker containers, you need to [install Docker](https://docs.docker.com/install/) (including docker-compose) and start the Docker daemon. Then, open this folder in the command line run the following commands:

```{sh}
docker-compose build
docker-compose up -d
```

Afterwards, the API is available at ```localhost:5000``` and the Frontend at ```localhost:8080```. The database is initialized with some sample data for Points of Interest and ratings.

The default credentials for the database are admin/admin. The Postgres database is exposed at port 5433 (and available at port 5432 within the containers).

To connect to PostgreSQL from the host system:

```{sh}
psql -h localhost -p 5433 -U admin -W
```

You can also use the [pgAdmin tool](https://www.pgadmin.org) to access the database and inspect the data.
