#!/bin/bash
cd $(dirname $(dirname $(readlink -f $0)))
source venv/bin/activate
pip install --upgrade pip
pip install wheel
pip install -r requirements-frozen.txt
python3 manage.py compilemessages
python3 manage.py collectstatic --noinput
python3 manage.py migrate
/usr/bin/systemctl --user restart status.service
