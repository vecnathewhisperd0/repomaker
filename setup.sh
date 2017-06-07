#!/usr/bin/env bash
set -x
pip3 install -r requirements.txt --user --upgrade --upgrade-strategy only-if-needed && \
python3 manage.py makemigrations maker && \
python3 manage.py migrate && \
echo "All set up, now execute run.sh"

