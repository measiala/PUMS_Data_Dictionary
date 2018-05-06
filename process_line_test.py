#!/usr/bin/python3

import py.test
from process_line import *

dd = DataDict('PUMS 2017 Dictionary')
pl = PUMSDict('PUMS 2017 Layout')

def test_add_header():
    assert add_header('HOUSING RECORD',pl) == 'H'
    assert len(pl.rts) == 1
    assert ('H' in pl.rtdict.keys()) == True

    assert add_header('PERSON RECORD',pl) == 'P'
    assert len(pl.rts) == 2
    assert ('P' in pl.rtdict.keys()) == True

    h = pl.rts[pl.rtdict['H']]
    assert pl.rtdict['H'] == 0
    assert h.name == 'H'
    assert h.desc == 'HOUSING RECORD'
    
    assert pl.rtdict['P'] == 1
  
    assert add_header('HOUSING RECORD - BASIC VARIABLES',pl) == 'BV'
    assert len(h.srts) == 1
    assert ('BV' in h.srtdict.keys()) == True

    haf = h.srts[h.srtdict['BV']]
    assert haf.name == 'BV'
    assert haf.desc == 'HOUSING RECORD-BASIC VARIABLES'
    
def test_add_var_name():
    assert add_var_name('WGT 5',dd,pl,'H','BV') == 'WGT'
    assert ('WGT' in dd.vardict.keys()) == True
    assert ('WGT' in pl.rts[pl.rtdict['H']].srts[pl.rts[pl.rtdict['H']].srtdict['BV']].vars) == True

    v = dd.vars[dd.vardict['WGT']]
    assert v.name == 'WGT'
    assert v.varlen == 5
    assert v.vartype == 'C'  # This is hard coded at the moment

def test_add_var_desc():
    v = dd.vars[dd.vardict['WGT']]
    
    assert add_var_desc('Housing ',dd,'WGT') == 'WGT'
    assert v.vardesc == 'Housing'
    assert add_var_desc(' Unit Weight',dd,'WGT') == 'WGT'
    assert v.vardesc == 'Housing Unit Weight'

    assert add_var_desc('Person',dd,'PWGT') == None
    
def test_add_var_value():
    v = dd.vars[dd.vardict['WGT']]
    assert add_var_value('0 .Vacant HU.',dd,'WGT') == '0'
    assert v.valdict['0'] == 'Vacant HU.'

    assert add_var_value('-9999..09999 .Integerized  ',dd,'WGT') == '-9999..09999'
    assert v.valdict['-9999..09999'] == 'Integerized'

    assert add_var_value('0 .Vacant HU.',dd,'WGTP') == None
    
def test_add_val_desc():
    v = dd.vars[dd.vardict['WGT']]
    assert add_val_desc('.Weight',dd,'WGT','314') == False

    assert add_val_desc('.Weight',dd,'WGT','-9999..09999') == True
    assert v.valdict['-9999..09999'] == 'Integerized Weight'
    
    assert add_val_desc('.Weight',dd,'WGTP','0') == False

def test_process_line():
    assert process_line('HOUSING RECORDS','Header',dd,pl,'','','','') == 'H'
    assert process_line('HOUSING RECORDS-BASIC VARIABLES','Header',dd,pl,'H','','','') == 'BV'
    assert process_line('WGTP 4','Var Name',dd,pl,'H','BV','','') == 'WGTP'
    assert process_line('Housing Unit Weight','Var Desc',dd,pl,'H','BV','WGTP','') == 'WGTP'
    assert process_line('1..9999 .Integerized','Var Value',dd,pl,'H','BV','WGTP','') == '1..9999'
    assert process_line('.Weight ','Val Desc',dd,pl,'H','BV','WGTP','1..9999') == True
    assert process_line('.Weight ','Val Desc',dd,pl,'H','BV','WGTP','') == False
    assert process_line('.Weight ','Val Desc',dd,pl,'H','BV','WGTP','-100..-1') == False
    assert process_line('0 .GQ Unit','Var Value',dd,pl,'H','BV','WGTP','1..9999') == '0'
    
    assert dd.vars[dd.vardict['WGTP']].name == 'WGTP'
    assert dd.vars[dd.vardict['WGTP']].vardesc == 'Housing Unit Weight'
    assert dd.vars[dd.vardict['WGTP']].varlen  == 4
    assert dd.vars[dd.vardict['WGTP']].valdict == {'1..9999': 'Integerized Weight','0': 'GQ Unit'}
