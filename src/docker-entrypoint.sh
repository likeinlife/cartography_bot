#!/bin/sh

if [ "$DEV_MODE" = "False" ]; then
      echo "RELEASE MODE"
else
      echo "DEBUG MODE"
fi

python main.py