class VarInfo:
    def __init__(self,name,vartype,varlen,vardesc):
        self.name = name
        self.vartype = vartype
        self.varlen  = varlen
        self.vardesc = vardesc
        self.valdict = {}

    def add_value(self,val_low,val_high,desc):
        if val_low == val_high or (val_low and not val_high):
            val = val_low
        else:
            val = val_low + '..' + val_high
        if val not in self.valdict.keys():
            self.valdict[val] = [ val_low, val_high, desc ]
            return True
        else:
            return False

class DataDict:
    def __init__(self,name):
        self.name = name
        self.vardict = {}
        self.vars = []

    def add_var(self,var):
        newvar = VarInfo(var)
        self.vars.append(newvar)
        self.vardict[var] = len(self.vars)
