class VarInfo:
    def __init__(self,name: str,varlen: int):
        self.name = name
        self.vartype = ''
        self.varlen  = varlen
        self.vardesc = ''
        self.valdict = {}

    def add_value(self,val_low: str,val_high: str,desc):
        if val_low == val_high or (val_low and not val_high):
            val = val_low
        else:
            val = val_low + '..' + val_high
        if val not in self.valdict.keys():
            self.valdict[val] = desc
            return True
        else:
            return False

class DataDict:
    def __init__(self,name):
        self.name = name
        self.vardict = {}
        self.vars = []

    def add_var(self,var,varlen):
        if var not in self.vars:
            newvar = VarInfo(var,varlen)
            self.vars.append(newvar)
            self.vardict[var] = len(self.vars) - 1
        else:
            print("Variable " + var + " already is in the data dictionary.")

class MinorRecordType:
    def __init__(self,name,desc):
        self.name = name
        self.desc = desc
        self.vars = []

    def add_var(self,var):
        if var not in self.vars:
            self.vars.append(var)
        else:
            print('Variable ' + var + ' already exists for this Minor Record Type.')

class MajorRecordType:
    def __init__(self,name,desc):
        self.name = name
        self.desc = desc
        self.srts = []
        self.srtdict = {}

    def add_srt(self,srt,sdesc):
        newsrt = MinorRecordType(srt,sdesc)
        self.srts.append(newsrt)
        self.srtdict[srt] = len(self.srts) - 1

class PUMSDict:
    def __init__(self,name):
        self.name = name
        self.rts = []
        self.rtdict = {}

    def add_rt(self,rt,desc):
        newrt = MajorRecordType(rt,desc)
        self.rts.append(newrt)
        self.rtdict[rt] = len(self.rts) - 1
