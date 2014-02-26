import xml.etree.ElementTree as ET

version = "1.0" #'\x01'

opcodes = {'11': "create_success",
           '12': "general_failure", 
           '21': "delete_success",
           '22': "general_failure",
           '31': "deposit_success",
           '32': "general_failure",
           '41': "withdraw_success",
           '42': "general_failure",
           '51': "balance_success",
           '52': "general_failure",
           '61': "end_session_success",
           '62': "unknown_opcode"
           }

response = ET.Element('response')
header = ET.SubElement(response, 'header')
body = ET.SubElement(response, 'body')

ver_num = ET.SubElement(header, 'ver_num')
ver_num.text = version

op_code = ET.SubElement(body, 'op_code')
op_code.text = "11"

return_val = ET.SubElement(body, "return_val")
return_val.text = "1"

root = ET.fromstring(ET.tostring(response))

ET.dump(root)
print root[0][0].text

if root[0][0].text == version:
    print root[0][0]
    opcode = root[1][0].text
    #send packet to correct handler
    try:
        print opcodes[opcode]
    except KeyError:
        print "key"