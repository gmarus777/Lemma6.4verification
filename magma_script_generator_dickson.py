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
M = 1
END_VALUE = 100

# Number of cores available
THREADS = 9

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
        c_4 =  3 * t -1
        c_5 = t - 1
        c_6 = 2 * t - 1
        c_7 = 3 * t - 2

        # last digit indicates line number in magma script file
        finite_field_1 = f'F:=FiniteField(3,{field_entry});'
        primitive_2 = f'a:= PrimitiveElement(F);'
        polynomial_ring_3 = f'P<x>:=PolynomialRing(F);'
        sum_inverse_4 = f'b:= a+a^-1;'

        dickson_1 = f'd_1:=DicksonFirst({c_1}, 1);'
        dickson_2 = f'd_2:=DicksonFirst({c_2}, 1);'
        dickson_3 = f'd_3:=DicksonFirst({c_3}, 1);'
        dickson_4 = f'd_4:=DicksonFirst(1, 1);'
        dickson_5 = f'd_5:=DicksonFirst({c_4}, 1);'
        dickson_6 = f'd_6:=DicksonFirst({t}, 1);'
        dickson_7 = f'd_7:=DicksonFirst({c_5}, 1);'
        dickson_8 = f'd_8:=DicksonFirst({c_6}, 1);'
        dickson_9 = f'd_9:=DicksonFirst({c_7}, 1);'

        trace_formula_6 = f'tr:=DicksonFirst({c_1}, 1)+DicksonFirst({c_2}, 1)+ DicksonFirst({c_3}, 1)+ DicksonFirst(1, 1)+DicksonFirst({c_4}, 1)+2*DicksonFirst({t}, 1)+2*DicksonFirst({c_5}, 1)+2*DicksonFirst({c_6}, 1)+DicksonFirst({c_7}, 1)+1;'
        image_6 = f'image:= Evaluate(tr, b);'
        order_image_7 = f'if Order(image) lt {q_minus_1_over_2} then PrintFile("Output_{m}", "False"); end if;'



        magma_command_list = [finite_field_1,primitive_2,polynomial_ring_3,
                              sum_inverse_4, trace_formula_6, image_6, order_image_7  ]




        # create the string for Template


        # create a Template file for MAGMA
        FILE_PATH = PATH / f'magma_{m}.txt'


        # we create and save a file which magma will be executing
        with open(FILE_PATH, "w") as f:
            f.write("\n".join(magma_command_list))



if __name__ == '__main__':
    main(sys.argv[1])