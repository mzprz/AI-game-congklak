# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:04:48 2020

@author: Mursito
"""

import random
from congklak_model import CongklakModel

class CongklakPlayer:
    nama = "Pemain"
    nomor = 0    
    
    def __init__(self, nama):
        self.nama = nama
        
    def setNomor(self, nomor):
        self.nomor = nomor
        
    # Pemain beraksi
    # Gunakan informasi dari papan untuk memilih nomor 
    # lubang mulai
    def main(self, papan):
        pilih = random.randint(0, papan.N_LUBANG-1) 
        print(self.nama, "main ", pilih)
        return pilih

