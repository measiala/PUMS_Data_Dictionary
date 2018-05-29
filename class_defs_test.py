import pytest

from class_defs import *

pd = PUMSDict('2017 1-year DD')
dd = DataDict('2017 1-year Variable Dictionary')

def test_PUMSDict():
    """ Test initialization """
    assert pd.name == '2017 1-year DD'
    assert len(pd.rts) == 0

    """ Test adding Major Record Types """
    pd.add_rt('H','Housing Record')
    assert len(pd.rts) == 1
    assert ('H' in pd.rtdict.keys()) == True
    
    pd.add_rt('P','Person Record')
    assert len(pd.rts) == 2
    assert ('P' in pd.rtdict.keys()) == True

    assert pd.rtdict['H'] == 0
    assert pd.rtdict['P'] == 1

    assert pd.rts[pd.rtdict['H']].name == 'H'
    assert pd.rts[pd.rtdict['P']].name == 'P'

    assert pd.rts[pd.rtdict['H']].desc == 'Housing Record'
    assert pd.rts[pd.rtdict['P']].desc == 'Person Record'

def test_MajorRecordType():
    h = pd.rts[pd.rtdict['H']]
    assert len(h.srts) == 0

    """ Test adding Minor Record Types """
    h.add_srt('HB','Basic Variables')
    assert len(h.srts) == 1
    assert ('HB' in h.srtdict.keys()) == True
    
    h.add_srt('HU','Housing Unit Variables')
    assert len(h.srts) == 2
    assert ('HU' in h.srtdict.keys()) == True

    assert h.srtdict['HB'] == 0
    assert h.srtdict['HU'] == 1

    assert h.srts[h.srtdict['HB']].name == 'HB'
    assert h.srts[h.srtdict['HU']].name == 'HU'

    assert h.srts[h.srtdict['HB']].desc == 'Basic Variables'
    assert h.srts[h.srtdict['HU']].desc == 'Housing Unit Variables'
    
def test_MinorRecordType():
    h = pd.rts[pd.rtdict['H']]
    hb = h.srts[h.srtdict['HB']]

    assert len(hb.vars) == 0

    """ Test adding variables """
    hb.add_var('ST')
    assert len(hb.vars) == 1
    assert hb.vars == ['ST']
    
    hb.add_var('PUMA')
    assert len(hb.vars) == 2
    assert hb.vars == ['ST','PUMA']

def test_DataDict():
    """ Test initialization """
    assert dd.name == '2017 1-year Variable Dictionary'
    assert len(dd.vars) == 0

    """ Test add variable """
    dd.add_var('ST','C',2)
    assert len(dd.vars) == 1
    assert ('ST' in dd.vardict.keys()) == True

    dd.add_var('PUMA','C',5)
    assert len(dd.vars) == 2
    assert ('PUMA' in dd.vardict.keys()) == True

    assert dd.vardict['ST'] == 0
    assert dd.vardict['PUMA'] == 1

    v1 = dd.vars[dd.vardict['ST']]
    v2 = dd.vars[dd.vardict['PUMA']]
    
    assert v1.name == 'ST'
    assert v2.name == 'PUMA'

    assert v1.vartype == 'C'
    assert v2.vartype == 'C'
    
    assert v1.varlen == 2
    assert v2.varlen == 5

    assert len(v1.vardesc) == 0
    assert len(v2.vardesc) == 0

def test_VarInfo():
    st = dd.vars[dd.vardict['ST']]

    st.vardesc = '2010 Census based State FIPS Code'

    assert st.vardesc == '2010 Census based State FIPS Code'

    st.add_value('01','06','Acceptable State Range 1')
    assert ('01..06' in st.valdict.keys()) == True
    
    st.add_value('07','','Out of Scope - American Samoa')
    assert ('07' in st.valdict.keys()) == True

    assert st.valdict['01..06'] == 'Acceptable State Range 1'
    assert st.valdict['07'] == 'Out of Scope - American Samoa'
