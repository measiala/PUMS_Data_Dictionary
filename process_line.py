from class_defs import *
from classify_line import classify_line

def add_var_name(p):
    words = p.split(maxsplit=1)
    varname = words[0]
    varlen  = words[1]
    if varname in dd.vardict.keys():
        print("ERROR: Variable already defined.")
        return None
    else:
        dd.add_var(varname)
        dd.vars[dd.vardict[varname]].varlen = varlen
        return varname

def add_var_desc(p,varname):
    print(varname,dd.vardict.keys())
    if varname in dd.vardict.keys():
        dd.vars[dd.vardict[varname]].vardesc = (dd.vars[dd.vardict[varname]].vardesc + p).strip()
        return True
    else:
        print("ERROR: Issue with assigning variable description.")
        return False

def add_var_value(p,varname):
    """ The parser creates a single split caused by required whitespace followed by a period """
    import re
    pparser = re.compile(r"[\t ]+\.")
    
    """ words will have [value range, value description] """
    words = pparser.split(p,maxsplit=1)

    """ Value range is either value_low..value_high or simply value_low """
    value_rng = words[0].split('..',maxsplit=1)
    value_low = value_rng[0]
    if len(value_rng) > 1:
        value_high = value_rng[1]
    else:
        value_high = None

    value_desc = words[1]

    """ FINISH """
    if varname in dd.vardict.keys():
        dd.vars[dd.vardict[varname]].add_value(value_low,value_high,value_desc)
        return True
    else:
        print("ERROR: Issue with assigning variable value.")
        return False
    
def add_val_desc(p,varname):
    """ The parser causes a single split caused by optional white space followed by a period """
    import re
    pparser = re.compile(r"[\t ]*\.")
    
    """ words will have [empty string, value description] """
    words = pparser.split(p,maxsplit=1)
    value_rng = words[0].split('..',maxsplit=1)
    
    value_low = value_rng[0]
    if len(value_rng) > 1:
        value_high = value_rng[1]
    else:
        value_high = None

    value_desc = words[1]

    """ FINISH """
    if varname in dd.vardict.keys():
        dd.vars[dd.vardict[varname]].vardesc = (dd.vars[dd.vardict[varname]].vardesc + p).strip()
        return True
    else:
        print("ERROR: Issue with assigning variable description.")
        return False

def process_line(p,ltype,varname):
    words = p.split()
    
    if ltype == 'Blank':
        print("")
    elif ltype == 'Var Name':
        return add_var_name(p)
    elif ltype == 'Var Desc':
        return add_var_desc(p,varname)
    elif ltype == 'Var Value':
        return add_var_value(p,varname)
    elif ltype == 'Val Desc':
        return add_val_desc(p,varname)

if __name__ == '__main__':
    dd = DataDict('PUMS 2017')
    plist = ['PWGTP 5','Person Weight','-9999..9999 .Integerized Person Weight','0 .Vacant Unit']
    pltype = 'Header'
    pvar = ''
    for p in plist:
        ltype = classify_line(p,pltype)
        tmp = process_line(p,ltype,pvar)
        if ltype == 'Var Name' and tmp != None:
            pvar = tmp
        print(ltype,tmp,pvar)
        print("Name",dd.vars[-1].name)
        print("Type",dd.vars[-1].vartype)
        print("LEN",dd.vars[-1].varlen)
        print("Desc",dd.vars[-1].vardesc)
        print("Dict",dd.vars[-1].valdict)
        print(pvar)
        pltype = ltype
   
