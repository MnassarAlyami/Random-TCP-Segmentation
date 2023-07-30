#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from scapy.all import *
import random
import csv
import pandas as pd


header = 82
input_file = ("file_name.pcap")
output_file = ("obfuscated.csv")

MIN = 5
MAX = 20
Prob = 0.8

#Write the Header in the file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Src", "Dst", "Length"])

def random_segmentation(input_file, output_file):
    capture = rdpcap(input_file) 
    t_start = capture[0].time

    for pkt in capture:
        #packet_timestamp = pkt.time
        packet_payload = len(pkt) - header
        packet_src = pkt.addr2
        packet_dst = pkt.addr1

        if packet_payload <= 0:
            continue #skip acks
        
        elif packet_payload > 0 and random.random() <= Prob:
            ptr = packet_payload
        
            while ptr > 0:
                alloc_len = random.randint(MIN, MAX)
                if ptr - alloc_len <= 0:
                    x = ptr
                else:
                    x = alloc_len
               
                chunk_size = x 
                with open(output_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    t_s = pkt.time - t_start
                    writer.writerow([t_s + (t_s * 0.2), packet_src, packet_dst, chunk_size + header])
                
                
                ptr -= chunk_size
        else:
            #Write the packets passed the random pick for segmentation
            with open(output_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([float(pkt.time - t_start), packet_src, packet_dst, packet_payload + header])
    
random_segmentation(input_file, output_file)  


# Read the CSV file
df = pd.read_csv(output_file)

# Sort the DataFrame based on the values in the first column
sorted_df = df.sort_values(by=df.columns[0])

# Write the sorted DataFrame to a new CSV file
sorted_df.to_csv(output_file, index=False)

