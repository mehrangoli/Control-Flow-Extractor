#Copyright (c) 2019 Group of Computer Architecture, university of Bremen. All Rights Reserved.
#Version 1  09-July-2019

#!/bin/bash
filename='gdb_symbol.txt'
filenameGDBLog='gdblog.txt'
filenameGDBLog_ctrl='gdblog_ctrl.txt'
flagDataExtractor=0
flagGDBCommand=0


if [ -f "$filename" ]; then
	python DataExtractor.py
	flagDataExtractor=1		
fi&&

if [ $flagDataExtractor -eq 1 ]; then
	gdb gdb_output <<EOF
	source gdb_source_generated.txt
EOF
fi&&

if [ -f "$filenameGDBLog" ]; then
	python EndFuncExtractor.py
	flagGDBCommand=1		
fi&&

if [ $flagGDBCommand -eq 1 ]; then
	gdb gdb_output <<EOF
	source gdb_source_generated_ctrl.txt
EOF
fi&&

if [ -f "$filenameGDBLog_ctrl" ]; then
	python ControlFlowGenerator.py		
fi;
