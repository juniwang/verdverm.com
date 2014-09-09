FROM google/debian:wheezy
MAINTAINER verdverm@gmail.com

# Update stuff
RUN apt-get update
RUN apt-get upgrade -y

# Install Python Setuptools
RUN apt-get --no-install-recommends install -y python-setuptools build-essential python-dev

# Install pip
RUN easy_install pip

ADD requirements.txt /tmp/requirements.txt

# Install requirements.txt
RUN pip install -r /tmp/requirements.txt

EXPOSE 5000

VOLUME ["/src"]

CMD python /src/run.py
