#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

set -x
cd $(dirname $(dirname $(readlink -f $0)))
~/venv/bin/pip3 install -U wheel
~/venv/bin/pip3 install -U pip
~/venv/bin/pip3 install -r requirements-frozen.txt
~/venv/bin/python3 manage.py compilemessages --ignore=.venv
~/venv/bin/python3 manage.py collectstatic --noinput
~/venv/bin/python3 manage.py migrate
/usr/bin/sudo /bin/systemctl restart portal.target
