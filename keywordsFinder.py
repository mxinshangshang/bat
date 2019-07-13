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
import importlib
importlib.reload(sys)

'''
get the win maximization
'''
from ctypes import windll, create_string_buffer
user32 = ctypes.WinDLL('user32')
SW_MAXIMISE = 3
hWnd = user32.GetForegroundWindow()
user32.ShowWindow(hWnd, SW_MAXIMISE)

winWidth = 236
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
FOREGROUND_DARKRED = 0x04 # dark red.
FOREGROUND_DARKGREEN = 0x02 # dark green.
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_RED = 0x0c # red.

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

def printDarkSkyBlue(mess):
    '''
    dark sky blue
    '''
    set_cmd_text_color(FOREGROUND_DARKSKYBLUE)
    sys.stdout.write(mess)
    resetColor()

def printRed(mess):
    set_cmd_text_color(FOREGROUND_DARKRED)
    sys.stdout.write(mess)
    resetColor()

def printDarkGreen(mess):
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(mess)
    resetColor()

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
    return '%.0fh : %.0fm : %.3fs'%(hour, minute, second)


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
            for z in (".tar.gz",".tar.bz2",".tar.bz",".tar.tgz",".tar",".tgz",".zip",".gz"):
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
    print ('  Checking zip files, just wait...')
    for file in fileList:
        #print "try to unzip %s" %(file)
        if(isDirExists(os.path.splitext(file)[0]) == False):
            rar_command ='"C:\Program Files\WinRAR\WinRAR.exe" x %s * %s\\'%(file, os.path.splitext(file)[0])
            os.system(rar_command)
    print ('  Check zip files done\n')

def getFileList(strdir):
    '''
    get a type of file list in a folder
    '''
    flists = []

    for root, dirs, fileNames in os.walk(strdir):
        if fileNames:
            for filename in fileNames:
                noNeedAdd = False
                for z in (".tar.gz",".tar.bz2",".tar.bz",".tar.tgz",".tar",".tgz",".zip",".gz",".exe"):
                    if filename.endswith(z):
                        noNeedAdd = (noNeedAdd | True)
                if (noNeedAdd == False):
                    filepath = os.path.join(root, filename)
                    flists.append(filepath)
    return flists


def Search(keyword, filename):
    '''
    search the keyword in a assign file
    '''
    if(isFileExists(filename) == False):
        print ('Input filepath is wrong,please check again!')
        sys.exit()
    linenum = 1
    findtime = 0
    with open(filename, 'r', encoding='UTF_8', errors ='ignore') as fread:
        lines = fread.readlines()
        for line in lines:
            rs = re.findall(keyword, line, re.IGNORECASE)
            if rs:
                #output linenum of keyword place 
                sys.stdout.write('line:%d '%linenum)
                lsstr = line.split(keyword)
                strlength = len(lsstr)
                findtime = findtime + 1
                for i in range(strlength):
                    if(i < (strlength - 1)):
                        sys.stdout.write((lsstr[i].strip() + ' '))
                        #sys.stdout.write(keyword)
                        printRed(keyword)
                    else:
                        sys.stdout.write((lsstr[i].strip() + '\n'))
            linenum = linenum + 1
    if (findtime != 0):
       print ('-' * winWidth)
       printDarkSkyBlue(('  Find in file: %s\n' %(filename)))
       printDarkSkyBlue(('  Keywords: %s %d times\n'%(keyword, findtime)))
       print ('-' * winWidth)
       print ('')

def SearchAll(keyword, strdir):
    '''
    search the keyword in a assign dir
    '''
    if(isDirExists(strdir) == False):
        print ('Input folderpath is wrong,please check again!')
        sys.exit()
    unRar()
    filels = getFileList(strdir)
    print ('  Searching...\n')
    for item in filels:
        Search(keyword, item)

def executeSearch():
    '''
    this is a execute search method
    '''
    keyWords = input("  Input keywords: ")
    start = getTime()
    sourceDir = os.path.split(os.path.realpath(__file__))[0]
    if(isDirExists(sourceDir) == False):
        print ('Input filepath is wrong,please check again!')
        sys.exit()
    printDarkSkyBlue('  Current search path: %s\n' %(sourceDir))
    SearchAll(keyWords, sourceDir)
    end = getTime()
    printDarkGreen('  Total cost time %s\n'%formatTime(end - start))
    print ('-' * winWidth)
    print ('')

if __name__=='__main__':
    while True:
       try:
           executeSearch()
       except KeyError:
           pass
