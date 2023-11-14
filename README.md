# FPGA-Designer

This program takes an input of equations and maps it to an FPGA. More here later

## Todo:
* ~ask about inputs~
* ~minimizer~
* factorer
* ~specify input format~
* data structure
* clean up
* bitstream

## Files
* FPGAinitializer.py : This program takes user input and creates the FPGA structure.
* logic_synthesis: This comes from assignment 1. It takes a list of equations and parses it so that each equation is in POS format and can be minimized. It also allows for factoring the equations related to each other.
* FPGAstructure.py : This defines the FPGA class
* template.blif : This is a template for a series of equations to use
