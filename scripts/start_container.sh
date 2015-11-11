#!/usr/bin/env bash

cd /home/ec2-user/open_fmri
/usr/local/bin/docker-compose build
/usr/local/bin/docker-compose up -d
