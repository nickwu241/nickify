#!/bin/sh

ssh $(terraform output ip) 'cd ~/nickify && \
    pipenv install && \
    pipenv run CLARIFAI_API_KEY="$CLARIFAI_API_KEY" ./app.py'
