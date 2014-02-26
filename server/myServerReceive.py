'''
Created on Feb 26, 2014


'''
from myServerSend import general_failure, end_session_success,create_success, delete_success,deposit_success,withdraw_success,balance_success
import sys

# used to take an xml object and return a dictionary, keys = tag and values = text
def unpack_xml(xml):
    xml_dict = {}
    for elem in xml.iter():
        xml_dict[elem.tag] = elem.text
    return xml_dict

#create new account
def create_request(conn,netBuffer,myData,lock):
    
    values = unpack_xml(netBuffer)
    
    lock.acquire()
    try:
        try:
            values['arg1'] = int(values['arg1'])
            values['arg2'] = int(values['arg2'])
        except ValueError:
            general_failure(conn, 'create', "invalid arguments")

        #get balance
        try:
          a1 = int(values['arg1'])
          a2 = int(values['arg2'])
        except ValueError:
          general_failure(conn, 'create', "invalid balance")
          return
          
        if(values['arg1'] >= 0 and values['arg1'] < sys.maxint):
            bal = int(values['arg1'])

        else:
            general_failure(conn, 'create', "invalid balance")
            return
        
        #get account number
        if values['arg2'] > 0 and values['arg2'] <= 100:
            act = values['arg2']
            if act in myData:
                general_failure(conn, 'create',"account already in use")
                return
            
        #generate a value if it was -1
        elif values['arg2'] == -1:
            i = 1
            while i in myData:
                i+=1
                if i == 101:
                    general_failure(conn, 'create',"no remaining accounts")
                    return
            act = i
        else:
            general_failure(conn, 'create',"invalid account number")
            return
            
        myData[act] = bal
        create_success(conn,act)
    finally:
        lock.release()
        print myData
    
    return

#delete an existing account
def delete_request(conn,netBuffer,myData,lock):
    values = unpack_xml(netBuffer)
    
    lock.acquire()
    try:

        try:
            values['arg1'] = int(values['arg1'])
        except ValueError:
            general_failure(conn, 'create', "invalid arguments")
            
        #get balance
        if(values['arg1'] >= 0 and values['arg1'] <= 100):
            act = values['arg1']
        else:
            general_failure(conn,'delete',"invalid account number")
            return
        
        if act not in myData:
            general_failure(conn,'delete',"nonexistent account number")
            return
            
        if myData[act] != 0:
            general_failure(conn,'delete',"nonzero money in that account")
            return

        del myData[act]
        delete_success(conn)
    finally:
        lock.release()
        print myData
    
    return

#deposit to an existing account
def deposit_request(conn,netBuffer,myData,lock):
    values = unpack_xml(netBuffer)
    lock.acquire()
    try:

        try:
            values['arg1'] = int(values['arg1'])
            values['arg2'] = int(values['arg2'])
        except ValueError:
            general_failure(conn, 'create', "invalid arguments")

        #get account number
        if(values['arg1'] >= 0 and values['arg1'] <= 100):
            act = values[0]
        else:
            general_failure(conn,'deposit',"invalid account number")
            return
        
        #check for existence of account
        if act not in myData:
            general_failure(conn,'deposit',"nonexistent account number")
            return
        
        #check for a valid deposit amount
        if values['arg2'] > 0:
            bal = values['arg2']
        else:
            general_failure(conn,'deposit',"nonsense deposit amount")
            return
            
        curr_bal = myData[act]
        
        #check that the new balance won't overflow
        if bal < sys.maxint - curr_bal - 1:
            myData[act] = curr_bal + bal
        else:
            general_failure(conn,'deposit',"account overflow... damn you are rich")
            return
        deposit_success(conn, curr_bal + bal)
    finally:
        lock.release()
        print myData
    
    
    return

#withdraw from an existing account
def withdraw_request(conn,netBuffer,myData,lock):
    values = unpack_xml(netBuffer)
    lock.acquire()
    try:

        try:
            values['arg1'] = int(values['arg1'])
            values['arg2'] = int(values['arg2'])
        except ValueError:
            general_failure(conn, 'create', "invalid arguments")

        #get account number
        if(values['arg1'] >= 0 and values['arg1'] <= 100):
            act = values['arg1']
        else:
            general_failure(conn,'withdraw',"invalid account number")
            return
        
        #check for existence of account
        if act not in myData:
            general_failure(conn,'withdraw',"nonexistent account number")
            return
        
        #check for a valid withdraw amount
        if values['arg2'] > 0:
            bal = values['arg2']
        else:
            general_failure(conn,'withdraw',"nonsense withdrawal amount")
            return
            
        curr_bal = myData[act]
        
        #check that the new balance won't overflow
        if curr_bal - bal >= 0:
            myData[act] = curr_bal - bal
        else:
            general_failure(conn,'withdraw',"not enough money in account")
            return
        withdraw_success(conn, curr_bal - bal)
    finally:
        lock.release()
        print myData 
    return

#withdraw from an existing account
def balance_request(conn,netBuffer,myData,lock):
    #no need to lock: we are just reading a value from a dict, which is thread-safe
    values = unpack_xml(netBuffer)

    try:
            values['arg1'] = int(values['arg1'])
        except ValueError:
            general_failure(conn, 'create', "invalid arguments")

    #get balance
    if(values['arg1'] >= 0 and values['arg1'] <= 100):
        act = values['arg1']
    else:
        general_failure(conn,'balance',"invalid account number")
        return
    
    #get the current balance
    try:
        bal = myData[act]
    except KeyError:
        general_failure(conn,'balance',"nonexistent account")
        return

    balance_success(conn,bal)
    
    return

#end a session
def end_session(conn,netBuffer,myData,lock):
    end_session_success(conn)
    conn.close()
    return



