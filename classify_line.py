#!/usr/bin/python3

""" 
General Record to Parse

<Blank>
<Header>
<Blank>
<Var Name>
<Var Desc>
<Var Value>
<Var Value>
<Val Desc>
<Var Value>
<Blank>
<Var Name>
...
"""

""" First define record type tests """

def is_blank_line(p):
    if not p.strip():
        return True
    return False

def is_record_header(p,pltype):
    """ Central requirement is that the line begins with HOUSING or PERSON followed by RECORD """
    if pltype in ['Blank','Header','Var Value','Val Desc']:
        words = p.split()
        if len(words) > 1:
            if words[1][:6] == 'RECORD' and words[0] in ['HOUSING','PERSON']:
                return True
    return False
    
def is_var_name(p,pltype):
    if pltype in ['Blank','Header','Var Value','Val Desc']:
        words = p.split()
        if len(words) == 2:
            if p[0].isalpha() and words[0].isalnum() and words[0].isupper() and words[1].isdigit():
                return True
    return False

def is_var_desc(p,pltype):
    import re
    if pltype in ['Var Name','Var Desc']:
        pparser = re.compile(r"[\t ]+\.")
        words = pparser.split(p)
        if len(words) == 1 and p[0] != '.':
            return True
    return False

def is_var_value(p,pltype):
    """ The parser creates a single split caused by required whitespace followed by a period """
    import re
    if pltype in ['Var Desc','Var Value','Val Desc']:
        pparser = re.compile(r"[\t ]+\.")
        words = pparser.split(p)
        if len(words) > 1 and words[0]:
            return True
    return False

def is_val_desc(p,pltype):
    """ The parser causes a single split caused by optional white space followed by a period """
    import re
    if pltype in ['Var Value','Val Desc']:
        pparser = re.compile(r"[\t ]*\.")
        words = pparser.split(p)
        if len(words) > 1 and not words[0]:
            return True
    return False

""" Now pull it together to classify a general line: order is important """

def classify_line(p,pltype):
    if is_blank_line(p):
        return 'Blank'
    elif is_record_header(p,pltype):
        return 'Header'
    elif is_var_name(p,pltype):
        return 'Var Name'
    elif is_var_desc(p,pltype):
        return 'Var Desc'
    elif is_var_value(p,pltype):
        return 'Var Value'
    elif is_val_desc(p,pltype):
        return 'Val Desc'
    else:
        return 'None'
    
