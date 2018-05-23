# Docker Compose Deployment

First, copy the files `docker-compose.yml`, `Makefile` and `.env` from this directory:

``` bash
cp docker/docker-compose.yml docker/Makefile docker/.env .
```

Decide on which domain name your repomaker instance will be running.
Then edit your `.env` file:

 - `REPOMAKER_HOSTNAME` Set your hostname, i.e `localhost`, `repomaker.domain.tld`, ...
 - `REPOMAKER_PORT` Leave it as default (80), or set another port if you get a port conflict.
 - `REPOMAKER_SECRET_KEY` Generate a new secret key for your deployment, for example like so:

``` bash
echo "REPOMAKER_SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)"
```

Then install start the docker containers:

```
make
```

If everything worked as it should,
there should now be a repomaker instance running on your domain name (i.e <http://localhost>).


## Makefile commands

When developing, you may need to rebuild assets,
reinstall npm dependencies or python dependencies.

``` bash
# After editing HTML, css or js
make rebuild

# After adding or removing npm deps
make npminstall
make rebuild

# After adding or removing python deps
make rebuild

# After editing Dockerfile
make rebuild_container
make rebuild
```


## Database browser

Go to <http://localhost:5050>, and login with: `postgres` / `admin`
