FROM google/debian:wheezy
MAINTAINER verdverm@gmail.com

# Update stuff
RUN apt-get update

# Install Python Setuptools
RUN apt-get --no-install-recommends install -y python-setuptools build-essential python-dev libpq-dev ca-certificates openssh-server supervisor

# Install pip
RUN easy_install pip

ADD requirements.txt /tmp/requirements.txt

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install requirements.txt
RUN pip install -r /tmp/requirements.txt

# Setup sshd
RUN mkdir /var/run/sshd
RUN echo 'root:root' |chpasswd

RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

EXPOSE 5000
EXPOSE 22

VOLUME ["/src"]
WORKDIR /src

ENTRYPOINT ["/usr/bin/supervisord"]
