# Docker

This is just a naive docker-compose setup that currently only contains a postgres service. 

To run the docker container, you need to [install Docker](https://docs.docker.com/install/) (including docker-compose) and start the Docker daemon. Then, open this folder in the command line run the following command:

```{sh}
docker-compose -f docker-compose.yml up -d
```

Alternatively, it can be started without docker-compose using ```docker stack```:

```{sh}
docker stack up -c docker-compose.yml poi
```

The default credentials are admin/admin. The postgres database is exposed at port 5433.

More info about the postgres Docker image including further documentation can be found [here](https://hub.docker.com/_/postgres/).

As we use docker-compose, this setup can be easily be extended with further services. An exemplary setup with Django can be found [here](https://docs.docker.com/compose/django/), alongside [further sample applications](https://docs.docker.com/samples/#sample-applications).
