
from sys import argv
from socket import (
    socket,
    timeout as TimeoutException,
    AF_INET as address_family,
    SOCK_DGRAM as datagram
)
import struct
from random import randint



def get_args():
    try:
        host = argv[1]
        port = int(argv[2])
        op_s = argv[3]
        opcode = int(argv[4])
        color = None if opcode is 3 else argv[5]

        return host, port, op_s, opcode, color
    except IndexError:
        print('\nUsage: python3 light-client.py <HOST-IP> <PORT: int> lightbulb.operation <OPCODE> <COLOR> \n')
        quit(1)

def request():
    pass

"""
def dns_lookup(client, table_address, host_name):
    pack_fmt = f'hhihh32s'
    question = f'{host_name} A IN'
    answer = ''
    count = 0
    data = {
        'message_type': 1,  # (16 bit) [1 = request]
        'return_code': 0,  # (16 bit) [0 = request]
        'message_id': randint(0, 100),  # (32 bit) [unique 0-100]
        'question_length': len(question),  # (16 bit)
        'answer_length': 0,  # (16 bit)
        'question': bytes(question, encoding='utf8'),  # (32 bit)
    }
    packed = struct.pack(pack_fmt, *list(data.values()))
    print('\n')

    for count in range(3):
        try:
            print(f'Sending request to - {table_address[0]}:{table_address[1]}')
            print(f'Message ID - {data.get("message_id", 0)}')
            print(f'Question length - {len(question)} bytes')
            print(f'Answer length - {len(answer)} bytes')
            print(f'Question - {question}')
            client.sendto(packed, table_address)

            response, table_address = client.recvfrom(1024)
            print(f'\nRecieved response from {table_address[0]}:{table_address[1]}')
            break

        except TimeoutException:
            print('Request timed out ...\n')

    if count is 2:
        print('Exiting Program. Servers not Responding.\n')
        exit(1)

    response = struct.unpack(pack_fmt + '32s', response)
    question = response[-2].decode('utf8').rstrip('\x00')
    answer = response[-1].decode('utf8').rstrip('\x00')

    print(f'Return Code - {response[1]}  {"(No Errors)" if not response[1] else "(Name does not Exist)"}')
    print(f'Message ID - {response[2]}')
    print(f'Question length - {len(question)} bytes')
    print(f'Question - {question}')

    if answer:
        print(f'Answer length - {len(answer)} bytes')
        print(f'Answer - {answer}')
"""

def main():
    host, port, op_s, opcode, color = get_args()
    client = socket(address_family, datagram)
    client.settimeout(1)
    # dns_lookup(client, (host_dns, port), host_name)


main()
