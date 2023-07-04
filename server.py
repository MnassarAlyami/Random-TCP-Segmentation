#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket 

def server_program():
    host = socket.gethostname()
    port = 7000 
    data_size = 0
    server_socket = socket.socket() 
    server_socket.bind((host, port))
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept() 
    print("Connection from: " + str(address))

    while True:
        data = conn.recv(100000).decode()
        data_size += len(data)
        if not data:
            # if data is not received break
            break
    print("Received " + str(data_size) + " Bytes")

    conn.close()  
if __name__ == '__main__':

    server_program()

