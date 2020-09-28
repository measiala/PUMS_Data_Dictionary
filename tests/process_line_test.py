#!/usr/bin/python3

import py.test
from process_line import *

dd = DataDict('PUMS 2017 Dictionary')
pl = PUMSDict('PUMS 2017 Layout')

def test_add_title():
    """ Test add title """
    assert add_title('2017 ACS PUMS Data Dictionary', pl) == '2017 ACS PUMS Data Dictionary'
    assert pl.title == '2017 ACS PUMS Data Dictionary'

    """ Should reject if already defined """
    assert add_title('2016 ACS PUMS Data Dictionary', pl) == None

def test_add_reldate():
    """ Test add release date """
    assert add_reldate('OCtobER 18, 2018', pl) == 'October 18, 2018'
    assert pl.reldate == 'October 18, 2018'

    """ Should reject if already defined """
    assert add_reldate('November 18, 2018', pl) == None

def test_add_header():
    """ Test add major header """
    assert add_header('HOUSING RECORD', pl) == 'H'
    assert len(pl.rts) == 1
    assert ('H' in pl.rts) == True

    """ Test add second header """
    assert add_header('PERSON RECORD', pl) == 'P'
    assert len(pl.rts) == 2
    assert ('P' in pl.rts) == True

    """ Verify order in dictionary """
    assert pl.rts['H'].name == list(pl.rts)[0]
    assert pl.rts['P'].name == list(pl.rts)[1]

    """ Check name """
    h = pl.rts['H']
    assert h.name == 'H'
    assert h.desc == 'HOUSING RECORD'

    """ Verify add subrecord type """
    assert add_header('HOUSING RECORD - BASIC VARIABLES', pl) == 'BV'
    assert len(h.srts) == 1
    assert ('BV' in h.srts) == True

    haf = h.srts['BV']
    assert haf.name == 'BV'
    assert haf.desc == 'HOUSING RECORD-BASIC VARIABLES'
    
def test_add_var_name():
    assert add_var_name('WGT Numeric 5', dd, pl, 'H', 'BV') == 'WGT'

    """ Verify var added to DataDict """
    assert ('WGT' in dd.vars) == True

    v1 = dd.vars['WGT']
    assert v1.name == 'WGT'
    assert v1.varlen == 5
    assert v1.vartype == 'N'

    """ Verify var added to PUMSDict """
    assert ('WGT' in pl.rts['H'].srts['BV'].vars) \
        == True

    """ Test character variable """
    assert add_var_name('AGS Character 1', dd, pl, 'H', 'BV') == 'AGS'
    assert ('AGS' in dd.vars) == True
    assert ('AGS' in pl.rts['H'].srts['BV'].vars) \
        == True

    v2 = dd.vars['AGS']
    assert v2.name == 'AGS'
    assert v2.varlen == 1
    assert v2.vartype == 'C'

def test_add_var_desc():
    """ Test add variable description """
    v = dd.vars['WGT']
    
    assert add_var_desc('Housing ', dd, 'WGT') == 'WGT'
    assert v.vardesc == 'Housing'

    """ Test add second line """
    assert add_var_desc(' Unit Weight', dd, 'WGT') == 'WGT'
    assert v.vardesc == 'Housing Unit Weight'

    """ Test prevention against duplication """
    assert add_var_desc('Housing Unit Weight', dd, 'WGT') == 'WGT'
    assert add_var_desc('HousingUnit Weight', dd, 'WGT') == 'WGT'

    assert add_var_desc('Person', dd, 'PWGT') == None
    
def test_add_var_value():
    """ Test single value """
    v1 = dd.vars['WGT']
    assert add_var_value('00000 .Vacant HU.', dd, 'WGT') == '00000'
    assert v1.vals['00000'] == 'Vacant HU.'

    """ Test range value """
    assert add_var_value('-9999..09999 .Integerized  ', dd, 'WGT') == '-9999..09999'
    assert v1.vals['-9999..09999'] == 'Integerized'

    """ Test complex variable value description and cleanup """
    assert add_var_value('00324 .Hello .Goodbye', dd, 'WGT') == '00324'
    assert v1.vals['00324'] == 'Hello Goodbye'

    """ Test cannot add value to nonexistent variable """
    assert add_var_value('0 .Vacant HU.', dd, 'WGTP') == None

    """ Test blank value standardization """
    v2 = dd.vars['AGS']
    assert add_var_value('B .N/A', dd, 'AGS') == 'B'
    assert ('b' in v2.vals) == True
    assert ('B' in v2.vals) == False
    assert v2.vals['b'] == 'N/A'

def test_add_val_desc():
    """ Test cannot append description to value of nonexistent variable """
    assert add_val_desc('.Weight', dd, 'WGTP', '0') == None

    """ Test cannot append description to nonexistent value """
    v = dd.vars['WGT']
    assert add_val_desc('.Weight', dd, 'WGT', '314') == None

    """ Test can append descriptiont to value and have extraneous space removed """
    assert add_val_desc('.Weight', dd, 'WGT', '-9999..09999') == '-9999..09999'
    assert v.vals['-9999..09999'] == 'Integerized Weight'

def test_process_line():
    """ Process typical lines """
    assert process_line('2017 ACS PUMS DATA DICTIONARY', 'Title', dd, pl, '', '', '', '') == None
    assert process_line('October 18, 2018', 'Rel Date', dd, pl, '', '', '', '') == None
    assert process_line('HOUSING RECORDS', 'Header', dd, pl, '', '', '', '') == 'H'
    assert process_line('HOUSING RECORDS-BASIC VARIABLES', 'Header', dd, pl, 'H', '', '', '') == 'BV'
    assert process_line('WGTP Numeric 4', 'Var Name', dd, pl, 'H', 'BV', '', '') == 'WGTP'
    assert process_line('Housing Unit Weight', 'Var Desc', dd, pl, 'H', 'BV', 'WGTP', '') == 'WGTP'
    assert process_line('1..9999 .Integerized', 'Var Value', dd, pl, 'H', 'BV', 'WGTP', '') == '1..9999'
    assert process_line('.Weight ', 'Val Desc', dd, pl, 'H', 'BV', 'WGTP', '1..9999') == '1..9999'
    assert process_line('.Weight ', 'Val Desc', dd, pl, 'H', 'BV', 'WGTP', '') == None
    assert process_line('.Weight ', 'Val Desc', dd, pl, 'H', 'BV', 'WGTP', '-100..-1') == None
    assert process_line('0 .GQ Unit', 'Var Value', dd, pl, 'H', 'BV', 'WGTP', '1..9999') == '0'

    """ Check full dd entry for WGTP """
    assert dd.vars['WGTP'].name == 'WGTP'
    assert dd.vars['WGTP'].vardesc == 'Housing Unit Weight'
    assert dd.vars['WGTP'].varlen  == 4
    assert dd.vars['WGTP'].vartype == 'N'
    assert dd.vars['WGTP'].vals == {'1..9999': 'Integerized Weight', '0': 'GQ Unit'}
