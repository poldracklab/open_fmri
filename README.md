## OpenfMRI
[![Circle CI](https://circleci.com/gh/poldracklab/open_fmri.svg?style=shield)](https://circleci.com/gh/poldracklab/open_fmri)
[![Coverage Status](https://coveralls.io/repos/poldracklab/open_fmri/badge.svg?branch=master&service=github)](https://coveralls.io/github/poldracklab/open_fmri?branch=master)
### Docker Usage
env_example will need to be renamed to .env. The Posgres environment variables
are used both by the uwsgi and postgres container. The postgres container will
use them to initialize a database and user password, while the uwsgi container
uses them for authentication against the postgres server.

Once that is in place standard docker-compose commands can be used to build and
start the project:
```
$docker-compose build
$docker-compose up
```

