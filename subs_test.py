import py.test

from subs import *

def test_is_record_header():
    assert is_record_header("HOUSING RECORD") == True
    assert is_record_header("PERSON RECORD") == True
    assert is_record_header("HOUSING RECORD-BASIC VARIABLES") == True
    assert is_record_header("HOUSING RECORD-HOUSING UNIT VARIABLES") == True
    assert is_record_header("HOUSING RECORD-HOUSEHOLD VARIABLES") == True
    assert is_record_header("HOUSING RECORD-ALLOCATION FLAGS") == True
    assert is_record_header("HOUSING RECORD-REPLICATE WEIGHTS") == True
    assert is_record_header("PERSON RECORD-BASIC VARIABLES") == True
    assert is_record_header("PERSON RECORD-PERSON VARIABLES") == True
    assert is_record_header("PERSON RECORD-PERSON RECODED VARIABLES") == True
    assert is_record_header("PERSON RECORD-ALLOCATION FLAGS") == True
    assert is_record_header("PERSON RECORD-REPLICATE WEIGHTS") == True
    assert is_record_header("housing record") == False
    assert is_record_header("Housing Record") == False
    assert is_record_header("HOUSING Record") == False
    assert is_record_header("HOUSING Variables") == False

def test_is_var_name():
    assert is_var_name("PWGT 5") == True
    assert is_var_name("PWGT1 5") == True
    assert is_var_name("PWGT1P 5") == True
    assert is_var_name("PWGT1P 5") == True
    assert is_var_name("PWGT1P A") == False
    assert is_var_name("  PWGT") == False
    assert is_var_name("1PWGT") == False
    assert is_var_name("Pwgt") == False
    assert is_var_name("Pwgt1") == False
    assert is_var_name("P_HUSAMP") == False
    assert is_var_name("pwgt") == False
    assert is_var_name("PWGT") == False
    assert is_var_name("PWGT1") == False
    assert is_var_name("PWGT1P") == False
    assert is_var_name("PWGT1P") == False

def test_is_var_desc():
    """ Think about this """
    assert is_var_desc("  Year of entry",'Var Name') == True
    assert is_var_desc("YOEP","Var Name") == True
    assert is_var_desc("YOEP","Var Desc") == True
    assert is_var_desc("Yoep","Var Desc") == True
    assert is_var_desc("Yoep","Var Value") == False
    assert is_var_desc("Yoep","Header") == False
    assert is_var_desc("Yoep","Val Desc") == False

""" is_var_value """
    
def test_is_val_desc():
    assert is_val_desc("1 .XJ7","Var Desc") == True
    assert is_val_desc("1..2 .XJ7","Var Desc") == True
    assert is_val_desc(" 1 .XJ7","Var Desc") == True
    assert is_val_desc(" 1..2 .XJ7","Var Desc") == True
    assert is_val_desc("year of entry","Var Desc") == False

    assert is_val_desc("1 .XJ7","Val Desc") == True
    assert is_val_desc("1..2 .XJ7","Val Desc") == True
    assert is_val_desc(" 1 .XJ7","Val Desc") == True
    assert is_val_desc(" 1..2 .XJ7","Val Desc") == True
    assert is_val_desc("Note: ",'Val Desc') == False

    assert is_val_desc("",'Var Desc') == False
    assert is_val_desc("",'Val Desc') == False

def test_add_var_name():
    """ Work on this """

def test_add_var_desc():
    """ work on this """
    
def test_add_val_desc():
    """ Work on this """

def test_classify_line():
    assert classify_line("",'Header') == 'Blank'
    assert classify_line("",'Var Name') == 'Blank'
    assert classify_line("",'Var Desc') == 'Blank'
    assert classify_line("",'Var Value') == 'Blank'
    assert classify_line("HOUSING RECORD",'Blank') == 'Header'
    assert classify_line("HOUSING RECORD",'Var Value') == 'Header'
    assert classify_line("HOUSING RECORD",'Header') == 'Header'
    assert classify_line("PWGTP",'Blank') == 'Var Name'
    assert classify_line("PWGTP 5",'Blank') == 'Var Name'
    assert classify_line("PWGTP",'Var Value') == 'Var Name'
    assert classify_line("PWGTP 5",'Var Value') == 'Var Name'
    assert classify_line("  Person Weight",'Var Name') == 'Var Desc'
    assert classify_line("  0XJ",'Var Desc') == 'Var Value'
    assert classify_line("  0XJ..0XL",'Var Desc') == 'Var Value'
    assert classify_line("  0XJ  .Meaningless",'Var Desc') == 'Var Value'
    assert classify_line("  0XJ",'Var Value') == 'Var Value'
    assert classify_line("  0XJ..0XL",'Var Value') == 'Var Value'
    assert classify_line("  0XJ  .Meaningless",'Var Value') == 'Var Value'
    
def test_process_line():
    """ Work on this """
        
