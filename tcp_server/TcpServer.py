"""
TODO:
AUTO TEST SCRIPT: MCU & SERVICE
use the struct module to handle binary data.
See https://docs.python.org/3/library/struct.html
"""

import sys
import time
import signal
import socket
import threading


ip = "127.0.0.1"
port = 1020
"""
config = {
    b'1': b'2',
    b'2': b'3'
}
"""
start_byte = b'\xAB'
end_byte = b'\xCD'
config = {

}


def handle_client(client):
    while True:
        pkg = client.recv(1)
        data = b''
        length = b''
        data_len = 0
        i = 1
        if pkg != start_byte:
            print('not the start byte')
            print(pkg)
            client.close()
            return
        while True:
            recv = client.recv(1)
            pkg += recv
            print(recv)
            i += 1
            if 8 <= i <= 9:
                length += recv
                if i == 9:
                    data_len = length.decode('utf-16-be')
            if data_len and 9 < i <= 9+data_len:
                data += recv
            if i == 9+data_len+2:
                break
        print("*********pkg**********")
        print(pkg)
        print("*********data**********")
        print(data)
        print("")
        msg = input("input ack msg or press Enter to use default config: ").strip()
        try:
            if not msg:
                client.send(config[pkg])
            else:
                client.send(bytes(bytearray.fromhex(msg)))
        except:
            pass


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(10)

    def exit(signal_num, sign):
        server.close()
        sys.exit(signal_num)

    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGTERM, exit)

    while True:
        client, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()
        time.sleep(10)


if __name__ == '__main__':
    main()
