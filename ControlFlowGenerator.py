#This is a parser to generate control flow of a SystemC design from its extracted run-time information by GDB and present it in XML or txt format.
#Copyright (c) 2019 Group of Computer Architecture, university of Bremen. All Rights Reserved.
#Filename: ControlFlowGenerator.py
#Version 1  09-July-2019
# -- coding: utf-8 --
#!/usr/bin/env python

import re
import copy
from Define import *

class CF_generator:
	
	def __init__(self):
		self.sequence_dict = {}
		self.unic_seq_dic = {}
		try:
			self.gdb_log = open("gdblog_ctrl.txt",'r')
		except IOError:
			print info_user.FAIL + "Could not find \"gdblog_ctrl.txt\" file!" + info_user.ENDC

	def CF_extractor (self):
		index = 0
		for line in self.gdb_log:
			if ('reakpoint' in line) and (('(this=' in line) or ('sc_main' in line)):
				split_line=line.split()
				mf_name = ""
				if ('Temporary' in line):
					mf_name = split_line[3]
					this = split_line[4]
				else:
					mf_name = split_line[2]
					this = split_line[3]
					
				if ('sc_main' in line):
					this = "NULL"
					mf_name = 'sc_main'
				elif ('(this=' in line):
					this = re.sub(r'\s', '', this).split('=')
					this = this[1].replace(")","")
				source_code=split_line[-1]
					
				for line in self.gdb_log:	
					if ('===' in line):
						split_line_time = line.split()
						time = int(split_line_time[-1])				
						break
				t = (mf_name, this, source_code, time)
				self.sequence_dict[index] = list(t)
				index = index +1		
		self.gdb_log.close()		

	def print_CF (self):
		result_file = open("CF.txt",'w')
		result_file.write( "\n")				
		result_file.write( "{:<18} {:<15}".format('Sequence','Execution_flow_information'))
		result_file.write( "\n\n"	)			
		for k in sorted(self.sequence_dict.keys()):
			result_file.write( "{:<12} {:<15}".format(k, self.sequence_dict[k]))
			result_file.write( "\n"	)
		result_file.close()	

	def Uniq_CF_extractor (self):
		index = 0
		for i in sorted(self.sequence_dict.keys()):
			#print seq_dic[i][1]
			temp1 = str(self.sequence_dict[i][0])+str(self.sequence_dict[i][1])
			if (i+1) <= max(self.sequence_dict.keys()):
				temp2 = str(self.sequence_dict[i+1][0])+str(self.sequence_dict[i+1][1])
				if (temp1 != temp2):
					self.unic_seq_dic[index] = self.sequence_dict[i]
					index = index +1
			if (i+1) == max(self.sequence_dict.keys()):
				self.unic_seq_dic[index] = self.sequence_dict[i+1]
				index = index +1
					
		
	
	def XML_generator (self):	
		xml_result_file = open("XML_CF.xml",'w')
		string = "<ESL_RUN_TIME_TRACE>\n\t"
		xml_result_file.write(string )
		tmp = []
		
		for k in sorted(self.unic_seq_dic.keys()):
			if self.unic_seq_dic[k][0] != 'sc_main':
				tmp = re.sub(r'\s', '', self.unic_seq_dic[k][0]).split(':')
				module_name = tmp[0]
				func_name = tmp[2]
			else:
				module_name = self.unic_seq_dic[k][0]
				func_name = self.unic_seq_dic[k][0]			
			tmp = re.sub(r'\s', '', self.unic_seq_dic[k][2]).split(':')
			source_name = tmp[0]
			line_number = tmp[1]		
			
			string = '<SEQUENCE>\n\t\t<SEQUENCE_NUMBER> %d </SEQUENCE_NUMBER>\n\t\t<ROOT_MODULE> %s </ROOT_MODULE>\n\t\t<FUNCTION_NAME> %s </FUNCTION_NAME>\n\t\t<INSTANCE_ID> %s </INSTANCE_ID>\n\t\t\
<LINE_OF_CODE>\n\t\t\t<SOURCE_FILE> %s </SOURCE_FILE>\n\t\t\t<LINE_NUMBER> %s </LINE_NUMBER>\n\t\t</LINE_OF_CODE>\n\t\t\
<SIMULATION_TIME> %s </SIMULATION_TIME>\n\t</SEQUENCE>\n\t'%(k, module_name, func_name, self.unic_seq_dic[k][1], source_name, line_number, self.unic_seq_dic[k][3])
			xml_result_file.write(string)
		xml_result_file.write ("\n")		
		xml_result_file.write ("</ESL_RUN_TIME_TRACE>\n")		


CF_generator_instance = CF_generator()
CF_generator_instance.CF_extractor()
CF_generator_instance.Uniq_CF_extractor()
input_arc = raw_input(info_user.OKBLUE +"Generating control flow in .txt format? (Y/N)\n"+ info_user.ENDC)
if input_arc == 'Y' or input_arc == 'y': 
	CF_generator_instance.print_CF()
	print info_user.OKGREEN +"Control flow in .txt format is generated!\n"+ info_user.ENDC
input_arc = raw_input(info_user.OKBLUE +"Generating control flow in .XML format? (Y/N)\n"+ info_user.ENDC)
if input_arc == 'Y' or input_arc == 'y':
	CF_generator_instance.XML_generator()
	print info_user.OKGREEN +"Control flow in .XML format is generated!\n"+ info_user.ENDC
