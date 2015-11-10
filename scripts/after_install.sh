#!/usr/bin/env bash

cd /home/ec2-user/open_fmri
sudo yum install -y docker apg
# docker-compose is not in our repositories so we need to download it
sudo curl -L https://github.com/docker/compose/releases/download/1.5.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose

# when docker is installed it sets its self to start in init.d on boot but it 
# may not be running yet.
sudo /etc/init.d/docker start

# generate self signed certs used by nginx
sudo openssl req -x509 -nodes -newkey rsa:2048 -subj "/C=US/ST=/L=/O=/CN=" -keyout ./nginx.key -out ./nginx.crt

# use apg to generate a password and write it plain text to a file in our home 
# directory and then use it to generate a htpasswd file. Password protection is
# just a deterent from the site being wandered upon right now. For actual 
# security with have proper logins setup in Django
PASS=$(apg -n 1)
echo $PASS > ../.user_pass
htpasswd -nb admin $PASS > ./.htpasswd

# set up environment variables used by docker
mv env_example .env
sed -i 's/postgres_pass/$(apg -n 1 -m 100)/g' .env
sed -i 's/secret_key/$(apg -n 1 -m 100)/g' .env

