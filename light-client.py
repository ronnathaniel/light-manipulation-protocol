from sys import argv
from socket import (
    socket,
    AF_INET as address_family,
    SOCK_DGRAM as datagram
)
import struct
from random import randint
debug = False
colour = ''

def get_params():
    global colour
    if debug:
        print("get params starts here")
    try:
        if debug:
            print("get param: try")
        host = argv[1]
        port = int(argv[2])
        address = (host, port)
        op = ' '.join(argv[3:])
        colour = op[32:]
        if debug:
            print("host is %s, port is %s, op is %s, colour is %s" % (host, port, op, colour))
        return dict(address=address, op=op)
    except IndexError:
        if debug:
            print("get param: except")
        print('\nUsage: python3 light-client.py <HOST-IP> <PORT: int> lightbulb.operation <OPCODE> <COLOR> \n')
        quit(1)


def request(client, address, op):
    global colour
    if debug:
        print("request starts here")
    req_fmt = 'hhihh64s'
    res_fmt = 'hhihh64s64s'

    message_id = randint(0, 100)

    data = {
        'message_type': 1,
        'return_code': 0,
        'message_id': message_id,
        'op_len': len(op),
        'result_len': 0,
        'op': bytes(op, 'utf-8'),
    }

    print(f'\nSending Request to {address[0]}:{address[1]}')
    print(f'Message ID: {message_id}')
    print(f'Operation Len: {len(op)}')
    print(f'Result Len: {0}')
    print(f'Operation: {op}')

    if debug:
        print("packing data here")
    packet = struct.pack(req_fmt, *list(data.values()))

    if debug:
        print("sending data here")
    client.sendto(packet, address)
    if debug:
        print("data sent")

    data, address = client.recvfrom(2048)
    if debug:
        print("testing received data")


    response = struct.unpack(res_fmt, data)

    return_code = response[1]
    # answer_s = str(data[-1]).rstrip(r'\x00')
    answer_s = response[-1].decode('utf-8')
    # print(f'\nANSWER - \n{answer_s}\n')

    print(f'\nRecieved Response from {address[0]}:{address[1]}')
    print(f'Return Code: {return_code}')
    print(f'Message ID: {message_id}')
    print(f'Operation Len: {len(op)}')
    print(f'Result Len: {len(answer_s)}')
    print(f'Operation: {op}')
    print(f'Result: {answer_s}')


def main():
    if debug:
        print("Main starts here")
    client = socket(address_family, datagram)
    # client.settimeout(1)
    request(client, **get_params())


main()
if debug:
    print("end of program")