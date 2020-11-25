
from sys import argv
from socket import (
    socket,
    AF_INET as address_family,
    SOCK_DGRAM as datagram
)
import struct
debug = False

class LightBulb:
    if debug:
        print("lightbulb class here")
    def __init__(self):
        self.color = None

    def turn_on(self, color):
        try:
            self.color = color
            return None
        except Exception as err:
            return err

    def turn_off(self):
        try:
            self.__init__()
            return None
        except Exception as err:
            return err

    def status(self):
        return self.color


def get_args():
    if debug:
        print("get_args starts here")
    try:
        if debug:
            print("get-try starts here")
        host = argv[1]
        port = int(argv[2])

        return host, port
    except IndexError:
        if debug:
            print("get-except starts here")
        print('\nUsage: python3 light-server.py <HOST-IP> <PORT: int>  \n')
        quit(1)


def serve_and_listen(server_s, bulb: LightBulb):
    if debug:
        print("serve/listen starts here")
    req_fmt = 'hhihh64s'
    res_fmt = 'hhihh64s64s'

    while 1:
        if debug:
            print("while 1 starts here")
        data, address = server_s.recvfrom(1024)
        print(f'\nServing Request from {address[0]}:{address[1]}')

        request = struct.unpack(req_fmt, data)

        message_id = request[2]
        op_len = request[3]
        question = request[-1]
        answer_s = 'lightbulb.operation '

        question_s = str(question)
        question_s = question_s.partition(answer_s)[2]
        question_s = question_s[:len(question_s)-1].rstrip(r'\x00').split(' ')


        op_code = int(question_s[0])
        op_color = None
        if len(question_s) > 1:
            op_color = question_s[1]



        if op_code in [1, 2]:
            err = bulb.turn_on(op_color)

            if err is not None:
                answer_s += f'{op_code} FAIL'
            else:
                answer_s += f'{op_code} {"ON" if op_code is 1 else "CHANGE"} SUCCESS'
        elif op_code == 3:
            color = bulb.status()
            if not color:
                answer_s += f'{op_code} FAIL'
            else:
                answer_s += f'{op_code} details: ON {color}'
        elif op_code == 4:
            err = bulb.turn_off()
            if err:
                answer_s += f'{op_code} FAIL'
            else:
                answer_s += f'OFF SUCCESS'



        res = {
            'message_type': 2,
            'return_code': 1 if 'FAIL' in answer_s else 0,
            'message_id': message_id,
            'op_len': len(question_s),
            'result_len': len(answer_s),
            'op': question,
            'res': bytes(answer_s, 'utf-8'),
        }

        packet = struct.pack(res_fmt, *list(res.values()))
        server_s.sendto(packet, address)


def main ():
    if debug:
        print("main starts here")
    host, port = get_args()
    server = socket(address_family, datagram)
    server.bind((host, port))
    # server.settimeout(1)
    bulb = LightBulb()

    print(f'\nServer listening on {host}:{port}\n')
    serve_and_listen(server, bulb)

if debug:
    print("main starts")
main()
if debug:
    print("main ends")