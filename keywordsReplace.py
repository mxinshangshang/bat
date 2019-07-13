#-*- encoding: utf-8 -*-
#author : mxin
#CreateDate : 2019-07-01
#version 1.0

import os
import sys
import re
import time

def alter(file, old_str, new_str):
    f = open(file,'r')
    alllines = f.readlines()
    f.close()
    f = open(file,'w+')
    for eachline in alllines:
        a = re.sub(old_str, new_str, eachline)
        f.writelines(a)
    f.close()

def get_file_path(root_path, file_list, dir_list):
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        dir_file_path = os.path.join(root_path, dir_file)
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            get_file_path(dir_file_path, file_list, dir_list)
        else:
            if os.path.splitext(dir_file_path)[1] in (".h", ".cpp"):
                file_list.append(dir_file_path)
                # print "%s" %(dir_file_path)

def execute_replace():
    f = open("./ReplaceDictionary.csv")
    time_start = time.time()
    for line in f.readlines():
        line = line.strip()
        initial_string = line.split(',', 2)[0]
        target_string = line.split(',', 2)[1]
        file_dir = './'
        file_list = []
        dir_list = []
        get_file_path(file_dir, file_list, dir_list)
        for i in file_list:
            alter(i, initial_string, target_string)
    f.close()
    time_end = time.time()
    print "Replace string done, cost time: %.3fs" %(time_end - time_start)

if __name__=='__main__':
    execute_replace()
