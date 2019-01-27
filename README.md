# Semantic Recommendations for Points of Interest

## General

This project contains a recommendation system for Points of Interest in Berlin. It is based on semantic analysis on the Points of Interest with a document embedding model as a content-based recommender, as well as a collaborative filtering recommender for when users have rated a sufficient amount of places. All software is provided in a Docker-compatible and service-oriented style.

To run the Docker containers, you need to [install Docker](https://docs.docker.com/install/) (including docker-compose) and start the Docker daemon. Then, open this folder in the command line run the following commands:

```{sh}
docker-compose build
docker-compose up -d
```

Afterwards, the API is available at [localhost:5000](http://localhost:5000) and the Frontend at [localhost:8080/dist](http://localhost:8080/dist). The database is initialized on the start of the backend with some sample data for Points of Interest and ratings. For using the frontend, the [Google Chrome](https://www.google.com/intl/en/chrome/) browser is recommended.

## Docker

In the case of the recommender (backend service), the local folder is bound to the container such that the following command is sufficient to restart the server when changes were made to the code:

```{sh}
docker-compose restart recommender
```

In order to view the logs of any Docker container, you can issue the following command, replacing **ContainerID** by the ID of the container you want to inspect:

```{sh}
docker logs -tf ContainerID
```

The ContainerID for any running Docker container can be found by executing the ```docker ps``` command. The backend service has the name _recommender_, while the frontend service is called _frontend_.

## Database

The default credentials for the database are admin/admin. The Postgres database is exposed at port 5433 (and available at port 5432 within the containers).

To connect to PostgreSQL from the host system:

```{sh}
psql -h localhost -p 5433 -U admin -W
```

You can also use the [pgAdmin tool](https://www.pgadmin.org) to access the database and inspect the data.
