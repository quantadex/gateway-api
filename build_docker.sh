#!/bin/sh

IMG=quanta-accounthist-api:`git log -1 --format=%h`
echo building $IMG
docker build -t $IMG .
docker tag $IMG quantalabs/$IMG
docker push quantalabs/$IMG
docker tag $IMG quantalabs/quanta-accounthist-api:latest
docker push quantalabs/quanta-accounthist-api:latest
