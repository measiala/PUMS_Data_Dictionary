from class_defs import *
from classify_line import classify_line

def add_var_name(p):
    words = p.split()
    varname = words[0]
    varlen  = words[1]
    if varname in dd.vardict.keys():
        print("ERROR: Variable already defined.")
        return False
    else:
        dd.add_var(varname)
        dd.vars[dd.vardict[varname]].varlen = varlen
        return True

def add_var_desc(p,varname):
    if varname in dd.vardict.keys():
        dd.vars[dd.vardict[varname]].vardesc = (dd.vars[dd.vardict[varname]].vardesc + p).strip()
        return True
    else:
        print("ERROR: Issue with assigning variable description.")
        return False
    
def add_val_desc(p,varname):
    if p.split()[0][0:3] == 'N.A':
        var_val = p.split()[0]
        words1d = p[len(var_val):].strip().split('.')
    else:
        words2d = p.split('..')
        if len(words2d) > 1:
            var_low = words2d[0].strip()
            words1d = words2d[1].strip().split('.')
            var_high = words1d[0].strip()
            var_val = var_low + '..' + var_high
            dd.vars[dd.vardict[varname]].valdict = [ var_low, var_high, '' ]
        else:
            words1d = p.split('.')
            var_val  = words1d[0].strip()
            var_low  = var_val
            var_high = var_val
    var_val_desc = words1d[1].strip()
    if len(words1d) > 1:
        for i in range(2, len(words1d)):
            var_val_desc = var_val_desc + '.' + words1d[i]
    dd.vars[dd.vardict[varname]].valdict = [ var_low, var_high, var_val_desc ]
    
def process_line(p,ltype,varname='var'):
    words = p.split()
    
    if ltype == 'Blank':
        print("")
    elif ltype == 'Var Name':
        add_var_name(p)
    elif ltype == 'Var Desc':
        add_var_desc(p,varname)
    elif ltype == 'Var Value':
        add_var_value(p,varname)

if __name__ == '__main__':
    dd = DataDict('PUMS 2017')
    plist = ['PWGTP 5','Person Weight','-9999..9999 .Integerized Person Weight']
    pltype = 'Header'
    pvar = ''
    for p in plist:
        ltype = classify_line(p,pltype)
        process_line(p,ltype,varname=pvar)
        pltype = ltype
   
