import os
import sys

def read_name_list(name_list_file):

    f = open(name_list_file, "r")
    text = f.read()

    return text.splitlines()

def split(total_number, thread_number, name_list):

    name_list=sorted(name_list)
    split_list=[]
    n=total_number/thread_number+1
    for i in range(thread_number+1):
        start=int(i*n)
        end=int((i+1)*n)
        if(end>total_number):
            end=total_number

        if(start<total_number):
            temp_list=[]
            for i in range(start, end, 1):
                temp_list.append(name_list[i])
            split_list.append(temp_list)

    return split_list

def create_name_list(name_list_file, outputdir):

    name_list = read_name_list(name_list_file)
    total_number = len(name_list)
    thread_number = 10

    split_list = split(total_number, thread_number, name_list)

    for i in range(len(split_list)):

        index = i + 1
        sub_name_list_file = outputdir + "/name_list" + str(index)
        f = open(sub_name_list_file, "w")
        for name in split_list[i]:
            f.write(name[:len(name)-6] + "\n")
        f.close()


create_name_list(sys.argv[1], sys.argv[2])


