# -*- coding: utf-8 -*-
import sys
import re
import os
META_DATA = {}

def parse_test_package_info(StrFilePath):
    '''
    Parser test items of script, ex: #define <report1> "SN Verify"
	To do: parse SN, SYS-PN, ...
    '''
    test_package_info = {}
    test_items = {}
    with open(StrFilePath,'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("#define"):			
                strReplaceWhiteSpace = line.replace("\t", " ")			
                x, var, val = strReplaceWhiteSpace.split(' ',2)				
                if var.startswith("<report"):	
                    test_items[var] = val
    f.close()
    test_package_info["test_items"] = test_items
#    print (test_package_info)
    return test_package_info

def parse_key_cmd(StrFilePath):
    '''
    Parser key command of script to key_cmds, ex: <console_write>, <sleep>, ...
    '''
    bIsCom = False
    key_cmds = list()
    with open(StrFilePath,'r') as f:
        data = f.read()
        if data.find("telnet"):
            bIsCom = True
            key_cmds.append("telnet")
        else :
            key_cmds.append("console")
			
        f.seek(0)
        for line in f:
            if line.startswith("<"):
                key_cmds.append(line)	
    return key_cmds

def config_dev_setting(StrFilePath, Type):
    '''
    Parser device setting file to dictionart{}, ex: C2600, NetBooter, ...
    '''
    bFindDev = False
    start_s = "[" + Type + "]"
    dev_cfg = {}
    with open(StrFilePath,'r') as f:
        for line in f:
            line = line.strip()
            if bFindDev	:
                strbuf = line.split('=')
                if(strbuf[0]==""):
                    bFindDev = False
                    break
                else:
                    dev_cfg[strbuf[0]] = strbuf[1]
            if not line.find(start_s):
                bFindDev = True			    
    f.close()
    return dev_cfg

def combine_include_var_file(StrInFile, StrResultPath):
    '''
    combine include file and test script
    '''
	
    StrRefernceFile = "include_reference.txt"
    with open(StrRefernceFile, "wt") as fReference:
        with open(StrInFile, "rt") as fIncludeIn:
            for line in fIncludeIn:
                if line.startswith("#define"):			
                    fReference.write(line.replace("\\a", "\\\\a").replace("\\f", "\\\\f").replace("\\n","\\\\n").replace("\\b", "\\\\b").replace("\\t", "\\\\t"))
                else :
                    fReference.write(line)
        fReference.write("\n\n")
        fIncludeIn.close()
		
        with open(StrResultPath, "rt") as fIncludeIn:
            for line in fIncludeIn:
                if line.startswith("#define"):			
                    fReference.write(line.replace("\\a", "\\\\a").replace("\\f", "\\\\f").replace("\\n","\\\\n").replace("\\b", "\\\\b").replace("\\t", "\\\\t"))
                else :
                    fReference.write(line)
        fIncludeIn.close()
    fReference.close()

    Transformat_Valid_Backslash(StrRefernceFile,StrResultPath)		
	
def def_var_parser(data, defined_vars):
    '''
    Parse the define data and replace it in the test script.
    '''
 #   defined_vars = {}

    for line in data:
        try:
            line = line.strip()
            if line.startswith("#define"):			
                strReplaceWhiteSpace = line.replace("\t", " ")			
                x, var, val = strReplaceWhiteSpace.split(' ',2)
                defined_vars[var] = val		
        except:
            #print("parse fail!", line)
            return False
            
    #print(defined_vars)
    return True

def replace_def_var(data, var_data):
    for x in var_data.keys():
        p = re.compile(x)
        #print(p.sub(var_data[x], str(data)))
        data = p.sub(var_data[x], str(data))
    return data
    
def config_parser(data):
    '''
    Parse data that start with [Item] string, end with space line.
    The "#"  mean comment mark, line start with comment will be ignore.
    key and value, split by "=" symbol.
    watch out the space before/after "=" symbol may be split into value.

    Example:
    [Item1]
    key1=value1
    key2=value2

    [Item2]
    key1=value1
    key2=value2
    '''
    global META_DATA
    dev_data = {}
    start = False

    for line in data:
        line = line.strip()
        match = re.search(r'\[.*\]',line)
        if line.startswith('#'):
            continue
        
        if not len(line) or line == data[-1] or match:
            if start:
                x = dev_data.copy()
                META_DATA[dict_index] = x
                dev_data.clear()
            start = False
            
        if start:
            strbuf = line.split('=')
            dev_data[strbuf[0]] = strbuf[1]
                            
        if match:
            dict_index = match.group()[1:-1]
            start = True
               
    return META_DATA
	
def Transformat_Valid_Backslash(StrInFile,StrOutFile):
    with open(StrOutFile, "wt") as fBackslashOut:
        with open(StrInFile, "rt") as fBackslashIn:
            for line in fBackslashIn:
                if line.startswith("#define"):			
                    fBackslashOut.write(line.replace("\\a", "\\\\a").replace("\\f", "\\\\f").replace("\\n","\\\\n").replace("\\b", "\\\\b").replace("\\t", "\\\\t"))
              #  print (line.replace("\\a", "\\\\a").replace("\\f", "\\\\f"))
                else :
                    fBackslashOut.write(line)
        fBackslashIn.close()
    fBackslashOut.close()
	
def Parse_Replace_DefItem_InSCP(StrFilePath, StrResultPath):
    ret = True
    StrBackslashFilePath = "out_Backslash.txt"
    Transformat_Valid_Backslash(StrFilePath,StrBackslashFilePath)

    with open(StrBackslashFilePath,'r') as fParser:
        var_data = fParser.readlines()
        fParser.seek(0)
        data = fParser.read()
		
        key_data = {}
        if def_var_parser(var_data,key_data):	
            result = replace_def_var(data, key_data)
	
            resFile = open(StrResultPath,"w")
            resFile.write(result)
            resFile.close()
            print ("Parser successful! Please go to see result in ",StrResultPath)
        else:
            print ("Parser Fail! Please check File ",StrResultPath)
            ret = False
			
    fParser.close()	
    os.remove(StrBackslashFilePath)
    return ret
	

def test(StrFilePath):
    with open(StrFilePath,'r') as f:
        data = f.readlines()
        Meta_data = config_parser(data)
        print(Meta_data)
    f.close()

def test2(StrFilePath):
    with open(StrFilePath,'r') as f:
        #fdata = f.read()
        var_data = f.readlines()
        data = f.read()
        def_var_parser(var_data)        
        replace_def_var(data, def_var_parser(var_data))
        #print(fdata)
    f.close()
    data = ["#define ooo xxx",
            "xx ood oiadjf",
            "#define v2 3333",
            " ",
            "",
            "#define var1 sosos",
            "var1 oooooo",
            "ooo vvvvv var1"
            ]

    #replace_def_var(data, def_var_parser(data))
    
if __name__ == "__main__":
    #test("parse_test_data.txt")
    #test2("parse_test_data.txt")
    
    StrIncludePath = "autotest.txt"
    StrTestScpPath = "parse_test_data.txt"
    combine_include_var_file(StrIncludePath,StrTestScpPath)
    Parse_Replace_DefItem_InSCP(StrTestScpPath, "result.txt")
    config_dev_setting("Device_setting.txt", "NetBooter")
    print(parse_key_cmd("test_report_and_cmd.txt"))

