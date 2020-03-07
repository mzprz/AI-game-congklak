# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:04:48 2020

@author: Mursito
"""

import random
from congklak_model import CongklakModel
from congklak_player import CongklakPlayer

class CongklakPlayer3(CongklakPlayer):

    def __init__(self):
        super().__init__('Sedikit Duluan Random')

    # Pemain beraksi
    # Gunakan informasi dari papan untuk memilih nomor
    # lubang mulai
    def main(self, papan):
        nexts = []
        lubang = papan.getLubang(self.nomor)

        # cari maksimal
        min = 9999
        for i in range(len(lubang)):
            if (lubang[i] == 0):
                continue
            if (lubang[i] < min):
                min = lubang[i]

        # tambahkan yang minimal
        for i in range(len(lubang)):
            if (lubang[i] == min):
                nexts.append((lubang[i], i))

        print(nexts)
        pilih = random.randint(0, len(nexts)-1)
        return nexts[pilih][1];
