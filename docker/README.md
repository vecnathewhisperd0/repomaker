# Docker Compose Deployment

This directory serves two purposes
1) It holds utilities used in the docker image
2) It holds example files that you should take into your root folder and modify them: `docker-compose.yml` and `.env` 
``` bash
cp docker/docker-compose.yml docker/.env .
```

Decide on which domain name your repomaker instance will be running.
Then edit your `.env` file:

 - `REPOMAKER_HOSTNAME` Set your hostname, i.e `localhost` or `repomaker.domain.tld`. Using `localhost` will activate debug mode
 - `REPOMAKER_PORT` Leave it as default (80), or set another port if you get a port conflict.
 - `REPOMAKER_SECRET_KEY` Generate a new secret key for your deployment, for example like so:
``` bash
echo "REPOMAKER_SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)"
```

## Database

The docker image supports SQLite, MySQL and Postgres databases. You decide which one you gonna use
by either specifying `REPOMAKER_POSTGRES_DB`, `REPOMAKER_POSTGRES_USER`, `REPOMAKER_POSTGRES_HOST`, and
`REPOMAKER_POSTGRES_PORT`. If you plan to use MySQL then simply replace POSTGRES with MYSQL so you will
define env vars `REPOMAKER_MYSQL_DB`, `REPOMAKER_MYSQL_USER`, `REPOMAKER_MYSQL_HOST`, and
`REPOMAKER_MYSQL_PORT`. The only mandatory one is `REPOMAKER_POSTGRES_DB` or `REPOMAKER_MYSQL_DB`
in order to use the selected database. If you don't specify any of those, a SQLite database will
be created in `${REPOMAKER_BASEPATH}/data/db.sqlite3`.

- Set up the database authentication, or disable it using [`POSTGRES_HOST_AUTH_METHOD=trust`](https://djangoforprofessionals.com/postgresql/#postgresql) in your docker-compose.yml


Then start the docker containers:

```
docker-compose up
```

If everything worked as it should,
there should now be a repomaker instance running on your domain name.
