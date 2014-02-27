'''
Created on Feb 18, 2010

Altered Feb 20, 2014
'''

from struct import pack
import serverXml as sxml
import xml.etree.ElementTree as ET

def general_failure(conn, type, reason):    
    #find the appropriate opcode to send for particular errors
    if type == 'create':
        op_code = '12'
    elif type == 'delete':
        op_code = '22'
    elif type == 'deposit':
        op_code = '32'
    elif type == 'withdraw':
        op_code = '42'
    elif type == 'balance':
        op_code = '52'

    response = sxml.construct_response(op_code, error=reason)
    
    #encode and send the string
    conn.send(ET.tostring(response))
    return

#create new account
def create_success(conn,act):
    response = sxml.construct_response('11', return_val=str(act))
    conn.send(ET.tostring(response))
    return

#delete an existing account
def delete_success(conn):
    response = sxml.construct_response('21')
    conn.send(ET.tostring(response))
    return

#deposit to an existing account
def deposit_success(conn,bal):
    response = sxml.construct_response('31', return_val=str(bal))
    conn.send(ET.tostring(response))
    return

#withdraw from an existing account
def withdraw_success(conn,bal):
    response = sxml.construct_response('41', return_val=str(bal))
    conn.send(ET.tostring(response))
    return

#withdraw from an existing account
def balance_success(conn,bal):
    response = sxml.construct_response('51', return_val=str(bal))
    conn.send(ET.tostring(response))
    return

#end a session
def end_session_success(conn):
    response = sxml.construct_response('61')
    conn.send(ET.tostring(response))
    return

#handle invalid opcodes
def unknown_opcode(conn):
    response = sxml.construct_response('62', error="Unknown opcode")
    conn.send(ET.tostring(response))
    return