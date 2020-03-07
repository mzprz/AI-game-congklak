# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 07:23:50 2020

Congklak Board Game

@author: Mursito
"""

import random

class CongklakModel:
    N_PEMAIN=2
    N_LUBANG=7
    ISI_AWAL=4
    ISI_TOTAL = ISI_AWAL*N_LUBANG*N_PEMAIN

    ISI_BANYAK=9
    MIN_BANYAK=6
    MAX_BANYAK=9

    # 0 : lanjutkan
    # 1 : biji sudah 0, ulang main lagi
    # 2 : habis di tabungan, main lagi
    # 3 : habis di lubang kosong sendiri, nembak
    # 4 : habis di lubang kosong lawan, selesai
    S_LANJUT = 0
    S_ULANG = 1
    S_TABUNG = 2
    S_TEMBAK = 3
    S_MATI = 4


    # private variable, tak bisa diakses leh pemain
    # tabungan ada di lubang ke-8 (index 7)

    __lubang = [[4, 4, 4, 4, 4, 4, 4, 0],[4, 4, 4, 4, 4, 4, 4, 0]]
    __pemain=0
    __sisi=0
    __langkah=0
    __biji=0


    def __init__(self, banyak):
        self.MIN_BANYAK = banyak

    # mengembalikan isi lubang
    # memberi ketidakpastian isi BANYAK
    def getLubang(self, i):
        l = self.__lubang[i][0:7].copy()
        for i in range (self.N_LUBANG):
            if l[i] >= self.MIN_BANYAK :
                l[i] = self.ISI_BANYAK
        # print()
        return l

    def getTabungan(self, i):
        return self.__lubang[i][self.N_LUBANG]

    def getTotal(self):
        sum=0
        for j in range(self.N_PEMAIN):
            for i in range(self.N_LUBANG+1):
                sum+=self.__lubang[j][i]
        return sum

    def getPemain(self):
        return self.__pemain

    def getBiji(self):
        return self.__biji

    def getLangkah(self):
        return self.__sisi, self.__langkah


    def awal(self):
        for j in range(self.N_PEMAIN):
            self.__lubang[j][self.N_LUBANG] = 0
            for i in range(self.N_LUBANG):
                self.__lubang[j][i] = self.ISI_AWAL
        self.__pemain=0
        self.__sisi=0
        self.__langkah=0

    def gantian(self):
        self.__pemain = (self.__pemain + 1) % self.N_PEMAIN
        return self.__pemain

    def bisaMain(self):
        p = self.__pemain
        for i in range(self.N_LUBANG):
            if self.__lubang[p][i] > 0:
                return True
        return False

    # mulai bermain dari lubang tertentu
    def main(self, langkah):
        self.__sisi=0
        self.__langkah=langkah
        self.__biji=self.__lubang[self.__pemain][langkah]
        self.__lubang[self.__pemain][langkah]=0
        if (self.__biji > 0):
            return self.S_LANJUT
        return self.S_ULANG

    # jalan satu langkah
    # return S_LANJUT ... S_MATI
    def jalan(self):
        # kalau dari awal biji sudah 0, salah jalan. Ulang
        if (self.__biji == 0):
            return self.S_ULANG

        # tempatkan lubang di posisi sendiri (0) atau lawan (1)
        lubang=[self.__lubang[0], self.__lubang[1]]
        if self.__pemain == 1:
            lubang=[self.__lubang[1], self.__lubang[0]]

        biji = self.__biji
        sisi = self.__sisi;
        langkah = self.__langkah

        # cari lubang untuk main berikutnya
        if (sisi == 0):
            if (langkah < self.N_LUBANG):
                langkah += 1
            else:
                sisi = 1
                langkah = 0
        else:
            if (langkah < self.N_LUBANG-1):
                langkah += 1
            else:
                sisi = 0
                langkah = 0

        # jatuhkan biji
        biji -= 1
        lubang[sisi][langkah] += 1

        self.__biji = biji
        self.__sisi = sisi
        self.__langkah = langkah

        # kalau biji masih ada, lanjutkan
        if (biji > 0):
            return self.S_LANJUT

        # biji habis ...
        # di sisi sendiri
        if (sisi == 0):
            # di tabungan, TABUNG
            if (langkah == 7):
                return self.S_TABUNG
            # di lubang kosong, tembak
            if (lubang[0][langkah] == 1):
                lubang[0][7] += lubang[1][langkah]
                lubang[1][langkah] = 0
                return self.S_TEMBAK
            # di lubang berisi, lanjut dari lubang terakhir
            self.__biji=lubang[0][langkah]
            lubang[0][langkah]=0
            return self.S_LANJUT
        else:
            # di sisi lawan
            # di lubang kosong, mati
            if (lubang[sisi][langkah] == 1):
                return self.S_MATI
            # di lubang berisi, lanjut dari lubang terakhir
            self.__biji=lubang[1][langkah]
            lubang[1][langkah]=0
            return self.S_LANJUT

    # periksa apakah sudah berakhir
    # True : berakhir
    # False : belum berakhir
    def akhir(self):
        total = self.__lubang[0][self.N_LUBANG]+self.__lubang[1][self.N_LUBANG]
        return (total >= self.ISI_TOTAL)

    def pemenang(self):
        tabung=[self.__lubang[0][self.N_LUBANG],self.__lubang[1][self.N_LUBANG]]
        if self.__lubang[0][self.N_LUBANG]>self.__lubang[1][self.N_LUBANG]:
            return tabung,0
        elif self.__lubang[0][self.N_LUBANG]<self.__lubang[1][self.N_LUBANG]:
            return tabung,2
        return tabung,1
