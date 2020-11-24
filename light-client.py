from sys import argv
from socket import (
    socket,
    AF_INET as address_family,
    SOCK_DGRAM as datagram
)
import struct
from random import randint


def get_params():
    try:
        host = argv[1]
        port = int(argv[2])
        address = (host, port)
        op = ' '.join(argv[3:])

        return dict(address=address, op=op)
    except IndexError:
        print('\nUsage: python3 light-client.py <HOST-IP> <PORT: int> lightbulb.operation <OPCODE> <COLOR> \n')
        quit(1)


def request(client, address, op):
    req_fmt = 'hhihh32s'
    res_fmt = 'hhihh32s32s'

    data = {
        'message_type': 1,
        'return_code': 0,
        'message_id': randint(0, 100),
        'op_len': len(op),
        'result_len': 0,
        'op': bytes(op, 'utf-8'),
    }

    packet = struct.pack(req_fmt, *list(data.values()))
    client.sendto(packet, address)

    data, address = client.recvfrom(2048)
    print(data)
    print(address)


def main():
    client = socket(address_family, datagram)
    # client.settimeout(1)
    request(client, **get_params())


main()
