#-*- encoding: utf-8 -*-
#author : mxin
#CreateDate : 2019-07-09
#version 1.0

import re
import sys
import os
import datetime
import time
import ctypes

'''
get the win width and height
'''
from ctypes import windll, create_string_buffer
user32 = ctypes.WinDLL('user32')
SW_MAXIMISE = 3
hWnd = user32.GetForegroundWindow()
user32.ShowWindow(hWnd, SW_MAXIMISE)
win_stdout = -11
fd = windll.kernel32.GetStdHandle(win_stdout)
cstruct = create_string_buffer(22)
rc_struct = windll.kernel32.GetConsoleScreenBufferInfo(fd, cstruct)
if rc_struct:
    import struct
    (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", cstruct)
    winWidth = right - left + 1
    winHeight = bottom - top + 1

def getTime():
    '''
    return time is format of time(unit is second)
    '''
    return time.time()
 
 
def getCPUClockTime():
    '''
    return time is CPU Clock time
    '''
    return time.clock()
 
 
def formatTime(timevalue):
    '''
    format the time numbers
    '''
    hour = 0
    minute = 0
    second = 0
    if timevalue > 0:
        #count hour
        hour = timevalue // 3600
        remain = timevalue % 3600
        #count minute
        minute = remain // 60
        remain = remain % 60
        #count second
        second = round(remain, 3)
    return '%.0fh:%.0fm:%.3fs'%(hour, minute, second)

def getParameters():
    '''
    get parameters from console command
    '''
    ret = []
    if len(sys.argv) < 3 or len(sys.argv) > 4:   
        print 'Please input correct parameter, for example:'
        print 'No1. python search.py keyword filepath'
        print 'No2. python search.py keyword folderpath txt'
    else:
        for i in range(1, len(sys.argv)):
            #print i, sys.argv[i]
            ret.append(sys.argv[i])
        print winWidth * '-'
        print '  Keyword = %s\n'%sys.argv[1]
    return ret


def isFileExists(strfile):
    '''
    check the file whether exists
    '''
    return os.path.isfile(strfile)


def isDirExists(strdir):
    '''
    check the dir whether exists
    '''
    return os.path.exists(strdir)

def getTarFilePath(rootPath, fileList, dirList):
    dirOrFiles = os.listdir(rootPath)
    for dirFile in dirOrFiles:
        dirFilePath = os.path.join(rootPath, dirFile)
        if os.path.isdir(dirFilePath):
            dirList.append(dirFilePath)
            getTarFilePath(dirFilePath, fileList, dirList)
        else:
            for z in (".tar.gz",".tar.bz2",".tar.bz",".tar.tgz",".tar",".tgz"):
                if dirFilePath.endswith(z):
                    fileList.append(dirFilePath)

def unRar():
    '''
    use winrar to extract files
    '''
    sourceDir = os.path.split(os.path.realpath(__file__))[0]
    fileList = []
    dirList = []
    getTarFilePath(sourceDir, fileList, dirList)
    for file in fileList:
        print "try to unrar %s" %(file)
        if(isDirExists(os.path.splitext(file)[0]) == False):
            rar_command ='"C:\Program Files\WinRAR\WinRAR.exe" x %s * %s\\'%(file, os.path.splitext(file)[0])
            os.system(rar_command)
    print ''

def getFileList(strdir):
    '''
    get a type of file list in a folder
    '''
    flist = []
    for root, dirs, fileNames in os.walk(strdir):
        if fileNames:
            for filename in fileNames:
                filepath = os.path.join(root, filename)
                flist.append(filepath)
    return flist


def Search(keyword, filename):
    '''
    search the keyword in a assign file
    '''
    if(isFileExists(filename) == False):
        print 'Input filepath is wrong,please check again!'
        sys.exit()
    linenum = 1
    findtime = 0
    with open(filename, 'r') as fread:
        lines = fread.readlines()
        for line in lines:
            rs = re.findall(keyword, line, re.IGNORECASE)
            if rs:
                #output linenum of keyword place 
                sys.stdout.write('line:%d '%linenum)
                lsstr = line.split(keyword)
                strlength = len(lsstr)
                findtime = findtime + 1
                #print strlength
                for i in range(strlength):
                    if(i < (strlength - 1)):
                        sys.stdout.write(lsstr[i].strip())
                        sys.stdout.write(keyword)
                    else:
                        sys.stdout.write(lsstr[i].strip() + '\n')
            linenum = linenum + 1
    if (findtime != 0):
       print winWidth * '-'
       print '  Find in file: %s' %(filename)
       print ('  keywords: %s %d times'%(keyword, findtime))
       print winWidth * '-'
       print ''

def SearchAll(keyword, strdir):
    '''
    search the keyword in a assign dir
    '''
    if(isDirExists(strdir) == False):
        print 'Input folderpath is wrong,please check again!'
        sys.exit()
    unRar()
    filels = getFileList(strdir)
    for item in filels:
        Search(keyword, item)

def executeSearch():
    '''
    this is a execute search method
    '''
    keyWords = raw_input("input keywords: ")
    start = getTime()
    sourceDir = sys.path[0]
    if(isDirExists(sourceDir) == False):
        print 'Input filepath is wrong,please check again!'
        sys.exit()
    print 'patch: %s' %(sourceDir)
    SearchAll(keyWords, sourceDir)
    end = getTime()
    print '  Total cost time: %s'%formatTime(end - start)
    print winWidth * '-'

if __name__=='__main__':
    executeSearch()
    os.system('pause')
