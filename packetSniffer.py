# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 03:16:26 2017

@author: Christian
"""

import socket
import struct
import textwrap

# Constants for tabs
TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t - '
DATA_TAB_2 = '\t\t - '
DATA_TAB_3 = '\t\t\t - '
DATA_TAB_4 = '\t\t\t\t - '

# Unpack Ethernet frame
def ethernet_frame(data):
    # ! signifies network data, dest_mac and src_mac are 6s or 6 characters (6 bytes), proto is H or small unsigned int (2 bytes)
    # This is a total of 14 bytes, so receive the first 14 bytes from data
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    print("Data: {}".format(data))
    # Now pass the mac addresses through the get_mac_addr which converts the bytes into readable mac addresses
    # And convert the protocol into a readable format, and pass the rest of the data after the 14 bytes onward
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]


# Returns the properly formatted MAC address FORMAT - AA:BB:CC:DD:EE:FF
def get_mac_addr(bytes_addr):
    
    # Format the bytes so it is 2 decimal place chunks
    bytes_str = map('{:02x}'.format, bytes_addr)
    
    # Finish the formatting by joining each chunk with :'s and setting to uppercase
    mac_addr = ':'.join(bytes_str).upper()
    return mac_addr

# Unpacks the IPv4 Packet
def ipv4_packet(data):
    # Get the version and version_header_length from the data (automatically will get all those bytes, this needs to be split later)
    version_header_length = data[0]
    
    # Shift the version 4 bits to the right to get the version length
    version = version_header_length >> 4
    
    # And the bytes : compare 2 bytes and get result when both bytes are 1
    # We need this to know when the header actually ends and when the rest of our 'useful' data begins
    header_length = (version_header_length & 15) * 4
    
    # ! - again signifying network traffic and makes sure our byte order is correct
    # Bringing in the next chunk of binary and extracting it into these variables according to the format '! 8x B B 2x 4s 4s'
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    
    # Return all the extracted data, format the src and target correctly with the ipv4 format function, and return the rest of the data AFTER the header_length
    return version, header_length, ttl, proto, ipv4(src), ipv4(target), data[header_length:]

# Returns properly formatted IPv4 address ex. 127.0.0.1
def ipv4(addr):
    
    # Format the address by converting to string and joining with .'s
    formatted_ipv4_addr = '.'.join(map(str, addr))
    
    # Return the formatted ipv4 address
    return formatted_ipv4_addr

# Unpacks ICMP packet (when the protocol == 1)
def icmp_packet(data):
    
    # Get the first 4 bytes of data and store into variables
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    
    # Return the unpacked bytes
    return icmp_type, code, checksum, data[4:]

# Unpacks the TCP packet (when the protocol == 6)
def tcp_segment(data):
    
    # Unpack 14 bytes into the following variables and format correctly (more formatting needed for offset_reserved_flags)
    (src_port, dest_port, sequence, acknowledgement, offset_reserved_flags) = struct.unpack('! H H L L H', data[:14])
    
    # The following is formatting for the offset_reserved_flags
    # Bit shift to the right 12
    offset = (offset_reserved_flags >> 12) * 4
    
    # These flags are like the SYN, ACK, FIN, from the TCP three-way-handshake
    flag_urg = (offset_reserved_flags & 32) >> 5
    flag_ack = (offset_reserved_flags & 16) >> 4
    flag_psh = (offset_reserved_flags & 8) >> 3
    flag_rst = (offset_reserved_flags & 4) >> 2
    flag_syn = (offset_reserved_flags & 2) >> 1
    flag_fin = offset_reserved_flags & 1
    
    # Finally return all the calculated and extracted values and all the data AFTER the offset
    return src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]

# Unpacks the UDP segment (when the protocol == 17)
def udp_segment(data):
    
    # Unpacks 8 bytes into the following variables and formats correctly
    src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
    
    # Return the unpacked values and the data AFTER the UDP segment (8 bytes)
    return src_port, dest_port, size, data[8:]

# Formats multi-line data
def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap(string, size)])

#######################################################
#################### MAIN FUNCTION ####################
#######################################################

def main():
    
    # Get the host computer and print out the host IP
    HOST = socket.gethostbyname(socket.gethostname())
    print('IP: {}'.format(HOST))
    
    # Set up the socket
    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    
    # Bind the socket and set up the socket
    conn.bind((HOST, 0))
    
    # This line includes IP headers
    conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    # Disable promiscuous mode
    conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    # Main Loop
    while True:
        
        # Receive the data from the connection as raw data and the addr
        raw_data, addr = conn.recvfrom(65535)
        
        # Send the raw_data through the ethernet_frame method to unpack it
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
        
        # Print out the data from the Ethernet Frame, including the destination and source MAC addresses and the Protocol
        print('\nEthernet Frame:')
        print('Destination: {}, Source: {}, Protocol: {}'.format(dest_mac, src_mac, eth_proto))
        
        print('Protocol: {}'.format(eth_proto))
        # Check if using IPv4
        if eth_proto == 8:
            
            # Now get the version, header_length, ttl, proto, src, and target from unpacking the IPv4 Packet from the data
            (version, header_length, ttl, proto, src, target, data) = ipv4_packet(data)
            
            # Print out the extracted information
            print(TAB_1 + 'IPv4 Packet:')
            print(TAB_2 + 'Version: {}, Header Length: {}, TTL: {} '.format(version, header_length, ttl))
            print(TAB_2 + 'Protocol: {}, Source: {}, Target: {} '.format(proto, src, target))
            
            ######################################################
            #################### ICMP Packets ####################
            ######################################################
            
            # Test to see if the packet is ICMP(1)
            if proto == 1:
                
                # Unpack the ICMP packet
                icmp_type, code, checksum, data = icmp_packet(data)
                
                # Print out the extracted information
                print(TAB_1 + 'ICMP Packet:')
                print(TAB_2 + 'Type: {}, Code: {}, Checksum: {} '.format(icmp_type, code, checksum))
                
                # Finally format and print out the data
                print(TAB_2 + 'Data: ')
                print(format_multi_line(DATA_TAB_3, data))
                
            #####################################################
            #################### TCP Packets ####################
            #####################################################
                
            # Test to see if the packet is TCP(6)
            elif proto == 6:
                
                # Unpack the TCP segment
                src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data = tcp_segment(data)
                
                # Print out the extracted information
                print(TAB_1 + 'TCP Segment:')
                print(TAB_2 + 'Src Port: {}, Dest Port: {}, Sequence: {}, Acknowledgement: {}'.format( src_port, dest_port, sequence, acknowledgement))
                print(TAB_2 + 'URG: {}, ACK: {}, PSH: {}, RST: {}, SYN: {}, FIN: {}'.format(flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin))
                
                # Finally format and print out the data
                print(TAB_2 + 'Data: ')
                print(format_multi_line(DATA_TAB_3, data))
                
            #####################################################
            #################### UDP Packets ####################
            #####################################################
            
            # Test to see if the packet is UDP(17)
            elif proto == 17:
                
                # Unpack the UDP segment
                src_port, dest_port, size, data = udp_segment(data)
                
                # Print out the extracted information
                print(TAB_1 + 'UDP Segment')
                print(TAB_2 + 'Src Port: {}, Dest Port: {}, Size: {}'.format(src_port, dest_port, size))
                
                # Finally format and print out the data
                print(TAB_2 + 'Data: ')
                print(format_multi_line(DATA_TAB_3, data))
        
        
# Run main()
main()