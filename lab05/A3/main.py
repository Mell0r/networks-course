import socket
import base64
import ssl
import sys

sender = sys.argv[1]
password = sys.argv[2]
receiver = sys.argv[3]
subject = sys.argv[4]
message_text = sys.argv[5]
image_path = sys.argv[6]
with open(image_path, 'rb') as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('smtp.mail.ru', 587))
print(client_socket.recv(1024).decode())
client_socket.sendall(f'EHLO localhost\r\n'.encode())
print(client_socket.recv(1024).decode())
client_socket.sendall(b"STARTTLS\r\n")
print(client_socket.recv(1024).decode())

with ssl.wrap_socket(sock=client_socket, ssl_version=ssl.PROTOCOL_SSLv23) as ssl_socket:
    ssl_socket.write(b"EHLO localhost\r\n")
    print(ssl_socket.recv(1024).decode())
    ssl_socket.sendall(b'AUTH LOGIN\r\n')
    print(ssl_socket.recv(1024).decode())
    ssl_socket.sendall(base64.b64encode(sender.encode()) + b'\r\n')
    print(ssl_socket.recv(1024).decode())
    ssl_socket.sendall(base64.b64encode(password.encode()) + b'\r\n')
    print(ssl_socket.recv(1024).decode())
    ssl_socket.sendall(f'MAIL FROM: <{sender}>\r\n'.encode())
    print(ssl_socket.recv(1024).decode())
    ssl_socket.sendall(f'RCPT TO: <{receiver}>\r\n'.encode())
    print(ssl_socket.recv(1024).decode())
    ssl_socket.sendall(b'DATA\r\n')
    print(ssl_socket.recv(1024).decode())
    message = f'From: {sender}\r\nTo: {receiver}\r\nSubject: {subject}\r\n' + \
              f'Content-Type: multipart/mixed; boundary="boundary"\r\n\r\n' + \
              f'--boundary\r\n' + \
              f'Content-Type: text/plain\r\n\r\n{message_text}\r\n\r\n' + \
              f'--boundary\r\n' + \
              f'Content-Type: image/jpeg\r\nContent-Transfer-Encoding: base64\r\n' + \
              f'Content-Disposition: attachment; filename="{image_path}"\r\n\r\n{image_base64}\r\n' + \
              f'--boundary--\r\n'
    ssl_socket.sendall(message.encode())
    ssl_socket.sendall(b'\r\n.\r\n')
    print(ssl_socket.recv(1024).decode())
    ssl_socket.sendall(b'QUIT\r\n')

client_socket.close()
print('Email sent successfully!')