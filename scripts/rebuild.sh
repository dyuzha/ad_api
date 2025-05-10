#!/bin/bash

docker stop aac && docker rm aac

./build.sh && ./run.sh
