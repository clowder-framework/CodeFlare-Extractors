#!/bin/bash

# no sudo for mac Docker, yes sudo for linux.
echo "Starting Clowder with extractors"
if [ $(uname) = "Darwin" ]; then
    echo "Platform is MacOS"
    docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
    echo "🌐 Starting Clowder (http://localhost:8000) in your default browser"
    open http://localhost:8000
    echo "❓ It may take up to a minute for the containers to start up, please try refreshing the page a few times."

elif [ $(uname -r | grep -c "microsoft") -eq 1 ]; then
    echo "Platform is WSL2"
    sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
    echo "🌐 Starting Clowder (http://localhost:8000) in your default browser"
    wslview http://localhost:8000
    echo "❓ It may take up to a minute for the containers to start up, please try refreshing the page a few times."

elif [ $(uname) = "Linux" ]; then
    echo "Platform is Linux"
    sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
    echo "🌐 Starting Clowder (http://localhost:8000) in your default browser"
    if ! which xdg-open > /dev/null; then
        sudo apt install xdg-utils -y
    fi
    xdg-open http://localhost:8000
    echo "❓ It may take up to a minute for the containers to start up, please try refreshing the page a few times."
fi