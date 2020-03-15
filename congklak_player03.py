import random
# from congklak_model_sim import CongklakModelSim
from congklak_view import CongklakView
from congklak_player import CongklakPlayer
import copy
import time

class CongklakPlayer03(CongklakPlayer):

    def __init__(self):
        # Tune-able Requirements
        super().__init__('TIGA')
        self.blimit = 200 #limit lebar anak tiap node
        self.plyLimit = 4
        self.batasAtas = 20

        # Utility Function Parameters
        self.faktor_lanjut = 0
        self.faktor_ulang = 0
        self.faktor_tabung = 0
        self.faktor_tembak = 0
        self.faktor_mati = 0

        self.w0_1 = 0.9      #tabungan
        self.w0_2 = -0.5    #tabungan musuh
        self.w0_3 = 0.01    #total biji di sisi player
        self.w0_4 = -0.01    #biji di sisi musuh
        self.w1 = 0.001     #lanjut
        self.w2 = -1        #ulang
        self.w3 = 0.15       #tabung
        self.w4 = 0.15       #tembak
        self.w5 = -1         #mati

        self.inc = 50   #increment

    # Terkait Evaluation Function ---------------------
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
        eval += self.w1 * frontier.getFaktor()[0]
        eval += self.w2 * frontier.getFaktor()[1]
        eval += self.w3 * frontier.getFaktor()[2]
        eval += self.w4 * frontier.getFaktor()[3]
        eval += self.w5 * frontier.getFaktor()[4]

        # print(frontier.getFaktor())
        # print(eval)
        # time.sleep(1.5)
        # self.resetFaktor()
        # print("eval", eval)
        return eval

    # Untuk mensimulasikan hasil ketika suatu langkah dipilih
    # dari kondisi papan tertentu
    # oleh pemain dg nomor tertentu ------------------------
    def nextStep(self, papan, langkah, nomor):
        if papan.getPemain() != nomor:
            papan.gantian()

        if papan.bisaMain():
            status=papan.main(langkah)
        else:
            status = papan.S_MATI

        while status == papan.S_LANJUT:
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
        return nextState #kondisi lubang akhir setelah satu langkah

    # Untuk mendapatkan langkah yang bisa diambil
    # oleh pemain dg nomor tertentu
    # dari kondisi papan tertentu -------------------------
    def getNexts(self, papan, nomor):
        nexts = []
        lubang = papan.getLubang(nomor)

        for i in range(len(lubang)):
            if lubang[i] > 0 :
                nexts.append(i)

        return list(set(nexts));

    # Untuk cari cabang dari suatu node
    def cariCabang(self, node1, nomor):
        cabang = []
        nexts = self.getNexts(node1, nomor)
        for i in range(len(nexts)):
            node = copy.deepcopy(node1)
            pilih = nexts[i]
            nextNode = self.nextStep(node, pilih, nomor)
            a = CongklakModelSim(self.batasAtas)
            a.setLubang(nextNode)

            a.setFaktor([self.faktor_lanjut, self.faktor_ulang, self.faktor_tabung, self.faktor_tembak, self.faktor_mati])
            self.resetFaktor()

            cabang.append((pilih, a))
        return cabang

    # Untuk cari value max
    def cariMax(self, evalScore):
        score = []
        max = -9999
        for i in range(len(evalScore)):
            if (evalScore[i] > max):
                max = evalScore[i]
        #
        # for i in range(len(evalScore)):
        #     if (evalScore[i] >= max):
        #         score.append(evalScore[i])
        return max

    # Untuk cari value min
    def cariMin(self, evalScore):
        score = []
        min = 9999
        for i in range(len(evalScore)):
            if (evalScore[i] < min):
                min = evalScore[i]

        # for i in range(len(evalScore)):
        #     if (evalScore[i] == min):
        #         score.append(evalScore[i])
        return min

    def main(self, papan):
        score = []
        pilihan = []
        evalScore = []
        node = []
        plyLimits = self.plyLimit

        # somehow it worked ?
        if plyLimits%2 == 0:
            testlim = 0
        else:
            testlim = 1

        # Untuk mempersiapkan space
        for i in range(plyLimits):
            node.append([])
            score.append([])
            # evalScore.append([])

        for i in range(plyLimits):
            for j in range(self.blimit):
                score[i].append([])
                # evalScore[i].append([])

        node[0].append([])

        stateNol = [papan.getLubang(0), papan.getLubang(1)]
        stateNol[0].append(papan.getTabungan(0))
        stateNol[1].append(papan.getTabungan(1))

        papan2 = CongklakModelSim(self.batasAtas)
        papan2.setLubang(stateNol)

        node[0][0] = ((0,0), papan2, 0)

        # untuk mendapatkan seluruh node pada kedalaman selanjutnya
        for i in range(plyLimits-1):
            if i%2 == 0: #max ?
                no = self.nomor
            else: #min
                no = 1 - self.nomor

            for j in range(len(node[i])):
                if j < self.blimit:
                    cabang = self.cariCabang(node[i][j][1], no)
                    for k in range(len(cabang)):
                        parent = (i,j)
                        node[i+1].append((parent, cabang[k][1], cabang[k][0]))
                        # print((parent, cabang[k][1], cabang[k][0]))
            # print(len(node[i+1]))
            # time.sleep(1)
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
            # if parent[1] < self.blimit:
            if plyLimits%2 == testlim:
                no = self.nomor
            else:
                no = 1 - self.nomor

            # print(parent[0],parent[1])
            try:
                evalScore[parent[0]][parent[1]].append(self.evalFunc(frontier[i][1],no))
            except:
                if len(evalScore)-1 < parent[0]:
                    while len(evalScore)-1 < parent[0]:
                        evalScore.append([])
                if len(evalScore[parent[0]])-1 < parent[1]:
                    while len(evalScore[parent[0]])-1 < parent[1]:
                        evalScore[parent[0]].append([])

                evalScore[parent[0]][parent[1]].append(self.evalFunc(frontier[i][1],no))
                # print("FRONTIER", self.evalFunc(frontier[i][1],no))
                # CongklakView().tampilPapan(frontier[i][1])

        # Minimax
        for i in reversed(range(plyLimits-1)): #dari node kedua dr ujung ke node 0
            for j in range(len(node[i])): #lebar node ini
                if j < self.blimit:
                    # print(evalScore)
                    # print(i, j)
                    try:
                        print(i)
                        if i % 2 == 0: #max
                            print("MAX")
                            score[i][j] = self.cariMax(evalScore[i][j])
                        else:
                            print("Min")
                            score[i][j] = self.cariMin(evalScore[i][j])
                        # time.sleep(1)
                    except:
                        pass

            for j in range(len(node[i])):
                if j < self.blimit:
                    parent = [node[i][j][0][0], node[i][j][0][1]]
                    try:
                        evalScore[parent[0]][parent[1]].append(score[i][j])
                    except:
                        if len(evalScore)-1 < parent[0]:
                            while len(evalScore)-1 < parent[0]:
                                evalScore.append([])
                        if len(evalScore[parent[0]])-1 < parent[1]:
                            while len(evalScore[parent[0]])-1 < parent[1]:
                                evalScore[parent[0]].append([])
                        evalScore[parent[0]][parent[1]].append(score[i][j])

            # print(score)
            # print("--------")
            # time.sleep(1.5)

        if score[0][0] != []:
            # print(score)
            # time.sleep(1)
            for i in range(len(score[1])):
                if score[1][i] != []:
                    if score[1][i] == score[0][0]:
                        if node[1][i][2] not in pilihan:
                            pilihan.append((node[1][i][1].getTabungan(self.nomor), node[1][i][2]))
                            print("ALTERNATIF", node[1][i][2], score[node[1][i][0][0]][node[1][i][0][1]])
                            CongklakView().tampilPapan(node[1][i][1])

        # in case tidak nemu pilihan
        # ambil dari 1 ply aja
        if len(pilihan) <1 :
            testLubang = papan.getLubang(self.nomor)
            for i in range(len(testLubang)):
                if testLubang[i]>0:
                    pilihan.append((papan.getTabungan(self.nomor),i))

        # Diurutkan berdasarkan yang memberi tabungan terbanyak pada langkah selanjutnya
        pilihan.sort(reverse=True)
        print("OPSI:", pilihan)

        pilih = 0
        # pilih = random.randint(0, len(pilihan)-1)

        # print(evalScore)
        # print(score)

        print("pilih:", pilihan[pilih][1])
        # time.sleep(1.5)
        return pilihan[pilih][1];

# Class untuk mensimulasikan gerakan
# Tambahan fungis : GetState & SetState
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
        self.faktor_lanjut = 0
        self.faktor_ulang = 0
        self.faktor_tabung = 0
        self.faktor_tembak = 0
        self.faktor_mati = 0

    def getFaktor(self):
        return  self.faktor_lanjut, self.faktor_ulang, self.faktor_tabung, self.faktor_tembak, self.faktor_mati

    def setFaktor(self,set):
        self.faktor_lanjut, self.faktor_ulang, self.faktor_tabung, self.faktor_tembak, self.faktor_mati = set

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
