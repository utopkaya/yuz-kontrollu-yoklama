# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'program.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

# VERITABANI DB

from PyQt5 import QtCore, QtGui, QtWidgets
from kayitliOgrenciListesi import Ui_Dialog_List
from yoklama import Ui_Dialog_Yoklama
import sqlite3

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(607, 430)
        self.ad = QtWidgets.QLineEdit(Dialog)
        self.ad.setGeometry(QtCore.QRect(40, 80, 321, 41))
        self.ad.setObjectName("ad")
        self.numara = QtWidgets.QLineEdit(Dialog)
        self.numara.setGeometry(QtCore.QRect(40, 180, 321, 41))
        self.numara.setObjectName("numara")
        self.cinsiyet = QtWidgets.QLineEdit(Dialog)
        self.cinsiyet.setGeometry(QtCore.QRect(40, 280, 321, 41))
        self.cinsiyet.setObjectName("cinsiyet")
        self.resimCek = QtWidgets.QPushButton(Dialog)
        self.resimCek.setGeometry(QtCore.QRect(30, 340, 331, 51))
        self.resimCek.setObjectName("resimCek")
        self.yoklamaAl = QtWidgets.QPushButton(Dialog)
        self.yoklamaAl.setGeometry(QtCore.QRect(410, 130, 161, 51))
        self.yoklamaAl.setObjectName("yoklamaAl")
        self.yoklamaListesi = QtWidgets.QPushButton(Dialog)
        self.yoklamaListesi.setGeometry(QtCore.QRect(410, 70, 161, 51))
        self.yoklamaListesi.setObjectName("yoklamaListesi")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 40, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 150, 121, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 250, 121, 16))
        self.label_3.setObjectName("label_3")

        self.resimCek.clicked.connect(self.veriEkle)
        self.yoklamaListesi.clicked.connect(self.kayitliOgrenciListeleButton)

        self.yoklamaAl.clicked.connect(self.yoklamaAlPencereButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    # VERI EKLEME
    def veriEkle(self):
        # !/usr/bin/env python3
        # -*- coding: utf-8 -*-
        """
        Created on Wed Dec 30 01:30:43 2020

        @author: umuttopkaya
        """

        # Original code from https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826

        import cv2

        isim =  self.ad.text()
        numara =  self.numara.text()
        cinsiyet =  self.cinsiyet.text()
        imgyol = "/images/"+isim+".jpg"

        kamera = cv2.VideoCapture(0)
        kamera.set(3, 640)  # video genişliğini belirle
        kamera.set(4, 480)  # video yüksekliğini belirle
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # Her farklı kişi için farklı bir yüz tamsayısı ata
        # face_id = input('\n enter user id end press <return> ==>  ')
        MAXFOTOSAY = 1  # Her bir yüz için kullanılacak imaj sayısı
        face_id = isim
        print("\n [INFO] Kayıtlar başlıyor. Kameraya bak ve bekle ...")

        say = 0

        # FOTOĞRAF ÇEKME İŞLEMİ
        while (True):
            ret, img = kamera.read()
            # img = cv2.flip(img, -1) # gerekiyorsa kullan
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            yuzler = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in yuzler:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                say += 1
                # Yakalanan imajı veriseti klasörüne kaydet
                cv2.imwrite("images/" + str(face_id) + ".jpg", gray[y:y + h, x:x + w])
                cv2.imshow('imaj', img)
                print("Kayıt no: ", say)
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
            elif say >= MAXFOTOSAY:
                break
        # Belleği temizle
        print("\n [INFO] Program sonlanıyor ve bellek temizleniyor.")
        kamera.release()
        cv2.destroyAllWindows()

        # ÇEKİLEN RESİMLE BİRLİKTE DOLDURULAN FORMUN VERİTABANINA KAYIT İŞLEMİ
        try:

            # veritabanina baglandik
            baglanti = sqlite3.connect("veritabani.db")
            cursor = baglanti.cursor()

            print("Veritabanına başarılı bir şekilde bağlanıldı!")

            yol = "images/" + isim + ".jpg"
            with open(yol, "rb") as file:
                veri = file.read()
                # return veri

            sorgu = "INSERT INTO uyeler(isim, numara, cinsiyet, gorsel, gorselyol) VALUES(?,?,?,?,?)"  # verileri execute ettik! (veritbanina ekledik)

            veriler = (isim, numara, cinsiyet, veri, imgyol)  # ? yerine gececek veriler
            cursor.execute(sorgu, veriler)
            baglanti.commit()

            print("veriler eklendi!")
            cursor.close()

        except sqlite3.Error as error:
            print("veritabanına bağlanırken sorun oluştu! SORUN : ", error)

        finally:
            if (baglanti):
                baglanti.close()
                print("Veritabanı kapatıldı!")

    # KAYIT LİSTESİ GÖRÜNTÜLEME
    def kayitliOgrenciListeleButton(self):
        print("liste") # DEVAM ET

        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Dialog_List() # acilacak pencerenin class ismi
        self.ui.setupUi(self.window)
        self.window.show()

    # YOKLAMA ALMA PENCERESİNE YÖNLENDİRME
    def yoklamaAlPencereButton(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Dialog_Yoklama()  # acilacak pencerenin class ismi
        self.ui.setupUi(self.window)
        self.window.show()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Öğrenci Kayıt Formu"))
        self.resimCek.setText(_translate("Dialog", "Resim Çek ve Kaydet"))
        self.yoklamaAl.setText(_translate("Dialog", "Yoklama Al"))
        self.yoklamaListesi.setText(_translate("Dialog", "Kayitli Öğrenci Listesi"))
        self.label.setText(_translate("Dialog", "AD ve SOYAD"))
        self.label_2.setText(_translate("Dialog", "OKUL NUMARASI"))
        self.label_3.setText(_translate("Dialog", "CİNSİYET"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

