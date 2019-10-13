FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y python3.7 ca-certificates
EXPOSE 53
COPY PyDNSProxy.py /
COPY config.ini /
USER root
CMD ["/usr/bin/python3.7", "/PyDNSProxy.py"]