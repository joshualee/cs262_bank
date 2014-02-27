import xml.etree.ElementTree as ET

# Copied from myServer.py to avoid circular import
OP_CREATE = '10'
OP_DELETE = '20'
OP_DEPOSIT = '30'
OP_WITHDRAW = '40'
OP_BALANCE = '50'
OP_ENDSESSION = '60'

#opcode associations
opcodes = [
    OP_CREATE,
    OP_DEPOSIT,
    OP_WITHDRAW,
    OP_BALANCE,
    OP_DELETE,
    OP_ENDSESSION
]

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

def parse_xml(s):
  return ET.fromstring(s)

def is_valid_opcode(op_code, arg1, arg2):
  if op_code not in opcodes:
    return UNKNOWN_OPCODE
  
  return NO_ERROR

def validate_request(root):
  if root.tag != "request": 
    return INVALID_REQUEST
    
  header = root.find("header")
  body = root.find("body")
  if header is None or body is None:
      return INVALID_REQUEST
    
  vnum = header.find("ver_num")
  if vnum is None:
    return INVALID_REQUEST
  
  if vnum.text != "1.0":
    return UNSUPPORTED_VERSION
    
  op_code = body.find("op_code")
  arg1 = body.find("arg1")
  arg2 = body.find("arg2")
  
  if op_code is None or arg1 is None or arg2 is None:
    return INVALID_REQUEST
  
  return is_valid_opcode(op_code.text, arg1.text, arg2.text)
    
def construct_response(op_code, error=None, return_val=None):
  response_xml = ET.Element('response')
  header = ET.SubElement(response_xml, 'header')
  body = ET.SubElement(response_xml, 'body')

  ver_num = ET.SubElement(header, 'ver_num')
  ver_num.text = "1.0"

  op_code_tag = ET.SubElement(body, 'op_code')
  op_code_tag.text = op_code

  error_tag = ET.SubElement(body, 'error')
  if error:
    error_tag.text = error

  return_val_tag = ET.SubElement(body, 'return_val')
  if return_val:
    return_val_tag.text = return_val

  return response_xml