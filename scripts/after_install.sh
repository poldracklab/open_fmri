#!/usr/bin/env bash

project_path=/home/ec2-user/open_fmri/

# generate self signed certs used by nginx
if [ ! -e ${project_path}nginx.key ] || [ ! -e ${project_path}nginx.crt ]
    then
        sudo openssl req -x509 -nodes -newkey rsa:2048 -subj "/C=US/ST=/L=/O=/CN=/" -keyout ${project_path}nginx.key -out ${project_path}nginx.crt
fi

sudo chown -R ec2-user. ${project_path}

sudo yum-config-manager --enable epel
sudo yum install -y docker apg httpd-tools
# docker-compose is not in our repositories so we need to download it
sudo sh -c 'curl -L https://github.com/docker/compose/releases/download/1.5.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose'
sudo chmod +x /usr/local/bin/docker-compose

# lets add ec2-user to docker group to let docker-compose calls succeed
sudo usermod -aG docker ec2-user

cd ${project_path}

# when docker is installed it sets its self to start in init.d on boot but it 
# may not be running yet.
sudo /etc/init.d/docker start

if [ ! -e ${project_path}.htpasswd ]
    then
        touch ${project_path}.htpasswd
fi

# set up environment variables used by docker
if [ ! -e ${project_path}.env ]
    then
        sudo mv ${project_path}env_example ${project_path}.env
        sudo sed -i "s/postgres_pass/$(apg -n 1 -m 100)/g" ${project_path}.env
        sudo sed -i "s/secret_key/$(apg -n 1 -m 100)/g" ${project_path}.env
fi
