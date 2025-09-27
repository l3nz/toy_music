#! /bin/bash

SD=./_sampledir

rm -rf ${SD}

mkdir ${SD}
mkdir ${SD}/x
mkdir ${SD}/y


touch ${SD}/a.mp3
touch ${SD}/b.mp3
touch ${SD}/x/c.mp3
touch ${SD}/y/d.mp3


tree ${SD}