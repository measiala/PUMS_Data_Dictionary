import py.test

from classify_line import *

def test_is_blank_line():
    assert is_blank_line("") == True
    assert is_blank_line("\t") == True
    assert is_blank_line(" \t ") == True
    assert is_blank_line(".") == False

def test_is_record_header():
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
    assert is_record_header("housing record",'Blank') == False
    assert is_record_header("Housing Record",'Blank') == False
    assert is_record_header("HOUSING Record",'Blank') == False
    assert is_record_header("HOUSING Variables",'Blank') == False

    assert is_record_header("HOUSING RECORD",'Header') == True
    assert is_record_header("HOUSING RECORD",'Var Name') == False
    assert is_record_header("HOUSING RECORD",'Var Desc') == False
    assert is_record_header("HOUSING RECORD",'Var Value') == True
    assert is_record_header("HOUSING RECORD",'Val Desc') == True

def test_is_var_name():
    assert is_var_name("PWGT 5",'Blank') == True
    assert is_var_name("PWGT1 5",'Blank') == True
    assert is_var_name("PWGT1P 5",'Blank') == True
    assert is_var_name("PWGT1P A",'Blank') == False
    assert is_var_name("1PWGT 5",'Blank') == False

    assert is_var_name("PWGT",'Blank') == False
    assert is_var_name("PWGT1",'Blank') == False
    assert is_var_name("PWGT1P",'Blank') == False
    assert is_var_name("1PWGT",'Blank') == False

    assert is_var_name(" PWGT 5",'Blank') == False
    assert is_var_name(" PWGT1 5",'Blank') == False
    assert is_var_name(" PWGT1P 5",'Blank') == False
    assert is_var_name(" PWGT1P A",'Blank') == False
    assert is_var_name(" 1PWGT 5",'Blank') == False
    
    assert is_var_name(" PWGT",'Blank') == False
    assert is_var_name(" PWGT1",'Blank') == False
    assert is_var_name(" PWGT1P",'Blank') == False
    assert is_var_name(" 1PWGT",'Blank') == False

    assert is_var_name("P_HUSAMP 5",'Blank') == False
    assert is_var_name("pwgt 5",'Blank') == False
    assert is_var_name("Pwgt 5",'Blank') == False

    assert is_var_name("P_HUSAMP",'Blank') == False
    assert is_var_name("pwgt",'Blank') == False
    assert is_var_name("Pwgt",'Blank') == False

    assert is_var_name("PWGT. 5",'Blank') == False
    assert is_var_name("PWGT 5 C",'Blank') == False

    assert is_var_name("PWGT 5",'Header') == True
    assert is_var_name("PWGT 5",'Var Value') == True
    assert is_var_name("PWGT 5",'Val Desc') == True
    assert is_var_name("PWGT 5",'Var Name') == False
    assert is_var_name("PWGT 5",'Var Desc') == False

def test_is_var_desc():
    assert is_var_desc("Person weight",'Blank') == False
    assert is_var_desc("Person weight",'Header') == False
    assert is_var_desc("Person weight",'Var Name') == True
    assert is_var_desc("Person weight",'Var Desc') == True
    assert is_var_desc("Person weight",'Var Value') == False
    assert is_var_desc("Person weight",'Val Desc') == False

    assert is_var_desc("Person weight.",'Var Name') == True
    assert is_var_desc("Person weight .",'Var Name') == False
    assert is_var_desc("  Person weight.",'Var Name') == True
    assert is_var_desc("  Person weight .",'Var Name') == False
    assert is_var_desc("foo .bar",'Var Name') == False
    assert is_var_desc(".bar",'Var Name') == False
    assert is_var_desc(" foo .bar",'Var Name') == False
    assert is_var_desc(" .bar",'Var Name') == False

def test_is_var_value():
    assert is_var_value("1 .XJ7","Var Desc") == True
    assert is_var_value("1..2 .XJ7","Var Desc") == True
    assert is_var_value(" 1 .XJ7","Var Desc") == True
    assert is_var_value(" 1..2 .XJ7","Var Desc") == True
    assert is_var_value("year of entry","Var Desc") == False

    assert is_var_value("1 .XJ7","Var Value") == True
    assert is_var_value("1..2 .XJ7","Var Value") == True
    assert is_var_value(" 1 .XJ7","Var Value") == True
    assert is_var_value(" 1..2 .XJ7","Var Value") == True
    assert is_var_value("year of entry","Var Value") == False

    assert is_var_value("1 .XJ7","Val Desc") == True
    assert is_var_value("1..2 .XJ7","Val Desc") == True
    assert is_var_value(" 1 .XJ7","Val Desc") == True
    assert is_var_value(" 1..2 .XJ7","Val Desc") == True
    assert is_var_value("year of entry","Val Desc") == False

    assert is_var_value(".XJ7","Var Desc") == False
    assert is_var_value(".XJ7","Var Value") == False
    assert is_var_value(".XJ7","Val Desc") == False
 
    assert is_var_value("",'Var Desc') == False
    assert is_var_value("",'Var Value') == False
    assert is_var_value("",'Val Desc') == False
    assert is_var_value("foo .bar","Var Desc") == True

def test_is_val_desc():
    assert is_val_desc("foo .bar","Var Desc") == False
    assert is_val_desc("foo .bar","Var Value") == False
    assert is_val_desc("foo .bar","Val Desc") == False
    assert is_val_desc(" .bar","Var Desc") == False
    assert is_val_desc(" .bar","Var Value") == True
    assert is_val_desc(" .bar","Val Desc") == True
    assert is_val_desc(".bar","Var Desc") == False
    assert is_val_desc(".bar","Var Value") == True
    assert is_val_desc(".bar","Val Desc") == True
    
def test_classify_line():
    assert classify_line("",'Blank') == 'Blank'
    assert classify_line("",'Header') == 'Blank'
    assert classify_line("",'Var Name') == 'Blank'
    assert classify_line("",'Var Desc') == 'Blank'
    assert classify_line("",'Var Value') == 'Blank'
    assert classify_line("",'Val Desc') == 'Blank'

    assert classify_line("HOUSING RECORD",'Blank') == 'Header'
    assert classify_line("HOUSING RECORD",'Header') == 'Header'
    assert classify_line("HOUSING RECORD",'Var Name') == 'Var Desc'
    assert classify_line("HOUSING RECORD",'Var Desc') == 'Var Desc'
    assert classify_line("HOUSING RECORD",'Var Value') == 'Header'
    assert classify_line("HOUSING RECORD",'Val Desc') == 'Header'

    assert classify_line("PWGTP 5",'Blank') == 'Var Name'
    assert classify_line("PWGTP 5",'Header') == 'Var Name'
    assert classify_line("PWGTP 5",'Var Name') == 'Var Desc'
    assert classify_line("PWGTP 5",'Var Desc') == 'Var Desc'
    assert classify_line("PWGTP 5",'Var Value') == 'Var Name'
    assert classify_line("PWGTP 5",'Val Desc') == 'Var Name'
    
    assert classify_line("Person Weight",'Blank') == 'None'
    assert classify_line("Person Weight",'Header') == 'None'
    assert classify_line("Person Weight",'Var Name') == 'Var Desc'
    assert classify_line("Person Weight",'Var Desc') == 'Var Desc'
    assert classify_line("Person Weight",'Var Value') == 'None'
    assert classify_line("Person Weight",'Val Desc') == 'None'

    assert classify_line("foo .bar",'Blank') == 'None'
    assert classify_line("foo .bar",'Header') == 'None'
    assert classify_line("foo .bar",'Var Name') == 'None'
    assert classify_line("foo .bar","Var Desc") == 'Var Value'
    assert classify_line("foo .bar",'Var Value') == 'Var Value'
    assert classify_line("foo .bar",'Val Desc') == 'Var Value'

    assert classify_line(".bar",'Blank') == 'None'
    assert classify_line(".bar",'Header') == 'None'
    assert classify_line(".bar",'Var Name') == 'None'
    assert classify_line(".bar",'Var Desc') == 'None'
    assert classify_line(".bar",'Var Value') == 'Val Desc'
    assert classify_line(".bar",'Val Desc') == 'Val Desc'
