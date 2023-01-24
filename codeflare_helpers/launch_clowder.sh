#!/bin/bash

# no sudo for mac Docker, yes sudo for linux.
echo "Starting Clowder with extractors"
if [ $(uname) = "Darwin" ]; then
    docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
    echo "🌐 Starting Clowder (http://localhost:8000) in your default browser"
    open http://localhost:8000
    echo "❓ It may take up to a minute for the containers to start up, please try refreshing the page a few times."

elif [ $(uname) = "Linux" ]; then
    sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
    echo "🌐 Starting Clowder (http://localhost:8000) in your default browser"
    xgd-open http://localhost:8000
    echo "❓ It may take up to a minute for the containers to start up, please try refreshing the page a few times."
fi