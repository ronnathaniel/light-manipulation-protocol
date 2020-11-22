
from sys import argv
from socket import (
    socket,
    AF_INET as address_family,
    SOCK_DGRAM as datagram
)
import struct


class LightBulb:
    def __init__(self):
        self.status = 0
        self.color = None

    def turn_on(self, color):
        self.color = color

    def turn_off(self):
        self.__init__()

    def is_on(self):
        return bool(self.status)


def get_args():
    try:
        host = argv[1]
        port = int(argv[2])

        return host, port
    except IndexError:
        print('\nUsage: python3 light-server.py <HOST-IP> <PORT: int>  \n')
        quit(1)


def serve_and_listen(server_s):

    req_fmt = 'hhihh32s'
    res_fmt = 'hhihh32s32s'

    while 1:
        data, address = server_s.recvfrom(1024)
        print(f'recieved from {address[0]}:{address[1]}')

        request = struct.unpack(req_fmt, data)


"""
def handle_dns_requests (server):

    table = _create_dns_table()

    while 1:
        pack_fmt = 'hhihh32s'

        data, address = server.recvfrom(1024)
        print(f'recieved from {address[0]}:{address[1]}')

        request = struct.unpack(pack_fmt, data)
        response = list(request)

        question = request[-1].decode('utf8')

        host = question.split(' ')[0]
        answer = table.get(host, '')
        if answer:
            answer = answer.get('ip')

        response[0] = 2  # message type reponse
        response[1] = 0 if answer else 1  # return code
        response[4] = len(answer)

        answer = bytes(answer, encoding='utf8')
        response.append(answer)
        response = struct.pack(pack_fmt + '32s', *response)

        print(f'sending to {address[0]}:{address[1]}\n')
        server.sendto(response, address)
"""

def main ():
    host, port = get_args()
    server = socket(address_family, datagram)
    server.bind((host, port))

    print(f'server listening on {host}:{port}\n')
    # handle_dns_requests(server)


main()
