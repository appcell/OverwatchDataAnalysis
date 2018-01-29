# coding: utf-8
"""
@Author: vega13
"""
import socket
import json


def client(host='www.baidu.com', port=80):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = socket.gethostbyname(host)
    s.connect((ip, port))
    message = "GET / HTTP/1.1\r\n\r\n".encode()
    s.sendall(message)

    reply = s.recv(4096)
    data = reply.split('\r\n\r\n')[1]
    return data


def json_request():
    # data = client()
    # json_data = json.loads(data)
    json_data = {'name': 'ORA OWL', 'current_version': 0.1}
    return json_data


def main():
    data = client()

if __name__ == '__main__':
    main()
