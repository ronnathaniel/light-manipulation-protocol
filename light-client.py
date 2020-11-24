from sys import argv
from socket import (
    socket,
    # timeout as TimeoutException,
    AF_INET as address_family,
    SOCK_DGRAM as datagram
)
import struct
from random import randint


def get_params():
    try:
        host = argv[1]
        port = int(argv[2])
        # address = f'{host}:{port}'
        address = (host, port)

        op = ' '.join(argv[3:6])
        print(op)

        # opcode = int(argv[4])
        # color = None if opcode is 3 else argv[5]

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
        
        
        
        
#Echo Client Side
#Nicolas Oberholtzer NLO2 31371045
import socket
import sys
import time
import random

sequence = 0
send_code = 1
receive_code = 2
noresponse = -1
timeoutVal = 1
return_code = 0

def ping(sock,messageNum,Hostname):
    quest_len = len(Hostname)
    ans_len = 0
    message = bytearray()
    message = send_code.to_bytes(2, byteorder='big')
    message += return_code.to_bytes(2, byteorder='big')
    message += messageNum.to_bytes(4, byteorder='big')
    message += quest_len.to_bytes(2, byteorder='big')
    message += ans_len.to_bytes(2, byteorder='big')
    message += Hostname.encode("utf-8")
    timestart = time.time()
    try:
        sent = sock.sendto(message, server_addr)
        data, server = sock.recvfrom(4096)
        timeend = time.time()
        elapsedtime = timeend - timestart
        messagetype = int.from_bytes(data[0:2], 'big')
        return_val = int.from_bytes(data[2:4], 'big')
        sequence = int.from_bytes(data[4:8], 'big')
        quest_len = int.from_bytes(data[8:10], 'big')
        ans_len = int.from_bytes(data[10:12], 'big')
        ans_start = 12 + quest_len
        ans_end = ans_start + ans_len
        ans_str = data[ans_start:ans_end]
        retval = {'return_value': return_val, 'identifier': sequence, 'time':elapsedtime, 'answer':ans_str.decode("utf-8")}
    except:
        retval = {'time': noresponse}
    return retval

def call_ping(sock, messageNum, Hostname):
    return ping(sock, messageNum, Hostname)

if (len(sys.argv)!=4):
    print("please provide 3 arguments")
    exit()

IP = sys.argv[1]
UDP = int(sys.argv[2])
Hostname = sys.argv[3]
Hostname += " A IN"

# First we create UDP socket
socket.setdefaulttimeout(timeoutVal)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (IP, UDP)
recval = 0
big = 0
small = timeoutVal
avg = 0
i = 0
quest_len = len(Hostname)
seq = random.randint(1, 100)

print('Sending Request to %s, %i' % (IP, UDP))
print('Message ID: %i' % seq)
print('Question Length: %i Bytes' % quest_len)
print('Answer length: 0 Bytes')
print('Question: %s' % Hostname)
print('')

for k in range(3):
    val = call_ping(sock, seq, Hostname)
    if val['time'] != noresponse:
        recval = recval + 1
        break
    else:
        if k != 2:
            print('Request timed out...')
            print('Sending Request to %s, %i' % (IP, UDP))
        else:
            print('Request timed out... Exiting Program')

if val['time'] == noresponse:
    value = -1
    ans_str = ''
    ans_len = 0

else:
    value = val['return_value']
    ans_str = val['answer']
    ans_len = len(val['answer'])
    print('Received Response from %s, %i' % (IP, UDP))
    if value == 0:
        print('Return Code 0, No Errors')
    else:
        print('Return Code 1, Does Not Exist')
    print('Message ID: %i' % seq)
    print('Question Length: %i Bytes' % quest_len)
    print('Answer length: %i Bytes' % ans_len)
    print('Question: %s' % Hostname)
    print('Answer: %s' % ans_str)

sock.close()

"""


def main():
    client = socket(address_family, datagram)
    # client.settimeout(1)
    request(client, **get_params())


main()
