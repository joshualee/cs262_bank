'''
Created on Feb 18, 2010

altered on Feb. 20, 2014
'''

from struct import pack
from sys import maxint, exit
import xml.etree.ElementTree as ET

#create new account
def create_request(conn):
    
    print "CREATING AN ACCOUNT \n"
    print "enter a starting balance:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break
        
    print "enter a an account number 1-100(input 0 for a random number):"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
        elif(netBuffer == 0):
            act = -1
            break
    
    send_message(create_xml("1.0","10",str(bal),str(act)),conn)
    return

#delete an existing account
def delete_request(conn):
    print "DELETING AN ACCOUNT \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
    
    send_message(create_xml("1.0","20",str(act),""),conn)
    return

#deposit to an existing account
def deposit_request(conn):
    print "DEPOSITING SOME DOUGH \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
    print "enter an amount to deposit:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break
        
    send_message(create_xml("1.0","30",str(bal),str(act)),conn)
    return

#withdraw from an existing account
def withdraw_request(conn):
    print "WITHDRAWING SOME DOUGH \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
        
    print "enter an amount to withdraw:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break
        
    send_message(create_xml("1.0","40",str(bal),str(act)),conn)
    return

#withdraw from an existing account
def balance_request(conn):
    print "CHECKING THE BALANCE OF AN ACCOUNT \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break

    send_message(create_xml("1.0","50",str(act),""),conn)
    return

#end a session
def end_session(conn):
    send_message(create_xml("1.0","60","",""),conn)
    return

def send_message(message, conn):
    try:
        conn.send(message)
    except:
            #close the client if the connection is down
            print "ERROR: connection down"
            exit()
    return

# create an xml object 
def create_xml(version, code, arg1,arg2):

    request = ET.Element('request')
    header = ET.SubElement(request, 'header')
    body = ET.SubElement(request, 'body')

    ver_num = ET.SubElement(header, 'ver_num')
    ver_num.text = version

    op_code = ET.SubElement(body, 'op_code')
    op_code.text = code


    a1 = ET.SubElement(body, "arg1")
    a1.text = arg1
    a2 = ET.SubElement(body, "arg2")
    a2.text = arg2

    return ET.tostring(request)




