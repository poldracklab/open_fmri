FROM ubuntu:trusty

# Install opensmtpd
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive  apt-get install -y opensmtpd \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# The spool should be a volume
VOLUME [ "/var/spool/smtpd" ]

# Expose the mail port
EXPOSE 25

# Run the smtpd server in the foreground
CMD [ "/usr/sbin/smtpd", "-d" ]
