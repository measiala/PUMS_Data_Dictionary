#!/usr/bin/python3

import sys
#from string import maketrans

import py.test
import textwrap

from print_txt import *

def test_print_line():
    assert print_line('foo.bar',ofile='print',platform='unix') == 'foo.bar'
    assert print_line('This is “foo” bar',ofile='print',platform='unix') == 'This is "foo" bar'
    assert print_line("I can’t take this",ofile='print',platform='unix') == "I can't take this"
    assert print_line("Stop—–Hammer time",ofile='print',platform='unix') == "Stop--Hammer time"

    assert print_line('foo.bar') == 'foo.bar'

def test_print_title():
    assert print_title('abc 123',ofile='print') == 'abc 123'

def test_print_reldate():
    assert print_reldate('abc 123',ofile='print') == 'abc 123\n'

# def test_print_record_type():
#     assert print_record_type('abc 123',ofile='print') == '\nabc 123'

def test_print_var_name():
    """ Check no-tab output """
    assert print_var_name('PWGTP',      'N',5,ofile='print',tabsep='NO') == '\nPWGTP       N           5'
    assert print_var_name('PWGTP80',    'N',5,ofile='print',tabsep='NO') == '\nPWGTP80     N           5'
    assert print_var_name('PWGTPWGTP',  'N',5,ofile='print',tabsep='NO') == '\nPWGTPWGTP   N           5'
    assert print_var_name('PWGTPWGTP80','N',5,ofile='print',tabsep='NO') == '\nPWGTPWGTP80 N           5'
    assert print_var_name('PWGTPWGTP801','N',5,ofile='print',tabsep='NO') == None

    """ Check tab output """
    assert print_var_name('PWGTP','N',5,ofile='print',tabsep='YES') == '\nPWGTP\tN\t5'
    assert print_var_name('PWGTP80','N',5,ofile='print',tabsep='YES') == '\nPWGTP80\tN\t5'
    assert print_var_name('PWGTPWGTP','N',5,ofile='print',tabsep='YES') == '\nPWGTPWGTP\tN\t5'
    assert print_var_name('PWGTPWGTP80','N',5,ofile='print',tabsep='YES') == '\nPWGTPWGTP80\tN\t5'
    assert print_var_name('PWGTPWGTP801','N',5,ofile='print',tabsep='YES') == None

    """ Check default is no tabs """
    assert print_var_name('PWGTP','N',5) == '\nPWGTP       N           5'

def test_print_var_desc():
    """ Verify indentation """
    assert print_var_desc('Person Weight',ofile='print',wrap_text='NO',indent='NO',tabindent='NO') \
        == 'Person Weight'
    assert print_var_desc('Person Weight',ofile='print',wrap_text='NO',indent='YES',tabindent='NO') \
        == '      Person Weight'
    assert print_var_desc('Person Weight',ofile='print',wrap_text='NO',indent='YES',tabindent='YES') \
        == '\tPerson Weight'
    assert print_var_desc('Person Weight',ofile='print',wrap_text='NO',indent='NO',tabindent='YES') \
        == 'Person Weight'

    """ Verify alternative output for wrap option, it is a list of lines """
    assert print_var_desc('Person Weight',ofile='print',wrap_text='YES',indent='NO',tabindent='NO') \
        == [ 'Person Weight' ]

    """ This line is 72 characters long and should not be wrapped """
    assert print_var_desc('Person Weight Person Weight Person Weight Person Weight Person Weight 12',\
                          ofile='print',wrap_text='NO',indent='NO',tabindent='NO') \
        == 'Person Weight Person Weight Person Weight Person Weight Person Weight 12'
    assert print_var_desc('Person Weight Person Weight Person Weight Person Weight Person Weight 12',\
                          ofile='print',wrap_text='YES',indent='NO',tabindent='NO') \
        == [ 'Person Weight Person Weight Person Weight Person Weight Person Weight 12' ]
    
    """ This line is 73 characters long and should wrap with option turned on """
    assert print_var_desc('Person Weight Person Weight Person Weight Person Weight Person Weight 123',\
                          ofile='print',wrap_text='NO',indent='NO',tabindent='NO') \
        == 'Person Weight Person Weight Person Weight Person Weight Person Weight 123'
    assert print_var_desc('Person Weight Person Weight Person Weight Person Weight Person Weight 123',\
                          ofile='print',wrap_text='YES',indent='NO',tabindent='NO') \
        == [ 'Person Weight Person Weight Person Weight Person Weight Person Weight','123' ]


    """ Check indentation combined with wrap text """
    assert print_var_desc('Person Weight Person Weight Person Weight Person Weight Person Weight 123',\
                          ofile='print',wrap_text='YES',indent='YES',tabindent='NO') \
        == [ '      Person Weight Person Weight Person Weight Person Weight Person Weight',
             '      123' ]
    assert print_var_desc('Person Weight Person Weight Person Weight Person Weight Person Weight 123',\
                          ofile='print',wrap_text='YES',indent='YES',tabindent='YES') \
        == [ '\tPerson Weight Person Weight Person Weight Person Weight Person Weight','\t123' ]

    assert print_var_desc('Person Weight',ofile='print',wrap_text='YES',indent='NO',tabindent='NO') \
        == print_var_desc('Person Weight')

def test_print_var_val():
    """ Test defaults """
    assert print_var_val('-9999..09999','Integerized Weights',5,
                         ofile='print',wrap_text='NO',tabindent='NO',tabsep='NO') \
                         == print_var_val('-9999..09999','Integerized Weights',5)

    """ Test standard indent and formatting for different length variables """
    assert print_var_val('-9999..09999','Integerized Weights',5) \
        == '            -9999..09999 .Integerized Weights'
    assert print_var_val('0','Integerized Weights',5) \
        == '            0            .Integerized Weights'
    assert print_var_val('0..9','Integerized Weights',1) \
        == '            0..9 .Integerized Weights'
    assert print_var_val('0','Integerized Weights',1) \
        == '            0    .Integerized Weights'

    """ Test tab indent """
    assert print_var_val('0..9','Integerized Weights',1,tabindent='YES') \
        == '\t\t0..9 .Integerized Weights'
    assert print_var_val('0','Integerized Weights',1,tabindent='YES') \
        == '\t\t0    .Integerized Weights'

    """ Test tab separator between var value and value desc """
    assert print_var_val('0..9','Integerized Weights',1,tabsep='YES') \
        == '            0..9\t.Integerized Weights'
    assert print_var_val('0','Integerized Weights',1,tabsep='YES') \
        == '            0\t.Integerized Weights'
    assert print_var_val('0..9','Integerized Weights',1,tabindent='YES',tabsep='YES') \
        == '\t\t0..9\t.Integerized Weights'
    assert print_var_val('0','Integerized Weights',1,tabindent='YES',tabsep='YES') \
        == '\t\t0\t.Integerized Weights'

    """ Test wrap text """
    assert \
        print_var_val('0..1',
                      'Person Weight Person Weight Person Weight Person Weight Person Weight 123',1,
                      wrap_text='NO') \
                      == '            0..1 .Person Weight Person Weight Person Weight Person Weight Person Weight 123'
    assert \
        print_var_val('0..1',
                      'Person Weight Person Weight Person Weight Person Weight Person Weight 123',1,
                      wrap_text='YES') \
                      == ['            0..1 .Person Weight Person Weight Person Weight Person Weight',
                          '                 .Person Weight 123']

def test_print_note():
    assert \
        print_note('Note: Person Weight Person Weight Person Weight Person Weight Person Weight 123',
                   ofile='print',wrap_text='NO') \
                   == '\nNote: Person Weight Person Weight Person Weight Person Weight Person Weight 123'
    assert \
        print_note('Note: Person Weight Person Weight Person Weight Person Weight Person Weight 123',
                   ofile='print',wrap_text='YES') \
                   == '\nNote: Person Weight Person Weight Person Weight Person Weight Person Weight\n123'
    assert \
        print_note('Note: Person Weight Person Weight Person Weight Person Weight Person Weight 123')\
        == '\nNote: Person Weight Person Weight Person Weight Person Weight Person Weight\n123'

  
