from socket import *
import wolfssl
import os
CA_CERTFILE = os.path.expanduser("~/fts/certs/server-cert.pem")
HOST = '127.0.0.1'
PORT = 50000

sock = socket(AF_INET, SOCK_STREAM,0)
context = wolfssl.SSLContext(wolfssl.PROTOCOL_TLSv1_2)
#How to ignore client verify ?
# context.verify_mode = wolfssl.CERT_NONE
context.load_verify_locations(capath=CA_CERTFILE)

secure_socket = context.wrap_socket(sock)
# secure_socket = wolfssl.wrap_socket(sock)
secure_socket.connect((HOST,PORT))
if secure_socket is not None:
     print('TLS connection is established')
filename = input('Input filename to receive: ')
# reqest the server to send a file named filename
secure_socket.write(filename.encode())

filedata = b''
while True:
     data = secure_socket.recv()
     if not data:
          break
     filedata += data

print(filedata.decode())
# ファイルの文字数がサーバー側とクライアント側の両方で一致するか確認する (TLSだと何故か一致しない)
# print('Word count of', filename,':', len(filedata))
# write to file
with open(filename, 'w+') as f:
        print(filedata.decode(), file=f, )

secure_socket.close()
sock.close()

