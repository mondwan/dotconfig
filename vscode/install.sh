#!/bin/sh

BASEDIR=$(dirname "$0")

echo "$BASEDIR"

# Split xargs into two different commands as it has a length limitation when
# replacing command argument
paste -d' ' -s "$BASEDIR/packages.txt" | \
    xargs -n1 -I{} sh -c "echo code --install-extension {}"
paste -d' ' -s "$BASEDIR/packages.txt" | \
    xargs -n1 -I{} sh -c "code --install-extension {} || exit 255"
