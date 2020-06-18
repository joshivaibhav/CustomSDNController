////**********************
                          

This is the README file containing the documentation pertaining to the sdn_controller.py file.
Author : Vaibhav Joshi (vj3470@rit.edu)

************************/////////                     
                        
The sdn_controller.py is the SDN Controller which communicates with the switches created by mininet in a ring topology.


In order to start the controller and demonstrate its execution the following steps are required:

1) Setup the custom topology with mininet
Create a python file containing the custom topology of 5 switches linked together in a ring.
 

2) Run the Python SDN Controller:
    Start up the python controller and make it listen on port 6653

3) Start the topology and assign our SDN Controller as the remote controller using the following command : 
sh sudo ovs-vsctl set-controller s1 tcp:127.0.0.1:6653


The above steps should do the job. After this, we capture the packet activity through WireShark and analyse the ECHO_REQUEST and ECHO_REPLIES.


This code is a continuation of the previous code. The controller fetches the ECHO_REPLY and sends back the FEATURE_REQ. It gets the FEATURE_REQ back and sends a MULIPART_REQ to the network. The MULTIPART_REPLY received will be parsed to build the topology and store it in a dictionary.



References : 

SDN Controller -  https://github.com/mininet/mininet/blob/master/examples/emptynet.py

