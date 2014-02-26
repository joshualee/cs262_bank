'''
Created on Feb 18, 2010

Altered Feb. 20, 2014
'''
from struct import unpack
from sys import exit

#handle errors from server side.
def general_failure(conn, root):
    print "\nERROR: " + root[1][1]
    return

#create new account
def create_success(conn, root):
    print "Account creation successful "+ root[1][1]
    return

#delete an existing account
def delete_success(conn, root):
    print "Account deletion successful"
    return

#deposit to an existing account
def deposit_success(conn,root):
    print "Deposit success. The updated balance: " + root[1][1]
    return

#withdraw from an existing account
def withdraw_success(conn,root):
    print "Withdrawal success. The updated balance: " + root[1][1]
    return

#withdraw from an existing account
def balance_success(conn,root):
    print "The balance of that account is: " + root[1][1]
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