#!/bin/bash

cp ../pyStudy.service ../../../../../etc/systemd/system

sed -i "s/^current_version:.*/current_version: 0.0.1/" config.yaml

systemctl daemon-reload