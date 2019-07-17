#This includes global functions and structures.
#Copyright (c) 2019 Group of Computer Architecture, university of Bremen. All Rights Reserved.
#Filename: Define.py
#Version 1  09-July-2019
# -- coding: utf-8 --
#!/usr/bin/env python


#--------------------------------define--------------------------------#	
tuple_type_c_plusplus = 'char','char16_t','char32_t','wchar_t','signed char','short','int','long','long long','unsigned char','unsigned short','unsigned', 'unsigned long'\
,'unsigned long long','float','double','long double','bool', 'void'

BLOCK = 'block #'
CONSTRUCT = 'construct'
CLASS = 'class'
STRUCT = 'struct'
SCMODULE = 'sc_module '
SCMAIN = 'function sc_main'
Symtab = 'Symtab'
CAT = 'computed at runtime'
CONST = 'const '
SCCORE = 'sc_core::'
EAD = 'End of assembler dump.'
RETURN = 'retq'
SID = '<__static_initialization_and_destruction_0'

#----------------------------------------------------------------------#

class info_user:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#----------------------------------------------------------------------#

def module_name_extractor(line):
	split_line=line.split()
	flag_length = 0
	module_name = ""
	if '>' in split_line[2]: #---- for template type
			module_name = split_line[1] +' ' +split_line[2]
	else:	
		module_name = split_line[1]
	return 	module_name

#----------------------------------------------------------------------#

		
def func_name_extractor(line, module_name):
	string_name=line
	split_line=string_name.split()
	if len(split_line) > 1 and ('~' not in string_name) and (module_name not in split_line[0]) :	#-------------------- ignore constractor function
		for i in split_line : #-----------------remove ';' from end of function name
			if '(' in i:
				string_name = i
				temp=string_name.index('(') #-----------------extract pure name of function	
				func_type_index = split_line.index(i)-1
		return string_name[:temp]
	return ""

#----------------------------------------------------------------------#

def function_finder(symbol_file, module_name):
	func_list =[]
	for line in symbol_file: #--------------------------inside of sc_module (struct)
		if ('}' not in line) and (line.strip() != '') and (');' in line) : #---------------- extract function of module
			func_name= func_name_extractor(line, module_name)
			if func_name != "":
				func_list.append(func_name)
		elif ('}' in line):
			break
	return func_list	

#----------------------------------------------------------------------#

def key_maker (module_func_name):
	if ('sc_main' in module_func_name):
		return module_func_name
	else:
		split_line=module_func_name.split('::')
		return split_line[0]+'_'+split_line[1]