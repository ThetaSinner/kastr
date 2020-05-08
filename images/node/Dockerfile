FROM node:14-buster

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        dos2unix \
        inotify-tools

WORKDIR /scripts
COPY dev-server.sh ./

RUN chmod +x dev-server.sh \
    && dos2unix -n dev-server.sh dev-server.sh

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt update \
    && apt install --no-install-recommends yarn

RUN yarn global add nodemon

ENTRYPOINT ["/bin/bash", "dev-server.sh"]
