#!/bin/sh

IMG=quanta-accounthist-api:`git log -1 --format=%h`
echo building $IMG
docker build -t $IMG .
docker tag $IMG quantalabs/$IMG
docker push quantalabs/$IMG