import random
# from congklak_model_sim import CongklakModelSim
from congklak_view import CongklakView
from congklak_player import CongklakPlayer
import numpy as np
import copy

class CongklakPlayer5(CongklakPlayer):

    def __init__(self):
        super().__init__('Tim Blabalbalba')
        self.blimit = 200
        self.plyLimit = 4
        self.batasAtas = 20

        self.faktor_lanjut = 0
        self.faktor_ulang = 0
        self.faktor_tabung = 0
        self.faktor_tembak = 0
        self.faktor_mati = 0

        self.w0_1 = 1   #tabungan
        self.w0_2 = -0.4 #tabungan musuh
        self.w0_3 = 0.8 #total biji di sisi player
        self.w0_4 = -0.6 #biji di sisi musuh
        self.w1 = 0.2     #lanjut
        self.w2 = -0     #ulang
        self.w3 = 0.1   #tabung
        self.w4 = 0.1    #tembak
        self.w5 = 0     #mati

        self.inc = 10   #increment


    # Pemain beraksi
    # Gunakan informasi dari papan untuk memilih nomor
    # lubang mulai

    def resetFaktor(self):
        self.faktor_lanjut = 0
        self.faktor_ulang = 0
        self.faktor_tabung = 0
        self.faktor_tembak = 0
        self.faktor_mati = 0

    def evalFunc(self, frontier, no):
        eval = 0
        eval = self.w0_1 * (frontier.getTabungan(no))
        eval += self.w0_2 * (frontier.getTabungan(1-no))
        eval += self.w0_3 * sum(frontier.getLubang(no))
        eval += self.w0_4 * sum(frontier.getLubang(1-no))
        eval += self.w1 * self.faktor_lanjut
        eval += self.w2 * self.faktor_ulang
        eval += self.w3 * self.faktor_tabung
        eval += self.w4 * self.faktor_tembak
        eval += self.w5 * self.faktor_mati

        self.resetFaktor()

        # print("eval", eval)
        return eval

    def nextStep(self, papan, langkah, nomor): #untuk mensimulasikan kalau lubang tsb dipilih
        # papan.__pemain = nomor

        # print("NO", nomor)
        # print("main", papan.__pemain)
        # print("AWAL")
        # CongklakView().tampilPapan(papan)

        if papan.getPemain() != nomor:
            papan.gantian()

        if papan.bisaMain():
            status=papan.main(langkah)
            # print("MAIN")
            # CongklakView().tampilPapan(papan)
        else:
            status = papan.S_MATI
            # print("MATI")

        # print(status)

        while status == papan.S_LANJUT:
            # print("JALAN")
            # CongklakView().tampilPapan(papan)
            status = papan.jalan()
            self.faktor_lanjut += self.inc
        if status == papan.S_ULANG:
            self.faktor_ulang += self.inc
            pass
        elif status == papan.S_TABUNG:
            self.faktor_tabung += self.inc
            pass
        elif status == papan.S_TEMBAK:
            self.faktor_tembak += self.inc
            pass
        elif status >= papan.S_MATI:
            self.faktor_mati += self.inc
            pass

        try:
            nextState = papan.getState()
        except:
            nextState = [papan.getLubang(0), papan.getLubang(1)]
            nextState[0].append(papan.getTabungan(0))
            nextState[1].append(papan.getTabungan(1))
            # print(nextState)
        return nextState #kondisi lubang keseluruhan

    def getNexts(self, papan, nomor):
        nexts = []
        lubang = papan.getLubang(nomor)

        for i in range(len(lubang)):
            if lubang[i] > 0 :
                nexts.append(i)

        # random = np.random.random()

        # if random > 0.5:

        # # cari max
        # max = 0.1
        # for i in range(len(lubang)):
        #     if (lubang[i] > max):
        #         max = lubang[i]
        #
        # # tambahkan yang max
        # for i in range(len(lubang)):
        #     # if max>0:
        #     if (lubang[i] >= max):
        #         nexts.append(i)
        #
        # # cari min
        # min = 9999
        # for i in range(len(lubang)):
        #     if (lubang[i] == 0):
        #         continue
        #     if (lubang[i] < min):
        #         min = lubang[i]
        #
        # # tambahkan yang min
        # for i in range(len(lubang)):
        #     # if min>0:
        #     if (lubang[i] == min):
        #         nexts.append(i)

        return list(set(nexts));

    def cariCabang(self, node1, nomor): #utuk cari cabang dari suatu node
        cabang = []
        nexts = self.getNexts(node1, nomor)
        # print("next", len(nexts))
        for i in range(len(nexts)):
            node = copy.deepcopy(node1)
            # print("init", node.getState())
            pilih = nexts[i]
            # print("pilih", pilih)
            nextNode = self.nextStep(node, pilih, nomor)
            # print("asd", nextNode)
            # print(node.getState())
            a = CongklakModelSim(self.batasAtas)
            a.setLubang(nextNode)

            cabang.append((pilih, a))
            # print(a.getState())
        return cabang

    def cariMax(self, evalScore):
        score = []
        max = 0
        for i in range(len(evalScore)):
            if (evalScore[i] > max):
                max = evalScore[i]

        # tambahkan yang minimal
        for i in range(len(evalScore)):
            if (evalScore[i] >= max):
                score.append(evalScore[i])
        return score

    def cariMin(self, evalScore):
        score = []
        min = 9999
        for i in range(len(evalScore)):
            if (evalScore[i] < min):
                min = evalScore[i]

        # tambahkan yang minimal
        for i in range(len(evalScore)):
            if (evalScore[i] == min):
                score.append(evalScore[i])
        return score

    def main(self, papan):
        # print("NO", self.nomor)
        score = []
        pilihan = []
        evalScore = []
        node = []
        plyLimits = self.plyLimit

        for i in range(plyLimits):
            node.append([])
            score.append([])
            evalScore.append([])
        for i in range(plyLimits):
            for j in range(self.blimit):
                score[i].append([])
                evalScore[i].append([])

        node[0].append([])

        stateNol = [papan.getLubang(0), papan.getLubang(1)]
        stateNol[0].append(papan.getTabungan(0))
        stateNol[1].append(papan.getTabungan(1))

        papan2 = CongklakModelSim(self.batasAtas)
        papan2.setLubang(stateNol)

        node[0][0] = ((0,0), papan2, 0)
        # print("LEN", node[0][0])

        # untuk mendapatkan seluruh node pada kedalaman selanjutnya

        # while papan2.getLubang(self.nomor) != [0,0,0,0,0,0,0]:
        for i in range(plyLimits-1):
            if i%2 == 0: #max ?
                no = self.nomor
            else: #min
                no = 1 - self.nomor

            for j in range(len(node[i])):
                if j < self.blimit:
                    # print(i,j, node[i][j])
                    cabang = self.cariCabang(node[i][j][1], no)
                    for k in range(len(cabang)):
                        parent = (i,j)
                        node[i+1].append((parent, cabang[k][1], cabang[k][0]))
                        # print("Cabang", parent, cabang[k][0])
                        # print("PAPAN: ", i+1, k, cabang[k][1])
                        # CongklakView().tampilPapan(cabang[k][1])
            # print("hola", len(node[i+1]))
            if len(node[i+1]) == 0:
                newLimit = i
                plyLimits = newLimit+1
                print("LIMIT CHANGED", plyLimits)
                break


        # mencari skor pada node paling akhir
        frontier = node[plyLimits-1]
        # print(frontier)
        for i in range(len(frontier)):
            parent = [frontier[i][0][0], frontier[i][0][1]]
            if parent[1] < self.blimit:
                if plyLimits%2 == 0:
                    no = self.nomor
                else:
                    no = 1 - self.nomor

                # print(parent[0],parent[1])
                evalScore[parent[0]][parent[1]].append(self.evalFunc(frontier[i][1],no))

                # print("FRONTIER", self.evalFunc(frontier[i][1],no))
                # CongklakView().tampilPapan(frontier[i][1])

        for i in range(plyLimits-1):
            i = plyLimits-2 -i #depth
            for j in range(len(node[i])): #lebar dari depth ini
                if j < self.blimit:
                    if i%2 == 0: #max?
                        score[i][j] = self.cariMax(evalScore[i][j])
                        # print(i,j, score[i][j])
                        #cari max --> mencari max pada parent yang sama
                    else:
                        score[i][j] = self.cariMin(evalScore[i][j])

                    # assign eval score untuk node di atasnya
                    frontier = node[i]
                    for k in range(len(frontier)):
                        parent = [frontier[k][0][0], frontier[k][0][1]]
                        # print(parent)
                        for m in range(len(score[i][j])):
                            # print(score[i][j][m])
                            if score[i][j][m] not in evalScore[parent[0]][parent[1]]:
                                evalScore[parent[0]][parent[1]].append(score[i][j][m])

        print('==> min = ', score[0][0])
        if len(score[0][0])>0:
            for i in range(len(score[1])):
                if len(score[1][i]) > 0:
                    # print(i, '1', score[1][i])
                    for j in range(len(score[1][i])):
                        if score[0][0][0] == score[1][i][j]:
                            if node[1][i][2] not in pilihan:
                                pilihan.append((node[1][i][1].getTabungan(self.nomor), node[1][i][2]))
                                print("ALTERNATIF", node[1][i][2], score[node[1][i][0][0]][node[1][i][0][1]])
                                CongklakView().tampilPapan(node[1][i][1])

        # ambil dari 1 ply aja
        if len(pilihan) <1 :
            testLubang = papan.getLubang(self.nomor)
            for i in range(len(testLubang)):
                if testLubang[i]>0:
                    pilihan.append((papan.getTabungan(self.nomor),i))

        
        pilihan.sort(reverse=True)
        print(pilihan)

        pilih = 0
        # pilih = random.randint(0, len(pilihan)-1)

        print("pilih:", pilihan[pilih][1])

        return pilihan[pilih][1];

# Class untuk mensimulasikan gerakan
class CongklakModelSim:
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

    # __pemain=0
    __sisi=0
    __langkah=0
    __biji=0


    def __init__(self, banyak):
        self.__lubang = [[4, 4, 4, 4, 4, 4, 4, 0],[4, 4, 4, 4, 4, 4, 4, 0]]
        self.MIN_BANYAK = banyak
        self.__pemain = 0

    def setLubang(self, set):
        self.__lubang = set

    def getState(self):
        return self.__lubang

    # mengembalikan isi lubang
    # memberi ketidakpastian isi BANYAK
    def getLubang(self, i):
        l = self.__lubang[i][0:7].copy()
        for i in range (self.N_LUBANG):
            if l[i] >= self.MIN_BANYAK :
                l[i] = self.ISI_BANYAK
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
