FROM node:14-buster

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        dos2unix \
        inotify-tools

WORKDIR /scripts

COPY dev-server.sh ./
RUN chmod + dev-server.sh \
    && dos2unix -n dev-server.sh dev-server.sh

ENTRYPOINT ["/bin/bash", "/scripts/dev-server.sh"]
