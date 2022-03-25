#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

set -x

cd $(dirname $(dirname $(readlink -f $0)))

export BRANCH_NAME=$1

systemctl --user disable gunicorn@$BRANCH_NAME.service gunicorn@$BRANCH_NAME.socket

systemctl --user stop gunicorn@$BRANCH_NAME.socket
systemctl --user stop gunicorn@$BRANCH_NAME.service
/usr/bin/dropdb $BRANCH_NAME
