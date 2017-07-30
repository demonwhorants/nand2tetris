#!/usr/bin/python

import sys

DEST_DICT = {
    'NULL': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111'
}

JMP_DICT = {
    'NULL': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

COMP_DICT = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    '!D': '0001101',
    '!A': '0110001',
    '-D': '0001111',
    '-A': '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M': '1110000',
    '!M': '1110001',
    '-M': '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101'
}

PRE_DEF_SYMBOLS = {

    'SP': '0000000000000000',
    'LCL': '0000000000000001',
    'ARG': '0000000000000010',
    'THIS': '0000000000000011',
    'THAT': '0000000000000100',
    'SCREEN': '0100000000000000',
    'KBD': '1100000000000000',
    'R0': '0000000000000000',
    'R1': '0000000000000001',
    'R2': '0000000000000010',
    'R3': '0000000000000011',
    'R4': '0000000000000100',
    'R5': '0000000000000101',
    'R6': '0000000000000110',
    'R7': '0000000000000111',
    'R8': '0000000000001000',
    'R9': '0000000000001001',
    'R10': '0000000000001010',
    'R11': '0000000000001011',
    'R12': '0000000000001100',
    'R13': '0000000000001101',
    'R14': '0000000000001110',
    'R15': '0000000000001111'
}

LABEL_DICT = {}

VARIABLE_DICT = {}

A_DICT_LIST = [LABEL_DICT, VARIABLE_DICT]

lineNumber = 0          # counter
formatted_lines = []
final_lines = []        #


class Assembler:

    def __init__(self):
        self.variable_m_loc = 16        # variable mem address counter

    def print_bin(self, machine_code):

        # output to file eventually
        print('{0:016b}'.format(machine_code))


    def parse_a_c(self, line):

        # decide wether each line is an A or C instruction and pass to the
        # relevant function

        if line[0] == '@':
            self.a_command(line)
        else:
            self.c_command(line)

    def a_command(self, line):

        #print("Line @ a_command: " + line)
        # if instruction contains a number
        if line[1:].isdigit():
            self.print_bin(int(line[1:15]))
            return
        # if instruction contains a predefined symbol
        elif line[1:] in list(PRE_DEF_SYMBOLS):
            asm = PRE_DEF_SYMBOLS[line[1:]]
            print(asm)
            return
        # if A instruction is in LABEL or VARIABLE
        for a_dict in A_DICT_LIST:
            
            if line[1:] in a_dict:
                #print("A_DICT check: " + str(a_dict[line[1:]]))
                self.print_bin(a_dict[line[1:]])
                return
            # else it must be a new variable
            else:
                
                new_var = line.strip()[1:]
                # add 'variable':'mem address' key:value pair
                a_dict[new_var] = self.variable_m_loc
                self.print_bin(self.variable_m_loc)
                # increment variable mem address counter
                self.variable_m_loc += 1
                return

    def c_command(self, line):

        #print("Line @ c_command: " + line)
        # deal with C instructions.
        if ';' in line:  # JMP
            comp, jmp = line.split(';')
            machine_code = '111' + COMP_DICT[comp] + '000' + JMP_DICT[jmp]

        elif '=' in line:  # INST

            dest, comp = line.split('=')
            machine_code = '111' + COMP_DICT[comp] + DEST_DICT[dest] + '000'

        print(machine_code)

    def l_command(self, line):

        # deal with labels

        self.print_bin(int(LABEL_DICT[line[1:-1]]))

    def add_label(self, line, lineNumber):

        # first pass, adds a label:linenumber key:value pair to a dictionary of
        # labels.

        label = line.strip()[1:-1]
        LABEL_DICT[label] = lineNumber

# open file

f = open(sys.argv[1], "r")
lines = f.readlines()
f.close()

lines = filter(None, (line.rstrip() for line in lines))  # remove trailing
lines = filter(None, (line.lstrip() for line in lines))  # remove leading whitespace


for line in lines:

    # format lines to remove comments

    if not line.startswith('//'):                   # if not a comment line
        # split on whitespace (removes inline comments)
        strip_line = line.split(' ', 1)
        # only take first element of split line (not the inline comment)
        formatted_lines.append(strip_line[0])


assembler = Assembler()

# symbol table (dictionary) gen

for line in formatted_lines:

    # call initial pass of asm, parsing for labels
    if line[0] == '(':
        assembler.add_label(line, lineNumber)
    # remove the (LABEL) lines from the final list of lines to be assembled
    if not line.startswith('('):
        final_lines.append(line)
        # increment lineNumer counter
        lineNumber = lineNumber + 1

# assembly gen

for line in final_lines:

    # assemble!
    
    assembler.parse_a_c(line)