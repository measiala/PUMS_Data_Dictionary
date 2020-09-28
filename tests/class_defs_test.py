import pytest

from class_defs import *

pd = PUMSDict('2017 1-year DD')
dd = DataDict('2017 1-year Variable Dictionary')

def test_PUMSDict():
    """ Test initialization """
    assert pd.name == '2017 1-year DD'
    assert len(pd.rts) == 0
    assert pd.title == ''
    assert pd.reldate == ''

    """ Test adding Major Record Types """
    pd.add_rt('H','Housing Record')
    assert len(pd.rts) == 1
    assert ('H' in pd.rts) == True
    
    pd.add_rt('P','Person Record')
    assert len(pd.rts) == 2
    assert ('P' in pd.rts) == True

    """ rts should store the record types in order """
    assert pd.rts['H'].name == list(pd.rts.keys())[0]
    assert pd.rts['P'].name == list(pd.rts)[1]

    """ rts should be properly assigned """
    assert pd.rts['H'].name == 'H'
    assert pd.rts['P'].name == 'P'

    assert pd.rts['H'].desc == 'Housing Record'
    assert pd.rts['P'].desc == 'Person Record'

    """ Verify that title and date are stored as expected """
    pd.title = '2017 1-Year ACS PUMS Data Dictionary'
    pd.reldate = 'October 18, 2018'
    assert pd.title == '2017 1-Year ACS PUMS Data Dictionary'
    assert pd.reldate == 'October 18, 2018'
    
def test_MajorRecordType():
    """ Test initialization of Major Record Type """
    h = pd.rts['H']
    assert h.srts == OrderedDict()

    """ Test adding Minor Record Types """
    assert h.add_srt('HB','Basic Variables') == None
    assert len(h.srts) == 1
    assert ('HB' in h.srts.keys()) == True
    
    assert h.add_srt('HU','Housing Unit Variables') == None
    assert len(h.srts) == 2
    assert ('HU' in h.srts.keys()) == True

    """ srts should store the record types in order """
    assert h.srts['HB'].name == list(h.srts)[0]
    assert h.srts['HU'].name == list(h.srts)[1]

    """ srts should be properly assigned """
    assert h.srts['HB'].name == 'HB'
    assert h.srts['HU'].name == 'HU'

    assert h.srts['HB'].desc == 'Basic Variables'
    assert h.srts['HU'].desc == 'Housing Unit Variables'
    
def test_MinorRecordType():
    h = pd.rts['H']
    hb = h.srts['HB']

    """ Test initialization of Minor Record Type """
    assert hb.vars == []

    """ Test adding variables to Minor Record Type """
    assert hb.add_var('st') == True
    assert len(hb.vars) == 1

    """ Added variable is uppercase """
    assert hb.vars == ['ST']
    
    """ Add second variable """
    assert hb.add_var('PUMA') == True
    assert len(hb.vars) == 2
    assert hb.vars == ['ST','PUMA']

    """ Check for duplication is case insensitive """
    assert hb.add_var('St') == False
    assert len(hb.vars) == 2
    assert hb.vars == ['ST','PUMA']

def test_DataDict():
    """ Test initialization """
    assert dd.name == '2017 1-year Variable Dictionary'
    assert dd.vars == OrderedDict()
    assert len(dd.vars) == 0

    """ Test add variable, variables should be stored in upper case """
    assert dd.add_var('St', 'C', 2) == True
    assert len(dd.vars) == 1
    assert ('ST' in dd.vars) == True

    assert dd.add_var('PUMA', 'C', 5) == True
    assert len(dd.vars) == 2
    assert ('PUMA' in dd.vars) == True

    """ add_var should reject duplicates ignoring input case"""
    assert dd.add_var('st', 'C', 2) == False
    
    """ Variables should be added in order """
    assert dd.vars['ST'].name == list(dd.vars)[0]
    assert dd.vars['PUMA'].name == list(dd.vars)[1]

    """ Verify proper assignment """
    v1 = dd.vars['ST']
    v2 = dd.vars['PUMA']
    
    assert v1.name == 'ST'
    assert v2.name == 'PUMA'

    assert v1.vartype == 'C'
    assert v2.vartype == 'C'
    
    assert v1.varlen == 2
    assert v2.varlen == 5

    assert len(v1.vardesc) == 0
    assert len(v2.vardesc) == 0

def test_VarInfo():
    """ Test initialization, main items tested above """
    st = dd.vars['ST']
    assert st.vardesc == ''
    assert st.vals == OrderedDict()

    """ Test adding variable description """
    st.vardesc = '2010 Census based State FIPS Code'
    assert st.vardesc == '2010 Census based State FIPS Code'

    """ Test adding values """
    assert st.add_value('01','06','Acceptable State Range 1') == True
    assert ('01..06' in st.vals) == True
    
    assert st.add_value('07','','Out of Scope - American Samoa') == True
    assert ('07' in st.vals) == True

    """ Trying to add a duplicate value should be rejected """
    assert st.add_value('07', '', 'Out of Scope - American Samoa') == False

    """ Note that singular values that exist within a defined range are not rejected 
    This could be a worthwhile improvement """
    assert st.add_value('02', '02', 'Alaska') == True
    
    assert st.vals['01..06'] == 'Acceptable State Range 1'
    assert st.vals['07'] == 'Out of Scope - American Samoa'
    assert list(st.vals) == ['01..06', '07', '02']
