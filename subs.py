def is_record_header(p):
    words = p.split()
    if len(words) > 1:
        if words[1][:6] == 'RECORD' and words[0] in ['HOUSING','PERSON']:
            return True
    return False
    
def is_var_name(p):
    words = p.split()
    if len(words) == 2:
        if p[0].isalpha() and words[0].isalnum() and words[0].isupper() and words[1].isdigit():
            return True
    return False

def is_var_desc(p,ptype):
    words = p.split('.')
    if ptype == 'Var Name':
        return True
    elif ptype == 'Var Desc' and len(words) == 1:
        return True
    return False

def is_val_desc(p,ptype):
    words = p.split('.')
    if len(words) > 1:
        if ptype in ['Var Name','Var Value']:
            return True
    return False

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


def classify_line(p,ptype):
    words = p.split()

    if not p:
        return 'Blank'
    elif is_record_header(p):
        return 'Header'
    elif is_var_name:
        return 'Var Name'
    elif is_var_desc(pltype):
        return 'Var Desc'
    elif is_val_desc(pltype):
        return 'Var Value'
    
def process_line(p,ltype):
    words = p.split()
    
    if ltype == 'Blank':
        print("")
    elif ltype == 'Var Name':
        add_var_name()
    elif ltype == 'Var Desc':
        add_var_desc()
    elif ltype == 'Var Value':
        add_var_value()

def main():
    dd = DataDict('PUMS 2017')

    # read par
    # p = par.text.strip()
            
if __name__ == '__main__':
    main()
