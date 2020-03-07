# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:08:08 2020

@author: Mursito
"""


import cv2

class CongklakView:
    
    def tampilPapan(self, model):
        BP0 = model.getLubang(0)
        BP1 = model.getLubang(1)
        BP1.reverse()
        print('P1 -->', model.getTabungan(1), BP1)
        print('P0 -->  ',BP0, model.getTabungan(0))

    def tampilAwal(self, model, players):
        print('CONGKLAK KEREN')
        print('Pemain 1: ', players[0].nama)
        print('Pemain 2: ', players[1].nama)
        self.tampilPapan(model)
        print('Total Biji: ', model.getTotal())
        print('TARGET    : ', model.ISI_TOTAL)
        
        
        
    def tampilMain(self, model, players):       
        p = model.getPemain()
        print('= MAIN ======================')
        print('Pemain : ', p)
        self.tampilPapan(model)
        sisi,langkah = model.getLangkah()
        print('Langkah: ', langkah)
        biji = model.getBiji()
        print('Biji   : ', biji)

    def tampilJalan(self, model, players):
        p = model.getPemain()
        self.tampilPapan(model)
        sisi,langkah = model.getLangkah()
        sisi = (sisi+p) % model.N_PEMAIN;
        print('Langkah: ', sisi,'-',langkah)
        biji = model.getBiji()
        total = model.getTotal()
        print('Biji   : ', biji, '/', total)

    def tampilUlang(self, model, players):
        p = model.getPemain()
        print('- Ulang -------------------')
        print('Pemain : ', p)
        sisi,langkah = model.getLangkah()
        print('Langkah: ', langkah)

    def tampilTabung(self, model, players):
        p = model.getPemain()
        print('- Tabung -------------------')
        print('Pemain : ', p)
        print('Tabung : ', model.getTabungan(p))        
        print('Total biji = ', model.getTotal())

    def tampilTembak(self, model, players):
        p = model.getPemain()
        print('- Tembak -------------------')
        print('Pemain : ', p)
        print('Tembak : ', model.getTabungan(p))        
        print('Total biji = ', model.getTotal())

    def tampilMati(self, model, players):
        print('- Mati -------------------')
        print('Total biji = ', model.getTotal())

    def tampilAkhir(self, model, players):
        t0 = model.getTabungan(0)
        t1 = model.getTabungan(1)
        print('= SELESAI ======================')
        print('Tabungan 1 = ', t0)
        print('Tabungan 2 = ', t1)
        if (t0 > t1):        
            print('Pemenang : ', players[0].nama) 
        elif (t0 < t1):       
            print('Pemenang : ', players[1].nama) 
        else:
            print('Seri !!!!') 
            
    def keyEscape(self):
        key = cv2.waitKey(1)         
        return key == 27

        
