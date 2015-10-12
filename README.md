## OpenfMRI
[![Circle CI](https://circleci.com/gh/poldracklab/open_fmri.svg?style=shield&circle-token=5048fdedd36bd9104ab925cc9b1848c66a79b0b7)](https://circleci.com/gh/poldracklab/open_fmri)
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

