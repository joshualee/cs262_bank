'''
CS 262: Distributed Systems

Created on Feb 18, 2010

Restructured and re-factored by Jim Waldo, 2/17/2014
'''

import socket
import struct
import myServerReceive
import myServerSend
from myServerSend import unknown_opcode
import thread
import serverXml as sxml
import xml.etree.ElementTree as ET

version = '1.0'
OP_CREATE = '10'
OP_DELETE = '20'
OP_DEPOSIT = '30'
OP_WITHDRAW = '40'
OP_BALANCE = '50'
OP_ENDSESSION = '60'

#opcode associations
opcodes = {
    OP_CREATE: myServerReceive.create_request, 
    OP_DELETE: myServerReceive.delete_request,
    OP_DEPOSIT: myServerReceive.deposit_request,
    OP_WITHDRAW: myServerReceive.withdraw_request,
    OP_BALANCE: myServerReceive.balance_request,
    OP_ENDSESSION: myServerReceive.end_session
}

# errors
NO_ERROR = 0
GENERAL_FAILURE = 1
ACCOUNT_NOT_FOUND = 2
INSUFFICIENT_FUNDS = 3
EXCEED_MAX_DAILY_WITHDRAWL = 4
EXCEED_MAX_SINGLE_WITHDRAWL = 5
INVALID_REQUEST = 6
UNSUPPORTED_VERSION = 7
UNKNOWN_OPCODE = 8

# used for error translation
errors = {
    # NO_ERROR: "no error"
    INVALID_REQUEST: "Invalid request",  # e.g. invalid XML
    GENERAL_FAILURE: "Internal server error",
    UNSUPPORTED_VERSION: "Unsupported protocol version",
    ACCOUNT_NOT_FOUND: "Account not found",
    INSUFFICIENT_FUNDS: "Insufficient account funds",
    EXCEED_MAX_DAILY_WITHDRAWL: "Exceeded maximum amount for a daily withdrawl",
    EXCEED_MAX_SINGLE_WITHDRAWL: "Exceeded maximum amount for a single withdrawl"
}

def recordConnect(log, addr):
    print 'Opened connection with ' + addr
    log.write('Opened connection with ' + addr + '\n')
    log.flush()
    
#thread for handling clients
def handler(conn,lock, myData):
    #keep track of erroneous opcodes
    second_attempt = 0
    while True:   
        #retrieve header
        try:
            netbuffer = conn.recv(1024)
        except:
            #close the thread if the connection is down
            thread.exit()

        #unpack message...
        request = sxml.parse_xml(netbuffer)
        error = sxml.validate_request(request)
        
        if error == NO_ERROR:
            opcode = request.find("body").find("op_code").text
            opcodes[opcode](conn, request, myData, lock)
        elif error == UNKNOWN_OPCODE:
            if(second_attempt):
                #disconnect the client
                myServerSend.end_session_success(conn)
                conn.close()
                return
            else:
                #send incorrect opcode message
                second_attempt = 1
                unknown_opcode(conn)

if __name__ == '__main__':
    #set up log
    log = open('log.txt', 'a')
    #data structure for storing account information
    myData = dict()

    #setup socket
    mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mySocket.bind(('',8080))
    mySocket.listen(5)  #param represents the number of queued connections

    #listening for connections
    while True:
        #This is the simple way to start this; we could also do a SELECT
        conn, address = mySocket.accept()
        #log connection
        recordConnect(log, str(address)) 
        #start a new thread
        lock = thread.allocate_lock()
        thread.start_new_thread(handler, (conn, lock, myData))

    log.close()