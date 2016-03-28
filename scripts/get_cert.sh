#! /bin/bash
# taken and slightly modified from https://www.metachris.com/2015/12/comparison-of-10-acme-lets-encrypt-clients/

# Create a directory for the keys and cert
DOMAIN=openfmri.org
mkdir -p /etc/letsencrypt/$DOMAIN
cd /etc/letsencrypt/$DOMAIN

# backup old key and cert
cp nginx.key{,.bak.$(date +%s)}
cp nginx.crt{,.bak.$(date +%s)}

# Generate a private key
openssl genrsa 4096 > account.key

# Generate a domain private key (if you haven't already)
openssl genrsa 4096 > nginx.key

# Create a CSR for $DOMAIN
openssl req -new -sha256 -key nginx.key -subj "/CN=$DOMAIN" > domain.csr

# Create the challenge folder in the webroot
mkdir -p /var/www/.well-known/acme-challenge/

# Get a signed certificate with acme-tiny
python /opt/acme-tiny/acme_tiny.py --account-key ./account.key --csr ./domain.csr --acme-dir /var/www/.well-known/acme-challenge/ > ./signed.crt

wget -O - https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem > intermediate.pem
cat signed.crt intermediate.pem > nginx.crt
