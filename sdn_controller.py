"""
File_Name : sdn_controller.py
Author : Vaibhav Joshi(vj3470@rit.edu)
Version : 2.0
Revisions : adding topology structure

This file contains the implementation code for the SDN Controller. It binds the controller with
the port 6653 (Mininet's default port) and accepts packets from our custom created ring topology
network. It parses the request headers and send the appropriate reply back and generates topology
"""
import socket
import sys
import binascii
from _thread import *
import errno
from socket import error as SocketError
import re




def message_parse(connection,client,net_info) :
    """
    Method that parses the headers and generates the
    network topology by sending requests and interpreting repljes
    Each switch has a new instance

    :param connection: connection details
    :param client: client addr
    :param net_info: data structure info
    :return: None
    """

    try:
        #unique dpid for each thread
        dpid=""
        # maintain the connection, receive the data from topology and send back appropriate response
        while True :

            data=connection.recv(1024)
            # convert incoming data to hex
            hex_code=binascii.hexlify(data)

            # convert hex to string for easier processing
            hex_to_str=str(hex_code, 'utf-8')

            if net_info is not None:
                # if ECHO_HELLO
                if hex_to_str[2 :4]=='00' :
                    hex_to_str=bytes.fromhex(hex_to_str)
                    # send back HELLO
                    connection.send(hex_to_str)

                # if ECHO_REQUEST
                elif hex_to_str[2 :4]=='02' :
                    hex_to_str.replace('02', '03')
                    hex_to_str=bytes.fromhex(hex_to_str)
                    connection.send(hex_to_str)

                # if echo reply
                elif hex_to_str[2 :4]=='03' :


                    hex_to_str.replace('03', '05')
                    hex_to_str="0505000800000000"
                    hex_to_str=bytes.fromhex(hex_to_str)

                    connection.send(hex_to_str)

                #received feature reply
                elif hex_to_str[2 :4]=='06' :

                    dpid=hex_to_str[31 :32]
                    net_info[dpid]={}  # initialize a dictionary for each dpid.
                    print("DPID:", dpid)
                    hex_to_str="0512001000000000000d00000000"
                    hex_to_str=bytes.fromhex(hex_to_str)
                    connection.send(hex_to_str)

                #Recieved multipart response
                elif hex_to_str[2:4]=='13':

                    # Generate dictionary
                    p1 = int(hex_to_str[32:40], 16)
                    hwaddr1= ':'.join(re.findall('..', hex_to_str[48:60]))
                    p2 = int(hex_to_str[176 :184], 16)
                    hwaddr2=':'.join(re.findall('..', hex_to_str[192 :204]))
                    p3 = int(hex_to_str[320 :328], 16)
                    hwaddr3 = ':'.join(re.findall('..', hex_to_str[336 :348]))
                    d = {p1 : hwaddr1, p2 : hwaddr2, p3 : hwaddr3}
                    net_info[dpid]=d
                    print(net_info)

    except SocketError as err:
        if err.errno == errno.ECONNRESET:
            pass





if __name__=='__main__' :

    HOST='127.0.0.1'  # localhost
    PORT=6653  # Mininets default port

    # creating TCP/IP socket
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # binding details
    server_address=(HOST, 6653)

    print('starting up on %s port %s'%server_address)

    # bind the socket to the port 6653
    sock.bind(server_address)

    # listen for incoming connections
    sock.listen(5)

    # dictionary to store network info
    net_info = {}

    # start multithreading
    while True:

        conn, client = sock.accept()
        # new instance for new thread
        start_new_thread(message_parse,(conn,client,net_info))





