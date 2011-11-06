#!/usr/bin/env bash

# Have the whole script fail if any individual command fails.
set -e

# Create the virtual environment and activate it.
virtualenv \
    --python=$(which python2.7) \
    --no-site-packages \
    --prompt="(replaydog) " \
    env
source env/bin/activate

# Install the requirements.

pip install mpyq # for some reason sc2reader won't install properly unless this
                 # is installed before the requirements.txt
pip install -r requirements.txt

# Make the database, if it doesn't exist
python scripts/makedb.py

# Make the directory for storing uploads
mkdir -p uploads
