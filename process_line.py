import logging
from class_defs import *
from classify_line import classify_line

def add_title(p, pl):
    if not pl.title.strip():
        pl.title = p
        return p
    else:
        logging.error("Title is already defined.")
    return None

def add_reldate(p, pl):
    if not pl.reldate.strip():
        words = p.split()
        mm = words[0].title()
        dd = words[1].strip(',') + ','
        yyyy = words[2]
        reldate = mm + ' ' + dd + ' ' + yyyy
        pl.reldate = reldate
        return reldate
    else:
        logging.error("Release Date is already defined.")     
    return None

def add_header(p, pl):
    import re
    pparser = re.compile(r"[\t -]+")
    words = pparser.split(p)
    header = words[0] + ' ' + words[1]
    rt = words[0][0]
    if rt in ['H', 'P']:
        if len(words) == 2:
            if rt not in pl.rts:
                pl.add_rt(rt, header)
                return rt
            else:
                logging.info("Duplicate Major Record Type -- Ignoring.")
                return rt
        elif len(words) > 2:
            if rt in pl.rts:
                header = header + '-' + words[2]
                srt = words[2][0]
                for word in words[3:]:
                    header = header + ' ' + word
                    srt = srt + word[0]
                if srt not in pl.rts[rt].srts:
                    pl.rts[rt].add_srt(srt, header)
                    return srt
                else:
                    logging.info("Duplicate Minor Record Type -- Ignoring.")
                    return srt
            else:
                logging.error("Record Minor Type with no Major Record Type defined.")
    return None
    
def add_var_name(p, dd, pl, lrt, lsrt):
    if lrt in pl.rts:
        rt = pl.rts[lrt]
        if lsrt in rt.srts:
            srt = rt.srts[lsrt]
        else:
            if rt.name not in rt.srts:
                rt.add_srt(rt.name, rt.desc)
            srt = rt.srts[rt.name]
        words = p.split(maxsplit=2)
        varname = words[0]
        vartype = words[1].upper()[0]
        varlen  = int(words[2])
        if varname not in dd.vars:
            dd.add_var(varname, vartype, varlen)
        else:
            logging.info("Variable %s already defined in Data Dictionary." % varname)
        if varname not in srt.vars:
            srt.add_var(varname)
        else:
            logging.error("Variable %s already exists in Layout for %s." % (varname, srt.desc))
        return varname
    return None

def add_var_desc(p, dd, varname):
    if varname in dd.vars:
        v = dd.vars[varname]
        if p.replace(' ', '') not in v.vardesc.replace(' ', ''):
            v.vardesc = (v.vardesc + ' ' + p.strip()).strip()
            return varname
        else:
            logging.warning("Possible duplication in variable description for %s ignored."
                  % varname)
            return varname
    else:
        logging.error("Variable %s does not exist in the data dictionary." % varname)
    return None

def add_var_value(p, dd, varname):
    """ The parser creates a single split caused by required whitespace followed by a period """
    import re
    pparser = re.compile(r"[\t ]+\.")
    
    """ words will have [value range, value description] """
    words = pparser.split(p.rstrip(), maxsplit=1)

    """ Value range is either value_low..value_high or simply value_low """
    value_rng = words[0].split('..', maxsplit=1)
    value_low = value_rng[0]
    if len(value_rng) > 1:
        value_high = value_rng[1]
    else:
        value_high = None

    """ Standardize blank value of all b/B to lowercase """ 
    if value_high == None:
        """ If value_low contains only lower- and uppercase b s """
        if bool(re.match('^[bB]+$', value_low)):
            value_low = value_low.lower()
        
    tmp = pparser.split(words[1])
    value_desc = ' '.join(tmp)

    """ FINISH """
    if varname in dd.vars:
        d = dd.vars[varname]
        if len(value_low) > d.varlen or (value_high != None and len(value_high) > d.varlen):
            logging.error("Value %s or %s may be smaller than prescribed length of %d."
                  % (value_low, value_high, d.varlen))
            return None
        elif len(value_low) < d.varlen or (value_high != None and len(value_high) < d.varlen):
            logging.info("Value %s or %s may be smaller than prescribed length of %d."
                  % (value_low, value_high, dd.vars[varname].varlen))
            
        d.add_value(value_low, value_high, value_desc)
        return words[0]
    else:
        logging.error("Issue with assigning variable value.")
    return None
    
def add_val_desc(p, dd, varname, valname):
    """ The parser causes a single split caused by optional white space followed by a period """
    import re
    """ tparser has optional whitespace """
    tparser = re.compile(r"[\t ]*\.")
    """ pparser has required whitespace """
    pparser = re.compile(r"[\t ]+\.")
    
    """ words will have [empty string, value description] """
    twords = tparser.split(p, maxsplit=1)
    words = pparser.split(twords[1])

    """ FINISH """
    if varname in dd.vars:
        v = dd.vars[varname]
        if valname in v.vals:
            for i in range(len(words)):
                value_desc = words[i].strip()
                v.vals[valname] = (v.vals[valname] + ' ' + value_desc).strip()
            return valname
    else:
        logging.error("Issue with assigning value description.")
    return None

def process_line(p, ltype, dd, pl, rt, srt, varname, valname):
    if ltype == 'Blank':
        return True
    elif ltype == 'Title':
        return add_title(p, pl)
    elif ltype == 'Rel Date':
        return add_reldate(p, pl)
    elif ltype == 'Header':
        return add_header(p, pl)
    elif ltype == 'Var Name':
        return add_var_name(p, dd, pl, rt, srt)
    elif ltype == 'Var Desc':
        return add_var_desc(p, dd, varname)
    elif ltype == 'Var Value':
        return add_var_value(p, dd, varname)
    elif ltype == 'Val Desc':
        return add_val_desc(p, dd, varname, valname)
    return None
