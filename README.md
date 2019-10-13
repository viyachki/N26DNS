# Python DNS proxy 
Simple Python proxy for to translate tcp or udp DNS request to TCP over TLS 

Docker details: 
1) To build run: 
    - docker build -t pydnsproxy .
2) To run:
    - sudo docker run --rm -d -p 53:53/tcp -p 53:53/udp pydnsproxy
 
