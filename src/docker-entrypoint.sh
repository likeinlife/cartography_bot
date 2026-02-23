#!/bin/sh

if [ "$DEV_MODE" = "False" ]; then
  echo "RELEASE MODE"
else
  echo "DEBUG MODE"
fi

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

exec python main.py
