
FROM ubuntu:xenial

RUN \
 apt-get update; \
 apt-get install curl -y; \
 curl -sSL 'http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x8AA7AF1F1091A5FD' | apt-key add - \
 && echo "deb [arch=amd64] http://repo.sawtooth.me/ubuntu/bumper/stable xenial universe" >> /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y -q \
    apt-transport-https \
    build-essential \
    ca-certificates \
    python3-sawtooth-sdk \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

EXPOSE 4004/tcp

WORKDIR /project/notary/pyprocessor
ENV PATH "$PATH:/project/notary/pyprocessor"

CMD bash -c 'python3 ./notary_tp.py'
