import socket


host = '192.168.0.188'
port = 1020
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

client.send('')
client.recv(1)
client.close()
