#This class generate a gdb command file (script) to automatically extract end point of each function of a module.
#Copyright (c) 2019 Group of Computer Architecture, university of Bremen. All Rights Reserved.
#Filename: EndFuncExtractor.py
#Version 1  09-July-2019
# -- coding: utf-8 --
#!/usr/bin/env python

import re 
from Define import *

class EndFuncEx:
	
	def __init__(self):
		self.end_func_dict = {}
		try:
			self.gdb_log = open("gdblog.txt",'r')
		except IOError:
			print info_user.FAIL + "Could not find \"gdblog.txt\" file!" + info_user.ENDC
			

	def find_func (self):
		for line in self.gdb_log:
			if ("breakpoint" in line) and ("sc_main" in line):
				self.find_end_func(self.gdb_log, "sc_main")
			elif ("breakpoint" in line) and ("(this=" in line):
				split_line=line.split()
				self.find_end_func(self.gdb_log, split_line[3])
			
		
	
	def find_end_func (self, gdb_log, module_func_name):
		for line in self.gdb_log:
			if (EAD in line):
				break;
			keep_previous_line = line
		end_func = self.extract_end_with_return (keep_previous_line)	
		if (end_func != "Jump"):
			self.end_func_dict[module_func_name] = end_func
		else:
			temp=module_func_name.index(':') #-----------------extract pure name of module
			module_name = module_func_name[:temp]
			end_func = self.extract_end_with_jump (self.gdb_log,module_name)
			self.end_func_dict[module_func_name] = end_func
			
	
	def extract_end_with_return (self, line):
		split_line=line.split()
		if (split_line[-1] == RETURN):
			return split_line[0]
		else:
			return "Jump"
	
	def extract_end_with_jump (self, gdb_log, module_name):
		for line in self.gdb_log:
			if (SID in line):
				split_line=line.split()
			 	if (module_name in split_line[3]):
					return split_line[1]
				

	def generate_gdb_command (self):
		gdb_source = open("gdb_source_generated_ctrl.txt",'w')					
		string = 'set logging on gdblog_ctrl.txt\nset logging redirect on\nset height 0\nset confirm off\n'	
		gdb_source.write(string)		
		
		for i in self.end_func_dict:
				
			string = 'def gdb_%s\n\tprintf "=== time is :  "\n\tprint sc_time_stamp().m_value\n\ttbreak +1\n\tcommands\n\t\t'%(key_maker(i))
			gdb_source.write(string)
			
			string = 'info line *$pc\n\t\tset $count_line_num = $_\n\t\t'
			gdb_source.write(string)
			
			string = '\n\t\tif ($count_line_num == $end_func_line_num_%s)'%(key_maker(i))
			gdb_source.write(string)
			
			string = '\n\t\t\tcontinue\n\t\telse'
			gdb_source.write(string)
						
			string = '\n\t\t\tgdb_%s\n\t\tend\n\tend\n\tcontinue\nend\n\n'%(key_maker(i))
			gdb_source.write(string)
			
			string = 'break %s\ncommands\n\t'%(i)
			gdb_source.write(string)
			
			if ('0x' in self.end_func_dict[i]):
				string = 'info line *%s\n\tset $end_func_line_num_%s= $_\n\t'%(self.end_func_dict[i],key_maker(i))
			else:
				string = 'info line %s\n\tset $end_func_line_num_%s= $_\n\t'%(self.end_func_dict[i],key_maker(i))
			
			gdb_source.write(string)
			
			string = 'gdb_%s\nend\n\n'%(key_maker(i))
			gdb_source.write(string)
															
		gdb_source.write('run\n')
		gdb_source.close()		
		
	

EndFuncEx_instance = EndFuncEx()
EndFuncEx_instance.find_func()
EndFuncEx_instance.generate_gdb_command()



