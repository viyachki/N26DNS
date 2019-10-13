from multiprocessing import Process
import socket
import configparser
import ssl 
import threading
import codecs


def convertToUDP(query):
    message = b"\x00"+ codecs.encode(chr(len(query))) + query  # converting the udp query to tcp. Includes \x00 and the size of the query
    return message

def handler(data, addr, socket, DNSserverIP):
    TCPanswer = sendTCPviaSSL(DNSServerIP, data, rport, True)
    if TCPanswer:
        UDPanswer = TCPanswer[2:]
        socket.sendto(UDPanswer, addr)

def sendTCPviaSSL(DNSserverIP, query, rport, udp=False):
    server = (DNSserverIP, rport)
    context = ssl.create_default_context()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock :
        with context.wrap_socket(sock, server_hostname=DNSserverIP) as ssock:
            ssock.connect(server)
            if udp==True:
                dnsquery = convertToUDP(query)
            else: 
                dnsquery = query
            ssock.send(dnsquery)  	
            data = ssock.recv(1024)
    return data

def TCPProcessFunction(DNSServerIP, lport, rport, host):
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysock.bind((host, lport))
    mysock.listen(5)
    while True:           
        connection, info = mysock.accept()
        data, addr = connection.recvfrom(1024)
        connection.send(sendTCPviaSSL(DNSServerIP, data, rport))

def UDPProcessFunction(DNSServerIP, lport, rport, host):
    mysock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mysock.bind((host, lport))
    while True:           
        data, addr = mysock.recvfrom(1024)
        threading._start_new_thread(handler, (data, addr, mysock, DNSServerIP))
        

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.ini')
    DNSServerIP = '1.1.1.1' if len(config['DEFAULT']['DNSServerIP']) == 1 else config['DEFAULT']['DNSServerIP']
    lport = 53 if len(config['DEFAULT']['lport']) == 1 else int(config['DEFAULT']['lport'])
    rport = 853 if len(config['DEFAULT']['rport']) == 1 else int(config['DEFAULT']['rport'])
    host = '' if len(config['DEFAULT']['host']) == 1 else config['DEFAULT']['host']
    

    tcpProcess = Process(target=TCPProcessFunction, args=(DNSServerIP, lport, rport, host))
    udpProcess = Process(target=UDPProcessFunction, args=(DNSServerIP, lport, rport, host))
    tcpProcess.start()
    udpProcess.start()
    tcpProcess.join()
    udpProcess.join()