import sympy
import os
import glob
import sys
import os
import hashlib
from multiprocessing import Pool
from subprocess import call
import pandas as pd
from pathlib import Path
import subprocess
from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr

# Stating value of N for verification of the trace formula
M = 2
END_VALUE = 10

# Number of cores available
THREADS = 3

# saving location for the LOG.txt
PATH = Path().resolve()
BASIC_LOG_FILE = PATH / 'basic_log.txt'


def main(starting_value=M, end_value=END_VALUE, threads=THREADS):
    print(f'Verifying the trace formula, starting at m={M}')
    # here we create Threads for our calls to MAGMA from the command line shell
    pool = Pool(processes=THREADS)

    # here we create the variables and pass the required string for processing to MAGMA

    m = Symbol('m')



    for m in range(M, END_VALUE):
        q = 3 ** (2 * m + 1)
        q_minus_1_over_2 = int((q - 1) / 2)
        q_minus_1_over_8 = int((q - 1) / 8)
        field_entry = 2 * m + 1
        t = 3 ** m
        # here we compute the exponent coefficients (pairwise positive and negative)
        c_1 = 2 * t
        c_2 = 2 * t - 2
        c_3 = 4 * t - 2
        c_4 = 1 - 3 * t
        c_5 = t - 1
        c_6 = 2 * t - 1
        c_7 = 3 * t - 2

        # last digit indicates line number in magma script file
        finite_field_1 = f'F:=FiniteField(3,{field_entry});'
        primitive_2 = f'a:= PrimitiveElement(F);'
        order_3 = f'Order(a);'
        function_field_4 = f'P<x>:=FunctionField(F);'
        trace_formula_5 = f'f:=x^({c_1}) + x^(-{c_1})+ x^({c_2}) + x^(-{c_2})+ x^({c_3}) + x^(-{c_3})+ x + x^(-1)+ x^({c_4}) + x^(-{c_4})+2*x^({t}) + 2*x^(-{t})+ 2*x^({c_5}) + 2*x^(-{c_5})+2*x^({c_6}) + 2*x^(-{c_6})+x**({c_7}) + x**({c_7})+1;'
        image_6 = f'mage:= Evaluate(f, a);'
        order_image_7 = f'if Order(image) ne {q-1} then image:= Evaluate(f, a^2); end if;'
        powers_8 = f'Powers:=[];'
        loop_9 = f'for i in [1..{q_minus_1_over_8}] do Powers:=Append(Powers, image^i); end for;'
        check_10 = f'b:= F! -1;'
        last_11 = f'b in Powers;'
        magma_command_list = [finite_field_1,primitive_2, order_3,
                              function_field_4,trace_formula_5, image_6,
                              order_image_7,powers_8, loop_9,
                              check_10,last_11 ]




        # create the string for Template


        # create a Template file for MAGMA
        FILE_PATH = PATH / f'magma_{m}.txt'


        # we create and save a file which magma will be executing
        with open(FILE_PATH, "w") as f:
            f.write("\n".join(magma_command_list))



