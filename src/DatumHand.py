# -*- coding: utf-8 -*-
'''
Created on Nov 11, 2015

@author: kael.Chi
'''
from bs4 import BeautifulSoup
import re
import TxtFileOperate


class DatumHand():
    
    def __ini__(self):
        self.TourName = ''
        self.SectionName = ''
        self.Round = ''
        self.BoardNum = ''
        self.HandDict = {}
        self.Datum = ''
        self.Dealer = ''
        self.Vul = ''
        self.PlayerSuit = []
        a = []
        
    def HandleDatumHand(self, content):
        soup = BeautifulSoup(content, "html.parser")
        self.TourName = soup.find('span', id="lTourname").text
        self.SectionName = soup.find('span', id="lSectionName").text
        self.Round = soup.find('span', id = 'lRound').text
        self.BoardNum = soup.find('span', id="lBoardNo").text
        self.Dealer = soup.find('span', id="lDealer").text
        self.Vul = soup.find('span', id="lVulnerable").text
        
        #Find datum and transfer to int.        
        DatumText = soup.find('span', id="lDatum").text
        DatumList = ''.join(re.findall('-?[0-9]', DatumText))
        self.Datum = DatumList
        
        #Find the hands.
        self.PlayerSuit = []
        self.HandDict = {}
        a = []
        HandList = soup.find_all('td', class_='hand')
        for item in HandList:
            for child in item.children:
                self.PlayerSuit.append(child['id'])
                self.HandDict[child['id']] = item.text
                
    def MakeHandText(self):
        a = []
        SHand = [self.HandDict['lSs'], self.HandDict['lSh'], self.HandDict['lSd'], self.HandDict['lSc']]
        WHand = [self.HandDict['lWs'], self.HandDict['lWh'], self.HandDict['lWd'], self.HandDict['lWc']]
        NHand = [self.HandDict['lNs'], self.HandDict['lNh'], self.HandDict['lNd'], self.HandDict['lNc']]
        EHand = [self.HandDict['lEs'], self.HandDict['lEh'], self.HandDict['lEd'], self.HandDict['lEc']]
        a.append(".".join(SHand))
        a.append(".".join(WHand))
        a.append(".".join(NHand))
        a.append(".".join(EHand))
        b = " ".join(a)
        self.HandText = "S:" + b
                
    def MakePBNText(self, Text):
        for i in range(len(Text)):
            if 'template_boardnum' in Text[i]:
                Text[i] = Text[i].replace('template_boardnum', self.BoardNum)
            elif 'template_dealer' in Text[i]:
                Text[i] = Text[i].replace('template_dealer', self.Dealer)
            elif 'template_vul' in Text[i]:
                Text[i] = Text[i].replace('template_vul', self.Vul)
            elif 'template_handtext' in Text[i]:
                Text[i] = Text[i].replace('template_handtext', self.HandText)
        return Text

    def MakeDatumText(self):
        DatumText = self.BoardNum + '\t' + self.Datum + '\r\n'
        return DatumText
        
        
    def PrintAllAttr(self):
        print self.TourName 
        print self.SectionName 
        print self.Round 
        print self.BoardNum 
        print self.Dealer
        print self.Vul
        for item in self.PlayerSuit:
            print item, ":",  self.HandDict[item]
        print self.Datum 