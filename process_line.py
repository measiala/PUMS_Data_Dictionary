from class_defs import *
from classify_line import classify_line

def add_var_name(p,dd):
    words = p.split(maxsplit=1)
    varname = words[0]
    varlen  = words[1]
    if varname in dd.vardict.keys():
        print("ERROR: Variable %s already defined." % varname)
        return None
    else:
        dd.add_var(varname)
        dd.vars[dd.vardict[varname]].varlen = int(varlen)
        return varname

def add_var_desc(p,dd,varname):
    if varname in dd.vardict.keys():
        v = dd.vars[dd.vardict[varname]]
        v.vardesc = (v.vardesc + ' ' + p).strip()
        return True
    else:
        print("ERROR: Issue with assigning variable description.")
        return False

def add_var_value(p,dd,varname):
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
        return words[0]
    else:
        print("ERROR: Issue with assigning variable value.")
        return None
    
def add_val_desc(p,dd,varname,valname):
    """ The parser causes a single split caused by optional white space followed by a period """
    import re
    pparser = re.compile(r"[\t ]*\.")
    
    """ words will have [empty string, value description] """
    words = pparser.split(p,maxsplit=1)
    value_desc = words[1]

    """ FINISH """
    if varname in dd.vardict.keys():
        v = dd.vars[dd.vardict[varname]]
        if valname in v.valdict.keys():
            #print(v,v.name,v.valdict[valname])
            v.valdict[valname] = (v.valdict[valname] + ' ' + value_desc).strip()
            #print(v,v.name,v.valdict[valname])
            return True
    else:
        print("ERROR: Issue with assigning variable description.")
    return False

def process_line(p,dd,ltype,varname,valname):
    words = p.split()
    
    if ltype == 'Blank':
        return True
    elif ltype == 'Var Name':
        return add_var_name(p,dd)
    elif ltype == 'Var Desc':
        return add_var_desc(p,dd,varname)
    elif ltype == 'Var Value':
        return add_var_value(p,dd,varname)
    elif ltype == 'Val Desc':
        return add_val_desc(p,dd,varname,valname)

if __name__ == '__main__':
    dd = DataDict('PUMS 2017')
    plist = ['PWGTP 5','Person Weight','-9999..9999 .Integerized Person Weight','.Vacant Unit']
    pltype = 'Header'
    pvar = ''
    pval = ''
    for p in plist:
        ltype = classify_line(p,pltype)
        tmp = process_line(p,dd,ltype,pvar,pval)
        if ltype == 'Var Name' and tmp != None:
            pvar = tmp
        if ltype == 'Var Value' and tmp != None:
            pval = tmp
        print(ltype,tmp,pvar)
        print("Name",dd.vars[-1].name)
        print("Type",dd.vars[-1].vartype)
        print("LEN",dd.vars[-1].varlen)
        print("Desc",dd.vars[-1].vardesc)
        print("Dict",dd.vars[-1].valdict)
        print(pvar)
        pltype = ltype
   
