"""

The DataDict class stores all information about each variable
block. It assumes that if a variable appears in both housing and
person records that they are defined in a consistent fashion.

The DataDict class is a set of VarInfo class objects along with
a helpful lookup dictionary (vardict) that maps the variable
name to the VarInfo class

The VarInfo class contains the initialization values that are
taken from the first line of the variable block in the data
dictionary. It then adds values or value ranges using a python
dictionary.

"""

import logging
from collections import OrderedDict

class VarInfo:
    """
    When initializing a variable, the name , type, and length is
    required
    """
    def __init__(self, name: str, vartype: str, varlen: int):
        self.name = name
        self.vartype = vartype
        self.varlen = varlen
        self.vardesc = ''
        self.vals = OrderedDict()

    def add_value(self, val_low: str, val_high: str, desc):
        """ Returns True if value/range added, False otherwise """
        if val_low == val_high or (val_low and not val_high):
            val = val_low
        else:
            val = val_low + '..' + val_high
        if val not in self.vals:
            self.vals[val] = desc
            return True
        else:
            logging.info('Value %s already exists for this variable, skipping.'\
                % val)
            return False


class DataDict:
    """
    Then the DataDict is initialized only a name is required.
    """
    def __init__(self, name):
        self.name = name
        self.vars = OrderedDict()
        return None

    def add_var(self, var, vartype, varlen):
        """ Returns True if var added, False otherwise """
        if var.upper() not in self.vars:
            newvar = VarInfo(var.upper(), vartype, varlen)
            self.vars[var.upper()] = newvar
            return True
        else:
            logging.info("Variable %s already is in the data dictionary." % var)
            return False


"""
The PUMSDict class stores the information on the layout. Basically
it will capture the title, release date, the major/minor headers for
record types, and the list of variables in order that they appear.

The classes below are cascading. PUMSDict includes the title, release
date, and the record types along with a map of record type name to
MajorRecordType class similar to the var map in DataDict.

MajorRecordType class then captures the name and description of the
record type. The name is a short version that contains only initials
whereas description contains the longer text that appears in the
document. It also provides the ability to add MinorRecordType
(sub-record type=srt) class entries along with a map of name to
MinorRecordType class similar to the other maps.

Finally, the MinorRecordType class stores the information on the list
of variables in the order that they appear. This is a much simpler
class since it only contains a short, abbreviated name, the full text
descriptions, and a python list of variables in their standard form.
"""

class MinorRecordType:
    """
    When a minor record type is initialized only the abbreviated
    name and full description is required.
    """
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.vars = []

    def add_var(self, var):
        """ Returns True if var added, False otherwise """
        if var.upper() not in self.vars:
            self.vars.append(var.upper())
            return True
        else:
            logging.warning('Variable %s already exists for this Minor Record Type.'
                % var)
            return False

class MajorRecordType:
    """
    When a major record type is initialized only the abbreviated
    name and full description is required.
    """
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.srts = OrderedDict()
        return None

    def add_srt(self, srt, sdesc):
        """ Returns True if srt added, False otherwise """
        newsrt = MinorRecordType(srt, sdesc)
        self.srts[srt] = newsrt
        return None

class PUMSDict:
    """
    When the PUMSDict is initialized only the name is required.
    """
    def __init__(self, name):
        self.name = name
        self.title = ''
        self.reldate = ''
        self.rts = OrderedDict()
        return None

    def add_rt(self, rt, desc):
        """ Returns True if rt added, False otherwise """
        newrt = MajorRecordType(rt, desc)
        self.rts[rt] = newrt
        return None
