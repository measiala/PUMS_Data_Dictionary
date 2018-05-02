#!/usr/bin/python3

import pytest

from main import *

class fakeparse:
    def __init__(self,yyyy,period):
        self.yyyy = yyyy
        self.period = period
        self.ifile = ''

args = fakeparse(2017,1)
