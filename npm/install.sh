#!/bin/sh

BASEDIR=$(dirname "$0")

# Split xargs into two different commands as it has a length limitation when
# replacing command argument
paste -d' ' -s "$BASEDIR/packages.txt" | \
    xargs -I{} sh -c "echo npm install -g {}"
paste -d' ' -s "$BASEDIR/packages.txt" | \
    xargs -I{} sh -c "npm install -g {} || exit 255"
