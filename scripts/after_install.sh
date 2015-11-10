#!/usr/bin/env bash

sudo chown -R ec2-user. /home/ec2-user/open_fmri
sudo yum-config-manager --enable epel
sudo yum install -y docker apg
# docker-compose is not in our repositories so we need to download it
sudo sh -c 'curl -L https://github.com/docker/compose/releases/download/1.5.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose'
sudo chmod +x /usr/local/bin/docker-compose

# lets add ec2-user to docker group to let docker-compose calls succeed
sudo usermod -aG docker ec2-user

exec sudo su -l $USER
cd /home/ec2-user/open_fmri

# when docker is installed it sets its self to start in init.d on boot but it 
# may not be running yet.
sudo /etc/init.d/docker start

# generate self signed certs used by nginx
sudo openssl req -x509 -nodes -newkey rsa:2048 -subj "/C=US/ST=/L=/O=/CN=" -keyout ./nginx.key -out ./nginx.crt
chown ec2-user. nginx.key nginx.crt

# use apg to generate a password and write it plain text to a file in our home 
# directory and then use it to generate a htpasswd file. Password protection is
# just a deterent from the site being wandered upon right now. For actual 
# security with have proper logins setup in Django
PASS=$(apg -n 1)
sudo echo $PASS > ../.user_pass
sudo htpasswd -nb admin $PASS > ./.htpasswd

# set up environment variables used by docker
sudo mv env_example .env
sudo sed -i 's/postgres_pass/$(apg -n 1 -m 100)/g' .env
sudo sed -i 's/secret_key/$(apg -n 1 -m 100)/g' .env

