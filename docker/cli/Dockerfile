FROM python:3.7

ARG SSHKEY_PUB

RUN apt-get update

RUN apt-get install --no-install-recommends -y openssh-server git
RUN mkdir -p /var/run/sshd &&\
    mkdir -p /root/.ssh &&\
    echo "$SSHKEY_PUB" > /root/.ssh/authorized_keys &&\
    chmod 700 /root/.ssh &&\
    chmod 600 /root/.ssh/authorized_keys

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config


RUN apt-get clean &&\
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

WORKDIR "/var/void"

COPY . /var/void

RUN pip install .

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
