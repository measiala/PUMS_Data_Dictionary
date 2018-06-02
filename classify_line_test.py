import py.test

from classify_line import *

def test_is_title():
    """ Test variations of titles, upper and lower case """
    assert is_title("2017 ACS PUMS Data Dictionary","None") == True
    assert is_title("2017 ACS 1-Year PUMS Data Dictionary","None") == True
    assert is_title("2017 ACS PUMS DATA DICTIONARY","None") == True
    assert is_title("2017 acs pums data dictionary","None") == True
    assert is_title("2013-2017 ACS 5-Year PUMS Data Dictionary","None") == True

    """ Test variations of titles that omit a key word """
    assert is_title("2017 PUMS Data Dictionary","None") == False
    assert is_title("2017 ACS Data Dictionary","None") == False
    assert is_title("2017 ACS PUMS Dictionary","None") == False
    assert is_title("2017 ACS PUMS Data","None") == False

    """ Test fixed title with other preceding line types """
    assert is_title("2017 ACS PUMS Data Dictionary","Blank") == True
    assert is_title("2017 ACS PUMS Data Dictionary","Title") == False
    assert is_title("2017 ACS PUMS Data Dictionary","Rel Date") == False
    assert is_title("2017 ACS PUMS Data Dictionary","Header") == False
    assert is_title("2017 ACS PUMS Data Dictionary","Var Name") == False
    assert is_title("2017 ACS PUMS Data Dictionary","Var Desc") == False
    assert is_title("2017 ACS PUMS Data Dictionary","Var Value") == False
    assert is_title("2017 ACS PUMS Data Dictionary","Val Desc") == False

def test_is_reldate():
    """ Test all months in title case """
    assert is_reldate("January 18, 2018",'Title') == True
    assert is_reldate("February 18, 2018",'Title') == True
    assert is_reldate("March 18, 2018",'Title') == True
    assert is_reldate("April 18, 2018",'Title') == True
    assert is_reldate("May 18, 2018",'Title') == True
    assert is_reldate("June 18, 2018",'Title') == True
    assert is_reldate("July 18, 2018",'Title') == True
    assert is_reldate("August 18, 2018",'Title') == True
    assert is_reldate("September 18, 2018",'Title') == True
    assert is_reldate("October 18, 2018",'Title') == True
    assert is_reldate("November 18, 2018",'Title') == True
    assert is_reldate("December 18, 2018",'Title') == True

    """ Test months is mixed case """
    assert is_reldate("OCTOBER 18, 2018",'Title') == True
    assert is_reldate("october 18, 2018",'Title') == True

    """ Test comma after date is optional but other characters are not """
    assert is_reldate("October 19 2018",'Title') == True
    assert is_reldate("October ,18 2018",'Title') == False
    assert is_reldate("October 18th 2018",'Title') == False

    """ Test abbreviated month should fail expecting full month """
    assert is_reldate("Oct 18, 2018",'Title') == False
    
    """ Test invalid dates and leap year """
    assert is_reldate("February 29, 2018",'Title') == False
    assert is_reldate("February 29, 2020",'Title') == True

    """ Test fixed date with other preceding line types """
    assert is_reldate("October 18, 2018",'Blank') == True
    assert is_reldate("October 18, 2018",'Title') == True
    assert is_reldate("October 18, 2018","Rel Date") == False
    assert is_reldate("October 18, 2018","Header") == False
    assert is_reldate("October 18, 2018","Var Name") == False
    assert is_reldate("October 18, 2018","Var Desc") == False
    assert is_reldate("October 18, 2018","Var Value") == False
    assert is_reldate("October 18, 2018","Val Desc") == False
    
def test_is_blank_line():
    """ Test various combinations of white space """
    assert is_blank_line("") == True
    assert is_blank_line("\t") == True
    assert is_blank_line(" \t ") == True

    """ Test line break within paragraph """
    assert is_blank_line(" \n ") == True

    """ Test nonblank line """
    assert is_blank_line(".") == False
    assert is_blank_line("\t.") == False

def test_is_record_header():
    """ Test basic line content parsing """
    assert is_record_header("HOUSING RECORD",'Blank') == True
    assert is_record_header("PERSON RECORD",'Blank') == True
    
    assert is_record_header("HOUSING RECORD-BASIC VARIABLES",'Blank') == True
    assert is_record_header("HOUSING RECORD-HOUSING UNIT VARIABLES",'Blank') == True
    assert is_record_header("HOUSING RECORD-HOUSEHOLD VARIABLES",'Blank') == True
    assert is_record_header("HOUSING RECORD-ALLOCATION FLAGS",'Blank') == True
    assert is_record_header("HOUSING RECORD-REPLICATE WEIGHTS",'Blank') == True

    assert is_record_header("PERSON RECORD-BASIC VARIABLES",'Blank') == True
    assert is_record_header("PERSON RECORD-PERSON VARIABLES",'Blank') == True
    assert is_record_header("PERSON RECORD-PERSON RECODED VARIABLES",'Blank') == True
    assert is_record_header("PERSON RECORD-ALLOCATION FLAGS",'Blank') == True
    assert is_record_header("PERSON RECORD-REPLICATE WEIGHTS",'Blank') == True

    assert is_record_header("HOUSING Variables",'Blank') == False

    """ Test case sensitivity """
    assert is_record_header("housing record",'Blank') == False
    assert is_record_header("Housing Record",'Blank') == False
    assert is_record_header("HOUSING Record",'Blank') == False

    """ Test preceding line type """
    assert is_record_header("HOUSING RECORD",'Blank') == True
    assert is_record_header("HOUSING RECORD","Title") == False
    assert is_record_header("HOUSING RECORD","Rel Date") == True
    assert is_record_header("HOUSING RECORD","Header") == True
    assert is_record_header("HOUSING RECORD","Var Name") == False
    assert is_record_header("HOUSING RECORD","Var Desc") == False
    assert is_record_header("HOUSING RECORD","Var Value") == True
    assert is_record_header("HOUSING RECORD","Val Desc") == True
    
def test_is_var_name():
    """ Test acceptable variable name """
    assert is_var_name("PWGT Numeric 5",'Blank') == True
    assert is_var_name("PWGT1 Numeric 5",'Blank') == True
    assert is_var_name("PWGT1P Numeric 5",'Blank') == True

    assert is_var_name("1PWGT Numeric 5",'Blank') == False
    assert is_var_name("pwgt Numeric 5",'Blank') == False
    assert is_var_name("PWGT1p Numeric 5",'Blank') == False
    assert is_var_name("P_HUSAMP Numeric 5",'Blank') == False

    """ Test acceptable variable type """
    assert is_var_name("PWGT numeric 5",'Blank') == True
    assert is_var_name("PWGT NUMERIC 5",'Blank') == True
    assert is_var_name("PWGT character 5",'Blank') == True
    assert is_var_name("PWGT CHARACTER 5",'Blank') == True
    
    assert is_var_name("PWGT num3ric 5",'Blank') == False
    assert is_var_name("PWGT numBeric 5",'Blank') == False
    assert is_var_name("PWGT N 5",'Blank') == False
    assert is_var_name("PWGT 5",'Blank') == False
    
    """ Test acceptable variable length """
    assert is_var_name("PWGT Numeric 5",'Blank') == True
    assert is_var_name("PWGT Numeric 500",'Blank') == True
    assert is_var_name("PWGT Numeric 5e0",'Blank') == False
    assert is_var_name("PWGT Numeric",'Blank') == False

    """ Test spacing """
    assert is_var_name(" PWGT Numeric 5",'Blank') == False
    assert is_var_name("\tPWGT Numeric 5",'Blank') == False
    assert is_var_name("\nPWGT Numeric 5",'Blank') == False
   
    """ Test preceding line type """
    assert is_var_name("PWGT Numeric 5",'Blank') == True
    assert is_var_name("PWGT Numeric 5","Title") == False
    assert is_var_name("PWGT Numeric 5","Rel Date") == False
    assert is_var_name("PWGT Numeric 5","Header") == True
    assert is_var_name("PWGT Numeric 5","Var Name") == False
    assert is_var_name("PWGT Numeric 5","Var Desc") == False
    assert is_var_name("PWGT Numeric 5","Var Value") == True
    assert is_var_name("PWGT Numeric 5","Val Desc") == True

def test_is_var_desc():
    """ Test minimum criteria """
    assert is_var_desc("Person weight.",'Var Name') == True
    assert is_var_desc("Person weight .",'Var Name') == False
    assert is_var_desc("  Person weight.",'Var Name') == True
    assert is_var_desc("\tPerson weight.",'Var Name') == True

    """ Demonstrate lack of robustness and why Blank pltype is not okay """
    assert is_var_desc("PWGT Num3ric 5","Blank") == False
    
    """ Test that typical value entries will get filtered out """
    assert is_var_desc("foo .bar",'Var Name') == False
    assert is_var_desc(".bar",'Var Name') == False
    assert is_var_desc(" foo .bar",'Var Name') == False
    assert is_var_desc(" .bar",'Var Name') == False
    assert is_var_desc(" .",'Var Name') == False

    """ Test preceding line type """
    assert is_var_desc("Person weight",'Blank') == False
    assert is_var_desc("Person weight","Title") == False
    assert is_var_desc("Person weight","Rel Date") == False
    assert is_var_desc("Person weight","Header") == False
    assert is_var_desc("Person weight","Var Name") == True
    assert is_var_desc("Person weight","Var Desc") == True
    assert is_var_desc("Person weight","Var Value") == False
    assert is_var_desc("Person weight","Val Desc") == False

def test_is_var_value():
    """ Test line content """
    assert is_var_value("1 .XJ7","Var Desc") == True
    assert is_var_value(" 1 .XJ7","Var Desc") == True
    assert is_var_value("\t1 .XJ7","Var Desc") == True
    
    assert is_var_value("1..2 .XJ7","Var Desc") == True
    assert is_var_value(" 1..2 .XJ7","Var Desc") == True
    assert is_var_value("\t1..2 .XJ7","Var Desc") == True
    
    assert is_var_value("year of entry","Var Desc") == False
    assert is_var_value(".XJ7","Var Desc") == False
 
    """ Test preceding line type """
    assert is_var_value("1 .XJ7",'Blank') == True
    assert is_var_value("1 .XJ7","Title") == False
    assert is_var_value("1 .XJ7","Rel Date") == False
    assert is_var_value("1 .XJ7","Header") == False
    assert is_var_value("1 .XJ7","Var Name") == False
    assert is_var_value("1 .XJ7","Var Desc") == True
    assert is_var_value("1 .XJ7","Var Value") == True
    assert is_var_value("1 .XJ7","Val Desc") == True

def test_is_val_desc():
    """ Test line content """
    assert is_val_desc('foo .bar','Var Value') == False
    assert is_val_desc('.bar','Var Value') == True
    assert is_val_desc(' .bar','Var Value') == True
    assert is_val_desc('\t.bar .bar','Var Value') == True
    assert is_val_desc(' .bar .bar','Var Value') == True
    
    """ Test preceding line type """
    assert is_val_desc(" .XJ7",'Blank') == True
    assert is_val_desc(" .XJ7","Title") == False
    assert is_val_desc(" .XJ7","Rel Date") == False
    assert is_val_desc(" .XJ7","Header") == False
    assert is_val_desc(" .XJ7","Var Name") == False
    assert is_val_desc(" .XJ7","Var Desc") == False
    assert is_val_desc(" .XJ7","Var Value") == True
    assert is_val_desc(" .XJ7","Val Desc") == True

def test_classify_line():
    """ A blank line should always return Blank regardless of pltype """
    assert classify_line("",'Blank') == 'Blank'
    assert classify_line("",'Title') == 'Blank'
    assert classify_line("",'Rel Date') == 'Blank'
    assert classify_line("",'Header') == 'Blank'
    assert classify_line("",'Var Name') == 'Blank'
    assert classify_line("",'Var Desc') == 'Blank'
    assert classify_line("",'Var Value') == 'Blank'
    assert classify_line("",'Val Desc') == 'Blank'

    """ HOUSING RECORD should return Header whenever possible. Only other
    option is Var Desc if it was all caps. """
    assert classify_line("HOUSING RECORD",'Blank') == 'Header'
    assert classify_line("HOUSING RECORD",'Title') == None
    assert classify_line("HOUSING RECORD",'Rel Date') == 'Header'
    assert classify_line("HOUSING RECORD",'Header') == 'Header'
    assert classify_line("HOUSING RECORD",'Var Name') == 'Var Desc'
    assert classify_line("HOUSING RECORD",'Var Desc') == 'Var Desc'
    assert classify_line("HOUSING RECORD",'Var Value') == 'Header'
    assert classify_line("HOUSING RECORD",'Val Desc') == 'Header'

    """ This gets similar results to header """
    assert classify_line("PWGTP Numeric 5",'Blank') == 'Var Name'
    assert classify_line("PWGTP Numeric 5",'Title') == None
    assert classify_line("PWGTP Numeric 5",'Rel Date') == None
    assert classify_line("PWGTP Numeric 5",'Header') == 'Var Name'
    assert classify_line("PWGTP Numeric 5",'Var Name') == 'Var Desc'
    assert classify_line("PWGTP Numeric 5",'Var Desc') == 'Var Desc'
    assert classify_line("PWGTP Numeric 5",'Var Value') == 'Var Name'
    assert classify_line("PWGTP Numeric 5",'Val Desc') == 'Var Name'

    """ This is most restrictive on pltype since text is mostly free form """
    assert classify_line("Person Weight",'Blank') == None
    assert classify_line("Person Weight",'Title') == None
    assert classify_line("Person Weight",'Rel Date') == None
    assert classify_line("Person Weight",'Header') == None
    assert classify_line("Person Weight",'Var Name') == 'Var Desc'
    assert classify_line("Person Weight",'Var Desc') == 'Var Desc'
    assert classify_line("Person Weight",'Var Value') == None
    assert classify_line("Person Weight",'Val Desc') == None

    assert classify_line("foo .bar",'Blank') == 'Var Value'
    assert classify_line("foo .bar",'Header') == None
    assert classify_line("foo .bar",'Var Name') == None
    assert classify_line("foo .bar","Var Desc") == 'Var Value'
    assert classify_line("foo .bar",'Var Value') == 'Var Value'
    assert classify_line("foo .bar",'Val Desc') == 'Var Value'
    assert classify_line("  1 .2010 (1.0 * 1.1)",'Var Desc') == 'Var Value'

    assert classify_line(".bar",'Blank') == 'Val Desc'
    assert classify_line(".bar",'Header') == None
    assert classify_line(".bar",'Var Name') == None
    assert classify_line(".bar",'Var Desc') == None
    assert classify_line(".bar",'Var Value') == 'Val Desc'
    assert classify_line(".bar",'Val Desc') == 'Val Desc'
