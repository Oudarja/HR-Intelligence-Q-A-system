import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('172.16.2.155', 4370))
    print("TCP port is open!")
except:
    print("TCP port is closed or unreachable.")
s.close()
