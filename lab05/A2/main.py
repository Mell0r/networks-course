import socket
import base64
import ssl
import sys

sender = sys.argv[1]
password = sys.argv[2]
receiver = sys.argv[3]
subject = sys.argv[4]
message_text = sys.argv[5]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('smtp.mail.ru', 587))
print(client_socket.recv(1024).decode())
client_socket.sendall(f'EHLO localhost\r\n'.encode())
print(client_socket.recv(1024).decode())
client_socket.sendall(b"STARTTLS\r\n")
print(client_socket.recv(1024).decode())

with ssl.wrap_socket(sock=client_socket, ssl_version=ssl.PROTOCOL_SSLv23) as ssl_socket:
    ssl_socket.write(b"EHLO localhost\r\n")
    ssl_socket.sendall(b'AUTH LOGIN\r\n')
    ssl_socket.sendall(base64.b64encode(sender.encode()) + b'\r\n')
    ssl_socket.sendall(base64.b64encode(password.encode()) + b'\r\n')
    ssl_socket.sendall(f'MAIL FROM: <{sender}>\r\n'.encode())
    ssl_socket.sendall(f'RCPT TO: <{receiver}>\r\n'.encode())
    ssl_socket.sendall(b'DATA\r\n')
    ssl_socket.sendall(f'From: {sender}\r\nTo: {receiver}\r\nSubject: {subject}\r\nContent-Type: text/plain\r\n{message_text}'.encode())
    ssl_socket.sendall(b'\r\n.\r\n')
    ssl_socket.sendall(b'QUIT\r\n')

client_socket.close()
print('Email sent successfully!')