#!/usr/bin/python3

"""General Record to Parse

<Blank>
<Header>
<Blank>
<Var Name>
<Var Desc>
<Var Value>
<Var Value>
<Val Desc> (this is a continuation line of a Var Value)
<Var Value>
<Blank>
<Var Name>
...

In general, each test makes sure that the record type can logically
follow its predecessor. Next, it verifies the properties that record
type must possess to differentiate it from other potential record
types. Finally the test returns True if the nested test passes. Since
all other situations will progress to the next (and final) step, False
is returned for any case that does not explicitly return True.

"""

""" First define record type tests """

def is_blank_line(p):
    """
    If p is all whitespace then p.strip will be null thus not p.strip
    is true in that case
    """
    if not p.strip():
        return True
    return False

def is_title(p,pltype):
    if pltype in ['None','Blank']:
        words = p.lower().split()
        if 'acs' in words and 'pums' in words and 'data' in words and 'dictionary' in words:
            return True
    return False

def is_reldate(p,pltype):
    if pltype in ['Blank','Title']:
        words = p.lower().split()
        if len(words) == 3:
            if words[0] in ['january','february','march','april','may','june','july','august',\
                            'september','october','november','december'] and words[2].isdigit():
                return True
    return False
    
def is_record_header(p,pltype):
    """
    Central requirement is that the line begins with HOUSING or PERSON
    followed by RECORD
    """
    if pltype in ['Blank','Rel Date','Header','Var Value','Val Desc']:
        words = p.split()
        if len(words) > 1:
            if words[1][:6] == 'RECORD' and words[0] in ['HOUSING','PERSON']:
                return True
    return False
    
def is_var_name(p,pltype):
    """
    We check that this starts a new variable block and has 3 elements:
    varname, vartype, varlen
    """
    if pltype in ['Blank','Header','Var Value','Val Desc']:
        words = p.split()
        if len(words) == 3:
            if p[0].isalpha() and words[0].isalnum() and words[0].isupper() \
               and words[1].upper() in ['CHARACTER','NUMERIC'] and words[2].isdigit():
                return True
    return False

def is_var_desc(p,pltype):
    """
    The variable description will either follow a Var Name or be a
    continuation of a Var Desc line
    """
    import re
    if pltype in ['Var Name','Var Desc']:
        pparser = re.compile(r"[\t ]+\.")
        words = pparser.split(p)
        if len(words) == 1 and p[0] != '.':
            return True
    return False

def is_var_value(p,pltype):
    """ 
    Variable values follow the variable description or other variable
    values or variable descriptions. It should have a value, whitespace,
    period, and then value description.
    """
    import re
    if pltype in ['Var Desc','Var Value','Val Desc']:
        pparser = re.compile(r"[\t ]+\.")
        words = pparser.split(p)
        if len(words) > 1 and words[0] and words[0][0] != '.' :
            return True
    return False

def is_val_desc(p,pltype):
    """
    Value descriptions are a continuation of a previous variable
    value or a (long) value description. It should have an optional
    whitespace, period, and then the value description.
    """
    import re
    if pltype in ['Var Value','Val Desc']:
        pparser = re.compile(r"[\t ]*\.")
        words = pparser.split(p)
        if len(words) > 1 and not words[0]:
            return True
    return False

""" 
Finally pull the tests together
"""

def classify_line(p,pltype):
    """
    The ordering of the tests below are important since the tests
    are not entirely self-sufficient
    """
    if is_blank_line(p):
        return 'Blank'
    elif is_title(p,pltype):
        return 'Title'
    elif is_reldate(p,pltype):
        return 'Rel Date'
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
        return None
    
