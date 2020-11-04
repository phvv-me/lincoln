#!/usr/bin/env bash

sudo apt-get update -y
git clone https://github.com/phvv-me/lincoln.git .

python3 -m pip install -r requirements.txt
python3 bot/main.py
