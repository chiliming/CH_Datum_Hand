# -*- coding: utf-8 -*-
'''
Created on 2015年11月4日

@author: Kael.Chi
'''


class FileOperate():

    
    def __init__(self):
        self.fileH = None
        self.content_temp = []
        
    def MakeCwdFolder(self, foldername):
        import os
        basedir = os.getcwd()
        parentdir = os.path.dirname(basedir)
        wholepath = parentdir + "/External_File/" + foldername
        os.mkdir(wholepath)
        
    def GetFilePath(self, filename):
        import os
        basedir = os.getcwd()
        wholename = basedir + "/" + filename
        self.AbsPath = wholename
        self.BaseDir = basedir
        return wholename
    
    def GetExtFilePath(self, filename):
        import os
        basedir = os.getcwd()
        parentdir = os.path.dirname(basedir)
        wholename = parentdir + "/External_File/" + filename
        self.AbsPath = wholename
        self.BaseDir = parentdir + "/External_File/"
        return wholename
    
    def OpenFile(self, path, mode):
        try:
            if self.fileH:
                self.CloseFile()
            self.fileH = open(path, mode)
        except IOError, e:
            print e
            return False
        else:
            return True
        
    def OpenChFile(self, path, mode, code):
        import codecs
        try:
            if self.fileH:
                self.CloseFile()
            self.fileH = codecs.open(path, mode, code)
        except:
            print 'There is problem when opening a Ch file!'
            return False
        else:
            return True
            
    def ReadLinesFromTxtFile(self):
        if    None != self.fileH:
            lines = self.fileH.readlines()
            return lines
        else:
            print "open file first!"
            
    def OpenExtFile(self, filename, mode, code):
        path = self.GetExtFilePath(filename)
        self.OpenChFile(path, mode, code)        
        
    def HandleInputFile(self, filename, code):
        mode = 'r'
        path = self.GetExtFilePath(filename)
        self.OpenChFile(path, mode, code)
        content_temp = self.ReadLinesFromTxtFile()
        self.CloseFile()
        return content_temp

    def ReadLineFromTxtFile(self, line):
        import re
        p = re.compile(r'\s+')
        
        if    None != self.fileH:
            lines = self.ReadLinesFromTxtFile()
            for item in lines:
                readKeyWord = p.split(item)
                writeKeyWord = p.split(line)
                if(0 == cmp(writeKeyWord[0], readKeyWord[0])):
                    return readKeyWord[1]
            return None
        else:
            print "open file first!"
        
    def AppendLineToTxtFile(self, line):
        if    None != self.fileH:
            self.fileH.write(line)
        else:
            print "open file first!"
            
    def ReplaceLineToTxtFile(self, line):
        import re
        p = re.compile(r'\s+')
        
        if    None != self.fileH:
            lines = self.ReadLinesFromTxtFile()
            itemNum = 0
            for item in lines:
                readKeyWord = p.split(item)
                writeKeyWord = p.split(line)
                if(0 == cmp(writeKeyWord[0], readKeyWord[0])):
                    lines[itemNum] = line
                    break
                itemNum += 1
            if    itemNum == len(lines):
                self.AppendLineToTxtFile(line)
            else:
                self.fileH.truncate(0)
                self.AppendLinesToTxtFile(lines)
        else:
            print "open file first!"
                        
    def ReplaceLinesToTxtFile(self, lines):
        import re
        p = re.compile(r'\s+')
        rstLines = []
        if    None != self.fileH:
            items = self.ReadLinesFromTxtFile()
            for elem in items:
                rstLines.append(elem)
            for line in lines:
                itemNum = 0
                for item in items:
                    readKeyWord = p.split(item)
                    writeKeyWord = p.split(line)
                    if(0 == cmp(writeKeyWord[0], readKeyWord[0])):
                        rstLines[itemNum] = line
                        break
                    itemNum += 1
                if    itemNum == len(items):
                    rstLines.append(line)
            self.fileH.truncate(0)
            self.AppendLinesToTxtFile(rstLines)
        else:
            print "open file first!"
        
    def AppendLinesToTxtFile(self, lines):
        if    None != self.fileH:
            if lines:
                self.fileH.writelines(lines)
        else:
            print "open file first!"
            
    def CloseFile(self):
        try:
            if self.fileH:
                self.fileH.close()
                self.fileH = None
        except IOError, e:
            print e
