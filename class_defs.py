class HeaderInfo:
    def __init__(self,name: str,level: int,htype: str,pos: int):
        self.name = name
        self.level = level
        self.htype = htype
        self.pos = pos

class VarInfo:
    def __init__(self,name: str):
        self.name = name
        self.vartype = ''
        self.varlen  = int
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
        self.hdrdict = {}
        self.headers = []

    def add_header(self,header,level,htype,pos):
        newheader = HeaderInfo(header,level,htype,pos)
        self.headers.append(newheader)
        self.hdrdict[header] = len(self.headers) -1
        
    def add_var(self,var):
        newvar = VarInfo(var)
        self.vars.append(newvar)
        self.vardict[var] = len(self.vars) - 1

if __name__ == "__main__":
    dd = DataDict('Test')

    dd.add_var('PWGT')
    v = dd.vars[dd.vardict['PWGT']]
    print(v)
    v.varlen = 5
    v.vartype = 'N'
    v.vardesc = 'Person Weight'
    
    v.add_value('-9999','9999','Integerized Person Weight')

    print(v.name, v.vartype, v.varlen, v.vardesc, v.valdict['-9999..9999'])
