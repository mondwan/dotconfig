#!/bin/sh

pkgs=" eslint"
pkgs="${pkgs} babel-eslint"
pkgs="${pkgs} eslint-plugin-jsx-a11y@^2.2.3"
pkgs="${pkgs} eslint-plugin-import@^2.1.0"
pkgs="${pkgs} eslint-plugin-react"
pkgs="${pkgs} eslint-config-airbnb"
pkgs="${pkgs} eslint-config-eslint"
pkgs="${pkgs} grunt-cli"
pkgs="${pkgs} bower"
pkgs="${pkgs} phantomjs-prebuilt"

for pkg in ${pkgs}; do
    echo "npm install -g ${pkg}"
    npm install -g ${pkg} || exit 1
done
