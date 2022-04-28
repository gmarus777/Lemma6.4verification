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

# Number of cores available
THREADS = 3


# Running a thread pool masks debug output. Set DEBUG to 1 to run
DEBUG = False

DEVNULL = open(os.devnull, "w")

def run_threaded_magma_scripts(start, end):
    list_of_m=[]
    pool = Pool(processes=THREADS)
    for i in range(start, end):
        list_of_m.append(i)

    pool.map(run_magma, list_of_m)






def run_magma(m):
    magma_commad = f'magma magma_{m}.txt'
    os.system(magma_commad)

if __name__ == '__main__':
    main(sys.argv[1])