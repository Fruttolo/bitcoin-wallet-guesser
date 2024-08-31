#!/bin/bash
echo "Starting the application"

cd /home
apt update
apt install -y python3
apt install -y pip
pip install -r requirements.txt
python3 main.py $1
