#!/usr/bin/env bash
export IS_DEBUG=${DEBUG:-false}
#exec gunicorn -b :${PORT:-5000} --access-logfile - --error-logfile - run:application
#Changed at the final step deployment of aws
exec gunicorn --bind 0.0.0.0:5000 --access-logfile - --error-logfile - run:application