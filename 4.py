#-*- encoding: utf-8 -*-
#author : mxin
#CreateDate : 2019-09-05
#version 1.0

import os
import sys
import re
from xml.dom.minidom import Document

finalname = "test"
ScriptPath = os.path.split( os.path.realpath(__file__))[0] + '\\'

class XmlMaker:
    def __init__(self,txtpath,xmlpath):
        self.txtPath = txtpath
        self.xmlPath = xmlpath
        self.txtList = []


    def readtxt(self):
        txtfile = open(self.txtPath, 'r')
        self.txtList = txtfile.readlines()
        for i in self.txtList:
            oneline = i.strip().split(" ")
            if len(oneline) != 3:
                print("Param count Error")

    def makexml(self):
        doc = Document()
        orderpack = doc.createElement(finalname)
        doc.appendChild(orderpack)
        objecname = "tag"
        for i in self.txtList:
            oneline = i.strip().split(" ")
            objectE = doc.createElement(objecname)
            objectE.setAttribute("key",oneline[0])
            objectE.setAttribute("type",oneline[1])

            try:
                int(oneline[2])
            except:
                continue
            else:
                k = int(oneline[2])
                if k > 20:
                    k = 20
                for j in range(k):
                    objectcontent = doc.createElement("value")
                    objectcontenttext = doc.createTextNode(oneline[2])
                    objectcontent.appendChild(objectcontenttext)
                    objectE.appendChild(objectcontent)

            orderpack.appendChild(objectE)
            f = open(self.xmlPath, 'w')
            doc.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='UTF_8')
            f.close()

def SearchDefinition(keyword, filename):
    '''
    search the keyword in definition file
    '''
    with open(filename, 'r', encoding='UTF_8', errors ='ignore') as fread:
        lines = fread.readlines()
        for line in lines:
            if keyword in line:
                rs = re.findall(".*HWCAM_DD_DEVICE_CAP\((.*),.*",line)
                for m in rs:
                    n = m.replace('(uint32_t)','')
                    o = n.replace(' ','')
                    p = o.replace(',',' ')
                    with open((ScriptPath + finalname + '.txt'),"a+") as f:
                        print (p)
                        f.writelines(p)
                        f.writelines('\n')
    read =XmlMaker((ScriptPath + finalname + '.txt'),(ScriptPath + finalname + '.xml'))
    read.readtxt()
    read.makexml()

def SearchTag(filename):
    '''
    Intercept keywords from source code
    '''
    with open(filename, 'r', encoding='UTF_8', errors ='ignore') as fread:
        lines = fread.readlines()
        for line in lines:
            rs = re.findall(".*setData\(([^,]*),.*",line)
            for x in rs:
                SearchDefinition(x, (ScriptPath + 'DeviceCapabilities.cpp'))

if __name__ == "__main__":
    input = sys.argv
    (filepath, tempfilename) = os.path.split(input[1])
    (finalname, extension) = os.path.splitext(tempfilename)
    file_path = ScriptPath + finalname + '.txt'
    if not os.path.exists(file_path):
        open(ScriptPath + finalname + '.txt', mode='w', encoding='utf-8')
    file_path = ScriptPath + finalname + '.xml'
    if not os.path.exists(file_path):
        open(ScriptPath + finalname + '.xml', mode='w', encoding='utf-8')
    with open((ScriptPath + finalname + '.xml'), "r+") as f:
        f.truncate()
    with open((ScriptPath + finalname + '.txt'), "r+") as f:
        f.truncate()
    SearchTag(input[1])
