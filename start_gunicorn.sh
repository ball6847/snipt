#!/usr/bin/env bash

cd "$(dirname $0)"

NAME="snipts-gunicorn"
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE="settings"
DJANGO_WSGI_MODULE="wsgi_handler"
BIND_ADDR="127.0.0.1:8599"
#BIND_ADDR="27.254.62.218:8599"

if [[ $VIRTUAL_ENV = "" ]]; then
    VIRTUAL_ENV="venv"
    source "$VIRTUAL_ENV/bin/activate"
fi

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$PWD:$PYTHONPATH

#SOCKFILE="/var/run/snipts.gunicorn.sock"

# Create the run directory if it doesn't exist
#RUNDIR="$(dirname $SOCKFILE)"
#test -d $RUNDIR || mkdir -p $RUNDIR

#echo "starting gunicorn using unix socket: $SOCKFILE"

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec "$VIRTUAL_ENV/bin/gunicorn" "$DJANGO_WSGI_MODULE:application" \
    --name $NAME \
    --workers $NUM_WORKERS \
    --log-level=debug \
    --bind=$BIND_ADDR
