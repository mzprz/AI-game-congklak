# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:04:48 2020

@author: Mursito
"""

import random
from congklak_model import CongklakModel
from congklak_player import CongklakPlayer

class CongklakPlayer4(CongklakPlayer):
    
    def __init__(self):
        super().__init__('Banyak Duluan Random')
        
    # Pemain beraksi
    # Gunakan informasi dari papan untuk memilih nomor 
    # lubang mulai
    def main(self, papan):
        nexts = []
        lubang = papan.getLubang(self.nomor)
        # cari maksimal
        max = 0
        for i in range(len(lubang)):
            if (lubang[i] > max):
                max = lubang[i]

        # tambahkan yang maksimal
        for i in range(len(lubang)):
            if (lubang[i] >= max):        
                nexts.append((lubang[i], i))

        print(nexts)
        pilih = random.randint(0, len(nexts)-1)
        return nexts[pilih][1];

