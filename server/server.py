from socket import *
import wolfssl
import sys
import os  #  to get the PATH of home directory
IP = '127.0.0.1'
PORT = 50000

# fts リポジトリが　ホームディレクトリ直下にある場合
SERVER_CERT_PATH = os.path.expanduser("~/fts/certs/server-cert.pem") 
SERVER_KEY_PATH = os.path.expanduser("~/fts/certs/server-key.pem") 

# このソケットにはまだクライアントの情報が入っていない。
sock = socket(AF_INET, SOCK_STREAM)
sock.bind((IP, PORT))
sock.listen(5)

context = wolfssl.SSLContext(wolfssl.PROTOCOL_TLSv1_2,server_side=True)
context.load_cert_chain(SERVER_CERT_PATH, SERVER_KEY_PATH)

while True:
    try:
        secure_socket = None
        # clientの情報をバインドしたnew_sockが返ってくる.
        print('The server is ready to accept ')
        new_sock, cli_addr = sock.accept()
        secure_socket = context.wrap_socket(new_sock)
        if  secure_socket is not None:
            print("Connection received from ",cli_addr)
            print(secure_socket)
        # secure_socket.write(b'I hear you fa shizzle!'.decode())
        # receive filename from client
        filename = secure_socket.read()
        print('The client requested to send File', filename.decode())
        # ファイルを開いてstrに格納
        try:
            with open(filename, "r") as f:
                # 行ごとに読み込んでリストに格納
                filedata = f.read()
                
                # 末尾の改行を削除 diff による整合性を保つためs
                filedata = filedata.rstrip()
                # print(filetext)
                print('Word count of', filename.decode(),':', len(filedata))
                secure_socket.sendall(filedata)
                

        except FileNotFoundError:
            print('File Not Exist!')
            sys.exit(7)
        
    except KeyboardInterrupt: # Ctrl+C
        print()
        break
    
    finally:
        if secure_socket:
            print('Closing TLS socket...')
            secure_socket.close()


print('Closing TCP socket...')
sock.close()


