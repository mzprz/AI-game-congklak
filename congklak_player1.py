# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:04:48 2020

@author: Mursito
"""

import random
from congklak_model import CongklakModel

from congklak_player import CongklakPlayer

class CongklakPlayer1(CongklakPlayer):    
    def __init__(self):
        super().__init__('Banyak Duluan')
        
    # Pemain beraksi
    # Gunakan informasi dari papan untuk memilih nomor 
    # lubang mulai
    def main(self, papan):
        nexts = []
        lubang = papan.getLubang(self.nomor)
        #print("Lubang: ", lubang)
        for i in range(len(lubang)):
            if (lubang[i] > 0):
                nexts.append((lubang[i], i))
        #print("Pilihan", nexts)
        nexts.sort(reverse=True)        
        pilih = nexts[0][1];
        return pilih
