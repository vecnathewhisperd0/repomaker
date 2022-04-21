#!/usr/bin/env bash

pylint=pylint
if which pylint3; then
    pylint=pylint3
fi
$pylint --load-plugins=pylint_django --django-settings-module=repomaker.settings_test --disable=C,R,fixme repomaker
