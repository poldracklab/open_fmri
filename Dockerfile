FROM python:3.5

ENV PYTHONUNBUFFERED 1

#RUN groupadd -r open_fmri && useradd --create-home --home-dir /home/open_fmri -r -g open_fmri open_fmri
#USER open_fmri
#WORKDIR /home/open_fmri

RUN apt-get update && apt-get install -y postgresql-client

# Requirements have to be pulled and installed here, otherwise caching won't work
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
