import socket
import threading

client={}
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.220.112', 8080))
server.listen()
print(f"Server is running")

def connectListen():
    global client
    sock, addr = server.accept()
    if not addr[0] in client:
        print(f"{addr} connecting")
        sock.sendall("getTemperature".encode())
        data = sock.recv(1024)
        client[addr[0]]={"connect":sock, "info":data.decode()}

listen=threading.Thread(target=connectListen)
listen.start()

def temp(ip):
    client[ip]['connect'].sendall("getTemperature".encode())
    data = client[ip]['connect'].recv(1024)
    print(data.decode())

while True:print(eval(input(">>")))