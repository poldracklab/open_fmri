FROM python:3.4

ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
ADD ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN apt-get update && apt-get -y install git
RUN git clone https://github.com/CognitiveAtlas/cogat-python
WORKDIR ./cogat-python
RUN python setup.py install
#RUN groupadd -r open_fmri && useradd -r -g open_fmri open_fmri
