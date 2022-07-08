#!/bin/bash

echo "Cleaning dist"
rm -rf dist/*

echo "Copying statics"
cp -r src/static dist/

FLASK_SKIP_DOTENV=1 FLASK_ENV=development FLASK_APP=src/app.py flask generate_static_html --directory dist

