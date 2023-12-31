import sys
import os
import math
import numpy as np
database="/data1/zhuyiheng/UniRef30_2022_02/UniRef30_2022_02"

bindir = "/data/zhuyiheng/toolbar/hh-suite/build/bin/"

def run_commond(workdir, name):

    query_file = workdir + "/seq/" + name + ".fasta"
    a3m_file = workdir + "/a3m/" + name + ".a3m"
    hhr_file = workdir + "/hhr/" + name + ".hhr"
    hhm_file = workdir + "/hhm/" + name +".hhm"
    msa_file = workdir + "/msa/" + name + ".msa"
    matrix_file = workdir + "/matrix/" + name + ".matrix"
    deal_msa_file = workdir + "/msa_deal/" + name + ".msa"


    cmd = bindir + "/hhblits -i " + query_file + " -d " + database + " -oa3m " + a3m_file + " -o " + hhr_file + " -n 3"
    os.system(cmd)

    cmd = bindir + "/hhmake -i " + a3m_file + " -o " + hhm_file
    os.system(cmd)

    cmd = bindir + "/hhfilter -i " + a3m_file + " -o " + msa_file + " -id 99 -cov 75"
    os.system(cmd)

    create_hhm_matrix(hhm_file, matrix_file)

    deal_msa(msa_file, deal_msa_file)


def deal_msa(original_msa_file, deal_msa_file):

    f = open(original_msa_file, "r")
    text = f.read()
    f.close()

    f = open(deal_msa_file, "w")
    for line in text.splitlines():
        line = line.strip()
        if(line.startswith(">")==False):
            f.write(line + "\n")
    f.close()


def create_hhm_matrix(hhm_file, matrix_file):

    f = open(hhm_file, "rU")
    text = f.read()
    f.close()
    line_array = text.splitlines()

    start=0
    while(start < len(line_array)):

        if(line_array[start].startswith("NULL")):
            break;
        start = start + 1
    start=start+4

    hhm_matrix = []
    while(start < len(line_array)):

        if(line_array[start].strip().startswith("//")):
            break

        value_list = line_array[start].strip().split()
        matrix_row_list=[]
        for i in range(2, len(value_list)-1):
            if(value_list[i]=="*"):
                matrix_row_list.append(0)
            else:
                matrix_row_list.append(math.pow(2, -0.001*float(value_list[i])))

        start = start + 1
        value_list = line_array[start].strip().split()
        for value in value_list:
            if (value == "*"):
                matrix_row_list.append(0)
            else:
                matrix_row_list.append(math.pow(2, -0.001 * float(value)))

        hhm_matrix.append(matrix_row_list)
        start=start+2

    hhm_matrix = np.matrix(hhm_matrix)
    np.savetxt(matrix_file, hhm_matrix, fmt="%.6f")

def get_name_list(name_file):

    f = open(name_file, "rU")
    text = f.read()
    f.close()

    return text.splitlines()

def create_single_hhm(dir, name_file):

    name_list = get_name_list(name_file)
    for name in name_list:
        run_commond(dir, name)

if __name__ == '__main__':

    dir = sys.argv[1]
    name_file = sys.argv[2]
    create_single_hhm(dir, name_file)