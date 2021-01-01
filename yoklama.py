# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yoklama.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import face_recognition
import cv2
import numpy as np
import os
import glob
import sqlite3
from yoklamaListesi import Ui_Dialog_YoklamaListesi

class Ui_Dialog_Yoklama(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Öğrenci Yoklama Formu")
        Dialog.resize(971, 639)
        self.yoklamaAl = QtWidgets.QPushButton(Dialog)
        self.yoklamaAl.setGeometry(QtCore.QRect(90, 70, 241, 61))
        self.yoklamaAl.setObjectName("yoklamaAl")
        self.yoklamaKaydet = QtWidgets.QPushButton(Dialog)
        self.yoklamaKaydet.setGeometry(QtCore.QRect(90, 150, 241, 61))
        self.yoklamaKaydet.setObjectName("yoklamaKaydet")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(390, 60, 271, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(390, 130, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(390, 180, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.yoklamaListesi = QtWidgets.QPushButton(Dialog)
        self.yoklamaListesi.setGeometry(QtCore.QRect(90, 230, 241, 16))
        self.yoklamaListesi.setObjectName("yoklamaListesi")
        self.ogrenciAd = QtWidgets.QLabel(Dialog)
        self.ogrenciAd.setGeometry(QtCore.QRect(530, 150, 91, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        self.ogrenciAd.setFont(font)
        self.ogrenciAd.setObjectName("ogrenciAd")
        self.ogrenciNumara = QtWidgets.QLabel(Dialog)
        self.ogrenciNumara.setGeometry(QtCore.QRect(580, 200, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        self.ogrenciNumara.setFont(font)
        self.ogrenciNumara.setObjectName("ogrenciNumara")

        self.yoklamaAl.clicked.connect(self.yoklamaAlButton)
        self.yoklamaKaydet.clicked.connect(self.yoklamaKaydetButton)
        self.yoklamaListesi.clicked.connect(self.yoklamaListesiButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    # YOKLAMA LISTESI
    def yoklamaListesiButton(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Dialog_YoklamaListesi()  # acilacak pencerenin class ismi
        self.ui.setupUi(self.window)
        self.window.show()

    # GÖRÜNTÜ ALIP -> BİLGİLERİ YAZDIRMA
    def yoklamaAlButton(self):
        faces_encodings = []
        faces_names = []
        cur_direc = os.getcwd()
        path = os.path.join(cur_direc, 'images/')
        list_of_files = [f for f in glob.glob(path + '*.jpg')]

        number_files = len(list_of_files)
        names = list_of_files.copy()

        for i in range(number_files):
            globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
            globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[
                0]
            faces_encodings.append(globals()['image_encoding_{}'.format(i)])
            # Create array of known names
            names[i] = names[i].replace(cur_direc, "")
            faces_names.append(names[i])

        #print(names)

        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        video_capture = cv2.VideoCapture(0)
        video_capture.set(3, 640)  # video genişliğini belirle
        video_capture.set(4, 480)  # video yüksekliğini belirle

        while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(faces_encodings, face_encoding)
                name = "Bilinmiyor"
                self.ogrenciAd.setText(name)

                face_distances = face_recognition.face_distance(faces_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = faces_names[best_match_index]
                    #print(name)
                    faces_names.append(names[i])

                    try:
                        # veritabanina baglandik
                        baglanti = sqlite3.connect("veritabani.db")
                        cursor = baglanti.cursor()
                        # print("Veritabanına başarılı bir şekilde bağlanıldı!")

                        def convertTuple(tup):
                            str = ' '.join(tup)
                            return str

                        cursor.execute("SELECT isim FROM uyeler WHERE gorselyol = '%s'" % name)
                        rows = cursor.fetchall()

                        degisken = convertTuple(rows[0])

                        self.ogrenciAd.setText(degisken)

                        #print("resimdeki kişi : " + degisken)
                        cursor.close()

                    except sqlite3.Error as error:
                        print("veritabanına bağlanırken sorun oluştu! SORUN : ", error)
                    finally:
                        if (baglanti):
                            baglanti.close()
                            # print("Veritabanı kapatıldı!")

                face_names.append(name)

            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Input text label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                # Display the resulting image
                cv2.imshow('Video', frame)
                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(0) & 0xFF == ord('e'): # e-> q idi -- 0-> 1 idi
                    break
                cv2.destroyAllWindows()

    # YOKLAMA KAYDET
    def yoklamaKaydetButton(self):
        if self.ogrenciAd.text() == "Bilinmiyor":
            print("Kayıt işlemi gerçekleştirilemedi !")
        else:
            try:

                def convertTuple(tup):
                    str = ' '.join(tup)
                    return str

                # veritabanina baglandik
                baglanti = sqlite3.connect("deneme.db")
                cursor = baglanti.cursor()

                #print("Veritabanına başarılı bir şekilde bağlanıldı!")
                yoklama_isim = self.ogrenciAd.text()
                #cursor.execute("SELECT isim FROM yoklama WHERE isim = '%s'" % yoklama_isim)
                #cursor.execute("SELECT isim FROM yoklama")
                cursor.execute("SELECT isim FROM yoklama WHERE isim = '%s'" % yoklama_isim)
                rows = cursor.fetchall()
                # for i in rows:
                #     if yoklama_isim == convertTuple(i):
                #         print("eslesiyor")
                #     else:
                #         print("eslesmiyor")
                #print(len(rows))
                if len(rows) == 0:

                    cursor.execute("INSERT INTO yoklama(isim) VALUES('%s')" % yoklama_isim)  # verileri execute ettik! (veritbanina ekledik)
                    baglanti.commit()

                    print("veriler eklendi!")
                    cursor.close()

                else:
                    if yoklama_isim == convertTuple(rows[0]):
                        print("kayit var")


            except sqlite3.Error as error:
                print("veritabanına bağlanırken sorun oluştu! SORUN : ", error)

            finally:
                if (baglanti):
                    baglanti.close()
                    #print("Veritabanı kapatıldı!")


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Öğrenci Yoklama Formu"))
        self.yoklamaAl.setText(_translate("Dialog", "YOKLAMA AL"))
        self.yoklamaKaydet.setText(_translate("Dialog", "YOKLAMA KAYDET"))
        self.label.setText(_translate("Dialog", "Taratılan Kişi Bilgileri"))
        self.label_2.setText(_translate("Dialog", "Öğrenci Adı :"))
        self.label_3.setText(_translate("Dialog", "Öğrenci Numarası : "))
        self.yoklamaListesi.setText(_translate("Dialog", "GÜNCEL YOKLAMA LİSTESİ"))
        self.ogrenciAd.setText(_translate("Dialog", "Bilinmiyor"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_Yoklama()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
