FROM debian:stable-slim
COPY entrypoint.sh add_team.sh /
RUN apt-get update && \
    apt install -y wget && \
    wget --output-document=/usr/local/bin/fly  "https://ci.fabric8.ru/api/v1/cli?arch=amd64&platform=linux" && \
    chmod +x /usr/local/bin/fly
ENTRYPOINT ['entrypoint.sh']