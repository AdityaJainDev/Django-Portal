#!/bin/sh
set -euo pipefail
pip3 install pylint==2.14.4 pylint-django pylint-exit astroid
FILES=$(find . -type d -exec test -e '{}/__init__.py' \; -print -prune -o -path './cache_usage_benchmark' -prune -o -name '*.py' -print)
pylint -j 2 --rcfile .pylintrc ${FILES} -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint.txt || pylint-exit $?
