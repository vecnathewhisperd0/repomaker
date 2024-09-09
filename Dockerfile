FROM debian:bullseye
MAINTAINER team@f-droid.org

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE repomaker.settings_docker
ENV REPOMAKER_SECRET_KEY "913d6#u8@-*#3l)spwzurd#fd77bey-6mfs5fc$a=yhnh!n4p9"

WORKDIR /repomaker

ADD . /repomaker

COPY docker/settings_docker.py ./repomaker/
COPY docker/apache.conf /etc/apache2/sites-available/repomaker.conf
COPY docker/wait-for ./
COPY docker/httpd-foreground ./

# Debian setup
ENV LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive
RUN echo Etc/UTC > /etc/timezone \
	&& echo 'APT::Install-Recommends "0";' \
		'APT::Install-Suggests "0";' \
		'APT::Acquire::Retries "20";' \
		'APT::Get::Assume-Yes "true";' \
		'Dpkg::Use-Pty "0";'\
		> /etc/apt/apt.conf.d/99headless \
	&& printf "Package: apksigner libapksig-java\nPin: release a=bullseye-backports\nPin-Priority: 500\n" \
		> /etc/apt/preferences.d/bullseye-backports.pref \
	&& echo "deb https://deb.debian.org/debian/ bullseye-backports main" \
		> /etc/apt/sources.list.d/bullseye-backports.list

# a version of the Debian package list is also in .gitlab-ci.yml
RUN apt-get update && apt-get dist-upgrade && apt-get install \
		apache2 \
		apksigner \
		gettext \
		git \
		gnupg \
		libapache2-mod-wsgi-py3 \
		netcat \
		npm \
		openssh-client \
		python3-babel \
		python3-bleach \
		python3-cryptography \
		python3-dev \
		python3-django-allauth \
		python3-django-compressor \
		python3-django-modeltranslation \
		python3-django-sass-processor \
		python3-dockerpycreds \
		python3-libcloud \
		python3-libsass \
		python3-magic \
		python3-pip \
		python3-psycopg2 \
		python3-qrcode \
		python3-rcssmin \
		python3-rjsmin \
		python3-setuptools \
		python3-websocket \
		python3-webview \
		python3-wheel \
		rsync \
		rclone \
		openjdk-11-jdk \
		s3cmd && \
	apt-get autoremove --purge && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* && \
	cat docker/ssh_config >> /etc/ssh/ssh_config && \
	a2dissite 000-default && \
	a2ensite repomaker && \
	pip3 install -r requirements-dev.txt && \
	npm install && \
	./pre-release.sh


RUN find /repomaker/ -perm -o=w  -exec chmod go-w {} \;
RUN chmod 644 /etc/apache2/sites-available/repomaker.conf
