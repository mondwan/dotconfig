#!/bin/sh

pkgs=" eslint"
pkgs+=" babel-eslint"
pkgs+=" eslint-plugin-react"
pkgs+=" eslint-config-airbnb"
pkgs+=" eslint-config-eslint"
pkgs+=" grunt-cli"
pkgs+=" bower"

for pkg in ${pkgs}; do
    echo "npm install -g ${pkg}"
    npm install -g ${pkg} || exit 1
done
