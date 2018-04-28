#!/usr/bin/python3

import pytest

from main import *

class fakeparse:
    def __init__(self,yyyy,period):
        self.yyyy = yyyy
        self.period = period
        self.ifile = ''

args = fakeparse(2017,1)

def test_assign_yyyy():
    args.yyyy = 1999
    assert assign_yyyy(args) == None
    args.yyyy = 2000
    assert assign_yyyy(args) == 2000
    args.yyyy = 2006
    assert assign_yyyy(args) == 2006
    args.yyyy = 2007
    assert assign_yyyy(args) == 2007
    args.yyyy = 2008
    assert assign_yyyy(args) == 2008
    args.yyyy = 2009
    assert assign_yyyy(args) == 2009
    args.yyyy = 2013
    assert assign_yyyy(args) == 2013
    args.yyyy = 2014
    assert assign_yyyy(args) == 2014
    args.yyyy = 2017
    assert assign_yyyy(args) == 2017
    args.yyyy = 2018
    assert assign_yyyy(args) == None

def test_assign_period():
    args.period = 1
    args.yyyy = 1999
    assert assign_period(args) == None
    args.yyyy = 2000
    assert assign_period(args) == 1

    args.period = 3
    args.yyyy = 2006
    assert assign_period(args) == None
    args.yyyy = 2007
    assert assign_period(args) == 3
    args.yyyy = 2008
    assert assign_period(args) == 3
    args.yyyy = 2009
    assert assign_period(args) == 3
    args.yyyy = 2013
    assert assign_period(args) == 3
    args.yyyy = 2014
    assert assign_period(args) == None

    args.period = 5
    args.yyyy = 2008
    assert assign_period(args) == None
    args.yyyy = 2009
    assert assign_period(args) == 5
    args.yyyy = 2017
    assert assign_period(args) == 5
    args.yyyy = 2018
    assert assign_period(args) == None

def test_assign_infile():
    """ Add here """
