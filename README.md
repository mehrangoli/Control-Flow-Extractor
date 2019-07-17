# Control-Flow-Extractor
Extracting control flow from the binary executable of SystemC designs.

This repository includes a static and dynamic data extractor that enables users to extract the static information from a given executable model of SystemC design (without needing its source code) and use it for run-time information extraction. The static information is extracted by analyzing the debug symbols of the SystemC design which is obtained from its binary executable model. This information is used to program GDB for run-time information retrieval.
This tool is able to generate XML and TXT formats of the extracted control flow (process and function activation) of the design.

For details on the techniques behind see the following publications 
- "AIBA: Automated Intra-Cycle Behavioral Analysis for SystemC-based Design Exploration" by Mehran Goli, Jannis Stoppe, and Rolf Drechsler accepted at ICCD 2016.
- "Automated Non-intrusive Analysis of Electronic System Level Designs" by Mehran Goli, Jannis Stoppe, and Rolf Drechsler accepted at TCAD 2018.


## Clone
Clone this tool using: https://github.com/mehrangoli/Control-Flow-Extractor.git



## Installation (shell interface)
To run this tool using bash script use the following command in terminal
```bash
bash bashscript.sh
```
To run this tool without using bash script the following steps are needed

```bash
python DataExtractor.py 
gdb gdb_output 
source gdb_source_generated.txt
python EndFuncExtractor.py
gdb gdb_output
source gdb_source_generated_ctrl.txt
python ControlFlowGenerator.py
```

## Requirements

- python version > 2.7

- SystemC version 2.3.1

- GNU Debugger (GDB) version > 7.0


## Debug Symbols Extraction
In order to generate debug symbol from SystemC executable model, you need to run the executable model under control of GNU Debugger (GDB) using the following command:
```bash
gdb output_exe
```
Then use the following gdb commands to generate debug symbols:
```bash
set logging redirect on
set height 0
break sc_main
commands
	maintenance print symbols "debug_symbol.txt"
end
run
```


The generated debug symbols "debug_symbol.txt" is used as the input of Control-Flow-Extractor tool.
