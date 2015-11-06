## OpenfMRI
[![Circle CI](https://circleci.com/gh/poldracklab/open_fmri.svg?style=shield)](https://circleci.com/gh/poldracklab/open_fmri)
[![Coverage Status](https://coveralls.io/repos/poldracklab/open_fmri/badge.svg?branch=master&service=github)](https://coveralls.io/github/poldracklab/open_fmri?branch=master)

### Nginx Configuration
The nginx.conf and docker-compose.yml expects a couple of files to exist that 
are not in the repo. A self signed signature will need to be generated, the 
following command assumes you are in the project's base directory:

'''
sudo openssl req -x509 -nodes -newkey rsa:2048 -keyout ./nginx.key -out ./nginx.crt
'''

Next is the htpasswd file that provides password protection for the site: 
'''
htpasswd -n a_user > ./.htpasswd
'''

Alternatively the auth lines in nginx conf can be removed with out affecting 
the project. Two lines that can be removed are:
'''
            auth_basic "";
            auth_basic_user_file /etc/nginx/.passwd;
'''


### Docker Usage
env_example will need to be renamed to .env. The Posgres environment variables
are used both by the uwsgi and postgres container. The postgres container will
use them to initialize a database and user password, while the uwsgi container
uses them for authentication against the postgres server. It is recommended 
that the postgres password and secret_key values be changed.

Once that is in place standard docker-compose commands can be used to build and
start the project:
```
$docker-compose build
$docker-compose up
```

There is no administrative user created by default so one will need to be 
generated:
```
docker-compose run uwsgi python /app/manage.py createsuperuser
```

### Email settings
In env_example there are the 4 main email environment variables used by the 
project. When these are set in .env they should not have quotation marks 
around them. The only other additional settings that may need to be set are 
either EMAIL_USE_SSL or EMAIL_USE_TLS. These are both set to false by default 
and can be set to True in the Django settings file being used depending on the 
configuration of the SMTP server being sent through.

### Contact Form
The contact form relies on the MANAGERS setting in the Django settings file 
being used. MANAGERS should be set equal to an array of tuples containing the
name and email address that contact form mail should be sent to:

```
MANAGERS = (
    ("test name", "test@example.org), 
    ("test name jr.", "testjr@example.com)
)
```
