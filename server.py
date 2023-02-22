import datetime
import signal
import socket
import struct
import sys

def signal_handler(signal, frame):
    print("\nStopping server and closing connections...")
    server_sock.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

host = '192.168.0.103'
port = 9999

BUF_SIZE = 4
server_sock = socket.socket(socket.AF_INET)
server_sock.bind((host, port))
server_sock.listen(2)

while True:
    print("기다리는 중")
    client_sock, addr = server_sock.accept()

    print('Connected by', addr)
    while True:
        # int 형 데이터 받기
        data = b''
        while len(data) < BUF_SIZE:
            packet = client_sock.recv(BUF_SIZE - len(data))
            if not packet:
                break
            data += packet
        if not data:
            break
        int_data = struct.unpack('i', data)[0]
        print(f"Received data: {int_data}")
        now = datetime.datetime.now()
        print("현재 시간:", now)

        # 클라이언트에 데이터 보내기
        client_sock.sendall(struct.pack('i', int_data))

    client_sock.close()

server_sock.close()