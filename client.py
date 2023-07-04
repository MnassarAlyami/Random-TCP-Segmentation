#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket 
import numpy as np
from numpy import random
import time

def client_program():
    server_IP = "3.19.240.187"
    port = 7000 

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client_socket.connect((server_IP, port))
    client_socket.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, True)
    
    # Set the initial size of the send buffer
    sndbuf_size = pow(2,12)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, sndbuf_size)
    
    data = ["x"] * 10000000
    
    Min = 100
    Max = 1400
    start_index = 0
    last_index = len(data)-1
    i = 0
    while start_index <= last_index:
        
        alloc_len = random.randint(Min, Max)
        
        #Update the send buffer to equal the receive buffer after the initial stage of communication
        if i == 100:
            sndbuf_size = pow(2,16)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, sndbuf_size)
        
        if start_index + alloc_len >= last_index:
            x = last_index
        else:
            x = start_index + alloc_len
        
        pkt = ''.join(data[start_index : x + 1])
        i = i + 1

        client_socket.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, True)
        client_socket.send(pkt.encode())
        
        start_index = x + 1 
    
    client_socket.close()  # close the connection
    
if __name__ == '__main__':
    client_program()

