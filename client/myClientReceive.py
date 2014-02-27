'''
Created on Feb 18, 2010

Altered Feb. 20, 2014
'''
from struct import unpack
from sys import exit
import xml.etree.ElementTree as ET

#handle errors from server side.
def general_failure(conn, root):
    val = root.find("body").find("error").text
    print "\nERROR: " + val
    return

#create new account
def create_success(conn, root):
    print "create_success"
    val = root.find("body").find("return_val").text
    print "Account creation successful "+ val
    return

#delete an existing account
def delete_success(conn, root):
    print "Account deletion successful"
    return

#deposit to an existing account
def deposit_success(conn,root):
    val = root.find("body").find("return_val").text
    print "Deposit success. The updated balance: " + val
    return

#withdraw from an existing account
def withdraw_success(conn,root):
    val = root.find("body").find("return_val").text
    print "Withdrawal success. The updated balance: " + val
    return

#withdraw from an existing account
def balance_success(conn,root):
    val = root.find("body").find("return_val").text
    print "The balance of that account is: " + val
    return

#end a session
def end_session_success(conn,root):
    print "SHUTTING DOWN"
    conn.close()
    exit()
    return

#handle invalid opcodes
def unknown_opcode(conn):
    print "ERROR: INCORRECT OPCODE"
    return