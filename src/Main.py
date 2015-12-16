# -*- coding: utf-8 -*-
'''
Created on Dec 2, 2015

@author: kael.Chi
'''

from FileOperate import FileOperate
import httplib2
from bs4 import BeautifulSoup
import re
from DatumHand import DatumHand
import time
import copy
import os

if __name__ == '__main__':
    url_file_name = 'url.txt'
    url_file_code = 'utf-8'
    h = httplib2.Http(".cache")
    board_url = []
    base_url = 'http://www.zgqpw.com.cn/Tour/'
    PBNTemplateName = 'PBN_Template.pbn'
    PBNTemplateCode = 'utf-8'
    CurrentTime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    CurrentDate = time.strftime("%Y-%m-%d", time.localtime())
    Site = 'bbs.7ntxx-13.com'



    pass

url_hand = FileOperate()
url_temp = url_hand.HandleInputFile(url_file_name, url_file_code)
Template = FileOperate()
TemplateText = Template.HandleInputFile(PBNTemplateName, PBNTemplateCode)




for i in range(len(url_temp)):
    board_url = []
    resp, content = h.request(url_temp[i].strip(), "GET")
    soup = BeautifulSoup(content, "html.parser")
    TourName = soup.find('span', id="lTourname").text
    SectionName = soup.find('span', id="lSectionName").text
    Round = soup.find('span', id="lRound").text
    PBNName = TourName + "_" + SectionName + "_" + u"第" + Round + u"轮" + "_" +  u"牌型" + "_ " + CurrentTime + ".pbn"
    DatumName = TourName + "_" + SectionName + "_" + u"第" + Round + u"轮" + "_" + 'Datum' + "_" +  CurrentTime + ".txt"
    FolderName = TourName 
    PBN = FileOperate()
    try: 
        PBN.MakeCwdFolder(FolderName)
    except:
        print 'The folder %s is exist!'%FolderName
        pass
    if "/" in PBNName:
        PBNName = PBNName.replace("/", "_")
    print 'PBN name is %s'%PBNName
    if "/" in DatumName:
        DatumName = DatumName.replace("/", "_")
    print 'Datum name is %s'%DatumName
    PBN.OpenExtFile(PBNName, 'w', 'utf-8')
    Datum = FileOperate()
    Datum.OpenExtFile(DatumName, 'w', 'utf-8')

    
    for item in soup.find_all('a', text=re.compile("[0-9][0-9]?"),  href=re.compile("^Board")):
        board_url.append(item)
    for item in board_url:
        resp, content = h.request(base_url + item['href'], "GET")
        Hand = DatumHand()
        Hand.HandleDatumHand(content)
        PBNText = copy.deepcopy(TemplateText)
        for j in range(len(PBNText)):
            if 'template_date' in PBNText[j]:
                PBNText[j] = PBNText[j].replace('template_date', CurrentDate)
            elif 'template_site' in PBNText[j]:
                PBNText[j] = PBNText[j].replace('template_site', Site)
        Hand.MakeHandText()
        Hand.MakePBNText(PBNText)
        DatumText = Hand.MakeDatumText()
        PBN.AppendLinesToTxtFile(PBNText)
        Datum.AppendLinesToTxtFile(DatumText)
        print 'finish hand %s'%Hand.BoardNum
    PBN.CloseFile()
    Datum.CloseFile()
    try:
        os.rename(PBN.AbsPath, PBN.BaseDir +  FolderName + "/" + PBNName)
        os.rename(Datum.AbsPath, Datum.BaseDir + FolderName + "/" + DatumName)
    except:
        pass
    print 'finish %d url'%(i+1)


