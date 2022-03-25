#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

set -x

cd $(dirname $(dirname $(readlink -f $0)))

export BRANCH_NAME=$1
export MERGE_REQUEST_ID=$2
export DJANGO_SETTINGS_MODULE=Portal.settings_review

echo >.env
echo "MERGE_REQUEST_ID=${MERGE_REQUEST_ID}" >>.env

/usr/bin/dropdb $BRANCH_NAME || true
/usr/bin/createdb $BRANCH_NAME || true
python3 -mvenv .venv
source .venv/bin/activate
pip3 install -U wheel
pip3 install -U pip
pip3 install -r requirements-frozen.txt
python3 manage.py compilemessages --ignore=.venv
python3 manage.py collectstatic --noinput
python3 manage.py migrate
python3 manage.py loaddata user.json

systemctl --user stop gunicorn@$BRANCH_NAME.service gunicorn@$BRANCH_NAME.socket
systemctl --user restart gunicorn@$BRANCH_NAME.socket
systemctl --user restart gunicorn@$BRANCH_NAME.service

systemctl --user enable gunicorn@$BRANCH_NAME.service gunicorn@$BRANCH_NAME.socket
