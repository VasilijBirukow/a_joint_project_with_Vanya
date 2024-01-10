#!/bin/bash

cd /root/pyBots/a_joint_project_with_Vanya || exit

git stash
git pull
git stash drop

python3.11 -m pip install --upgrade pip
pip install -r requirements.txt

current_version=$(grep -oP '### Version \K(\d+\.\d+\.\d+)' changelog.md | head -1)

sed -i "s/^current_version:.*/current_version: $current_version/" config.yaml