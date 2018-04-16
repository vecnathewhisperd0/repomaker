all: build_container pipinstall npminstall build run_tasks start logs

build_container:
	docker build .

rebuild_container:
	docker build --no-cache .

pipinstall:
	docker-compose up -d
	docker exec -it repomaker-web bash -c "pip3 install -r requirements.txt"
	docker exec -it repomaker-tasks bash -c "pip3 install -r requirements.txt"
	docker exec -it repomaker-bash bash -c "pip3 install -r requirements.txt"
	docker exec -it repomaker-bash bash -c "pip3 install -r requirements-dev.txt"

npminstall:
	docker-compose up -d bash
	docker exec -it repomaker-bash bash -c "npm install"

build:
	docker-compose up -d bash
	docker exec -it repomaker-bash bash -c "./pre-release.sh"

start:
	docker-compose up -d
	docker exec -it repomaker-web bash -c "a2dissite 000-default && a2ensite repomaker"
	docker exec -dit repomaker-web bash -c "./wait-for db:5432 -- python3 manage.py migrate && ./httpd-foreground"

rebuild: restart_workers pipinstall build start logs

restart_workers:
	docker-compose restart -t 1 web tasks

bash:
	docker-compose up -d bash
	docker exec -it repomaker-bash bash

bash_web:
	docker-compose up -d web
	docker exec -it repomaker-web bash

assets:
	docker exec -it repomaker-bash bash -c "./assets.py"

webserver:
	docker exec -it repomaker-web bash -c "./httpd-foreground"

run_tasks:
	docker exec -dit repomaker-tasks bash -c "./wait-for web:80 -- su - www-data -p -s /bin/bash -c 'cd /repomaker && python3 manage.py process_tasks'"

logs:
	docker-compose logs -ft
