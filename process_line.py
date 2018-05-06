from class_defs import *
from classify_line import classify_line

def add_header(p,pl):
    import re
    pparser = re.compile(r"[\t -]+")
    words = pparser.split(p)
    header = words[0] + ' ' + words[1]
    rt = words[0][0]
    if rt in ['H','P']:
        if len(words) == 2:
            if rt not in pl.rtdict.keys():
                pl.add_rt(rt,header)
                return rt
            else:
                print("NOTE: Duplicate Major Record Type -- Ignoring.")
                return rt
        elif len(words) > 2:
            if rt in pl.rtdict.keys():
                header = header + '-' + words[2]
                srt = words[2][0]
                for word in words[3:]:
                    header = header + ' ' + word
                    srt = srt + word[0]
                if srt not in pl.rts[pl.rtdict[rt]].srtdict.keys():
                    pl.rts[pl.rtdict[rt]].add_srt(srt,header)
                    return srt
                else:
                    print("NOTE: Duplicate Minor Record Type -- Ignoring.")
                    return srt
            else:
                print("ERROR: Record Minor Type with no Major Record Type defined.")
    return None
    
def add_var_name(p,dd,pl,lrt,lsrt):
    if lrt in pl.rtdict.keys():
        rt = pl.rts[pl.rtdict[lrt]]
        if lsrt in rt.srtdict.keys():
            srt = rt.srts[rt.srtdict[lsrt]]
        else:
            if rt.name not in rt.srtdict.keys():
                rt.add_srt(rt.name,rt.desc)
            srt = rt.srts[rt.srtdict[rt.name]]
        words = p.split(maxsplit=1)
        varname = words[0]
        varlen  = int(words[1])
        """
        WARNING: THE VARIABLE TYPE NEEDS TO BE UPDATED ONCE LAYOUT IS FINALIZED
        """
        vartype = 'C'
        if varname not in dd.vardict.keys():
            dd.add_var(varname,varlen)
            dd.vars[dd.vardict[varname]].vartype = vartype
        else:
            print("NOTE: Variable %s already defined in Data Dictionary." % varname)
        if varname not in srt.vars:
            srt.add_var(varname)
        else:
            print("ERROR: Variable %s already exists in Layout for %s." % (varname,srt.desc))
        return varname
    return None

def add_var_desc(p,dd,varname):
    if varname in dd.vardict.keys():
        v = dd.vars[dd.vardict[varname]]
        if p.strip() not in v.vardesc:
            v.vardesc = (v.vardesc + ' ' + p.strip()).strip()
            return varname
        else:
            print("ERROR: Possible duplication of variable description.")
    else:
        print("ERROR: Variable %s does not exist in the data dictionary." % varname)
    return None

def add_var_value(p,dd,varname):
    """ The parser creates a single split caused by required whitespace followed by a period """
    import re
    pparser = re.compile(r"[\t ]+\.")
    
    """ words will have [value range, value description] """
    words = pparser.split(p.rstrip(),maxsplit=1)

    """ Value range is either value_low..value_high or simply value_low """
    value_rng = words[0].split('..',maxsplit=1)
    value_low = value_rng[0]
    if len(value_rng) > 1:
        value_high = value_rng[1]
    else:
        value_high = None

    tmp = pparser.split(words[1])
    if len(tmp) == 1:
        value_desc = tmp
    elif len(tmp) > 1:
        value_desc = tmp[0]
        for i in range(1,len(tmp)):
            value_desc = value_desc + ' ' + tmp[i]
    value_desc = value_desc[0]
#    value_desc = words[1]

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
    tparser = re.compile(r"[\t ]*\.")
    pparser = re.compile(r"[\t ]+\.")
    
    """ words will have [empty string, value description] """
    twords = tparser.split(p,maxsplit=1)
    words = pparser.split(twords[1])

    """ FINISH """
    if varname in dd.vardict.keys():
        v = dd.vars[dd.vardict[varname]]
        if valname in v.valdict.keys():
            for i in range(len(words)):
                value_desc = words[i].strip()
                v.valdict[valname] = (v.valdict[valname] + ' ' + value_desc).strip()
            return True
    else:
        print("ERROR: Issue with assigning value description.")
    return False

def process_line(p,ltype,dd,pl,rt,srt,varname,valname):
    if ltype == 'Blank':
        return True
    elif ltype == 'Header':
        return add_header(p,pl)
    elif ltype == 'Var Name':
        return add_var_name(p,dd,pl,rt,srt)
    elif ltype == 'Var Desc':
        return add_var_desc(p,dd,varname)
    elif ltype == 'Var Value':
        return add_var_value(p,dd,varname)
    elif ltype == 'Val Desc':
        return add_val_desc(p,dd,varname,valname)
