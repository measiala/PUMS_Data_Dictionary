#!/usr/bin/python3

import py.test
from process_line import *

dd = DataDict('PUMS 2017')

def test_add_header():
    assert add_header('HOUSING RECORD',dd) == 0
    assert len(dd.headers) == 1
    assert dd.headers[-1].name == 'HOUSING RECORD'
    assert dd.headers[-1].level == 1
    assert dd.headers[-1].htype == 'H'
    assert dd.headers[-1].pos == 0
    assert add_header('HOUSING RECORD - ALLOCATION',dd) == 0
    assert len(dd.headers) == 2
    assert dd.headers[-1].name == 'HOUSING RECORD-ALLOCATION'
    assert dd.headers[-1].level == 2
    assert dd.headers[-1].htype == 'H'
    assert dd.headers[-1].pos == 0    
    assert add_header('HOUSING RECORD  -- ALLOCATION',dd) == 0
    assert len(dd.headers) == 3
    assert dd.headers[-1].name == 'HOUSING RECORD-ALLOCATION'
    assert dd.headers[-1].level == 2
    assert dd.headers[-1].htype == 'H'
    assert dd.headers[-1].pos == 0    
    assert add_header('PERSON RECORD - ALLOCATION VARIABLES',dd) == 0
    assert len(dd.headers) == 4
    assert dd.headers[-1].name == 'PERSON RECORD-ALLOCATION VARIABLES'
    assert dd.headers[-1].level == 2
    assert dd.headers[-1].htype == 'P'
    assert dd.headers[-1].pos == 0    
    
def test_add_var_name():
    assert add_var_name('PWGT 5',dd) == 'PWGT'
    assert dd.vardict['PWGT'] == 0
    assert dd.vars[0].name == 'PWGT'
    assert dd.vars[0].varlen == 5
    assert add_var_name('PWGT 5',dd) == None

    assert add_var_name('PWGTP 5',dd) == 'PWGTP'
    assert dd.vardict['PWGTP'] == 1

def test_add_var_desc():
    assert add_var_desc('Original ',dd,'PWGT') == True
    assert dd.vars[0].vardesc == 'Original'
    assert add_var_desc('Person Weight',dd,'PWGT') == True
    assert dd.vars[0].vardesc == 'Original Person Weight'
    
    assert add_var_desc('PUMS Person Weight',dd,'PWGTP') == True
    assert dd.vars[1].vardesc == 'PUMS Person Weight'

    assert add_var_desc('Bogus Person Weight',dd,'BPWGT') == False

def test_add_var_value():
    assert add_var_value('0 .Vacant HU.',dd,'PWGT') == '0'
    assert dd.vars[0].valdict['0'] == 'Vacant HU.'

    assert add_var_value('-9999..09999 .Integerized',dd,'PWGTP') == '-9999..09999'
    assert dd.vars[1].valdict['-9999..09999'] == 'Integerized'
    
def test_add_val_desc():
    assert add_val_desc('.Weight',dd,'PWGT','314') == False

    assert add_val_desc('.Weight',dd,'PWGTP','-9999..09999') == True
    assert dd.vars[1].valdict['-9999..09999'] == 'Integerized Weight'
    
    assert add_val_desc('.Weight',dd,'PWGTP','0') == False

def test_process_line():
    assert process_line('WGT 4',dd,'Var Name','','') == 'WGT'
    assert process_line('Housing Unit Weight',dd,'Var Desc','WGT','') == True
    assert process_line('1..9999 .Integerized',dd,'Var Value','WGT','') == '1..9999'
    assert process_line('.Weight ',dd,'Val Desc','WGT','1..9999') == True
    assert process_line('.Weight ',dd,'Val Desc','WGT','') == False
    assert process_line('.Weight ',dd,'Val Desc','WGT','-100..-1') == False
    assert process_line('0 .GQ Unit',dd,'Var Value','WGT','1..9999') == '0'
    
    assert dd.vars[dd.vardict['WGT']].name == 'WGT'
    assert dd.vars[dd.vardict['WGT']].vardesc == 'Housing Unit Weight'
    assert dd.vars[dd.vardict['WGT']].varlen  == 4
    assert dd.vars[dd.vardict['WGT']].valdict == {'1..9999': 'Integerized Weight','0': 'GQ Unit'}
