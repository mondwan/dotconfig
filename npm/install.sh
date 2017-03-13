#!/bin/sh

BASEDIR=$(dirname "$0")

paste -d' ' -s "$BASEDIR/packages.txt" | \
    xargs -I{} sh -c "echo npm install -g {}; npm install -g {} || exit 255"
