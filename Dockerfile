FROM registry.gitlab.com/fdroid/ci-images-repomaker:latest
MAINTAINER team@f-droid.org

RUN apt update && \
    apt install -y --no-install-recommends \
    openssh-client netcat gettext postgresql-client \
    apache2 libapache2-mod-wsgi-py3

COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
COPY requirements-gui.txt requirements-gui.txt
COPY debian/requirements.txt debian/requirements.txt

RUN pip3 install -r requirements-gui.txt && \
    pip3 install -r requirements-dev.txt
