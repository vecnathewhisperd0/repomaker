#!/usr/bin/env bash

python3 manage.py makemessages --keep-pot --no-wrap --no-location --no-obsolete --ignore node_modules -v 3
python3 manage.py makemessages --keep-pot --no-wrap --no-location --no-obsolete --ignore node_modules -v 3 -d djangojs
python3 manage.py compilemessages

sed -i -e '/^"POT-Creation-Date: /d' locale/*/LC_MESSAGES/django.po
sed -i -e '/^"POT-Creation-Date: /d' locale/*/LC_MESSAGES/djangojs.po

