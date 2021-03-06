#!/bin/bash

VERSION=$(git rev-parse --short HEAD)
echo "Building and pushing $VERSION"
IMAGE_VERSION="215758104365.dkr.ecr.us-east-1.amazonaws.com/diegorocha:$VERSION"
docker build -t $IMAGE_VERSION --build-arg VERSION_CODE=$VERSION .
docker push $IMAGE_VERSION
VERSION_CODE=$VERSION python manage.py collectstatic --noinput
