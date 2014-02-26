import myServer as S

SERVER_RESPONSE_XMLTEMPLATE =
" \
<response> \
    <header> \
        <ver_num></ver_num> \
    </header> \
    <body> \
        <op_code></op_code> \
        <error></error> \
        <return_val></return_val> \
    </body> \
</response> \
"

def parse_xml(s):
  pass

def is_valid_opcode(op_code, arg1, arg2):
  if op_code not in S.opcodes:
    return INVALID_REQUEST  
    
  if op_code == OP_DELETE:
    try:
      _ = int(arg1)
    except ValueError:
      return INVALID_REQUEST
  elif op_code == OP_DEPOSIT:
    try:
      _ = int(arg1)
      _ = int(arg2)
    except ValueError:
      return INVALID_REQUEST
  elif op_code == OP_WITHDRAW:
    try:
      _ = int(arg1)
      _ = int(arg2)
    except ValueError:
      return INVALID_REQUEST
  elif op_code == OP_BALANCE:
    try:
      _ = int(arg1)
    except ValueError:
      return INVALID_REQUEST  
  
  return NO_ERROR

def validate_request(root):
  if root.tag != "request": 
    return INVALID_REQUEST
    
  header = root.find("header")
  body = root.find("body")
  if not header or not body:
      return INVALID_REQUEST
    
  vnum = header.find("ver_num")
  if not vnum:
    return INVALID_REQUEST
  
  if vnum.text != S.version:
    return UNSUPPORTED_VERSION
    
  op_code = body.find("op_code")
  arg1 = body.find("arg1")
  arg2 = body.find("arg2")
  
  if not op_code or not arg1 or not arg2:
    return INVALID_REQUEST
  
  return is_valid_opcode(op_code, arg1, arg2)
    
def construct_response(op_code, error=None, return_val=None):
  response_xml = ET.Element('response')
  header = ET.SubElement(response_xml, 'header')
  body = ET.SubElement(response_xml, 'body')

  ver_num = ET.SubElement(header, 'ver_num')
  ver_num.text = S.version

  op_code = ET.SubElement(body, 'op_code')
  op_code.text = inputs['op_code']

  error_tag = ET.SubElement(body, 'error')
  if error:
    error_tag.text = error

  return_val_tag = ET.SubElement(body, 'return_val')
  if return_val:
    return_val_tag.text = return_val

  return response_xml