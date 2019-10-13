FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive
EXPOSE 53
COPY PyDNSProxy.py /
COPY config.ini /

