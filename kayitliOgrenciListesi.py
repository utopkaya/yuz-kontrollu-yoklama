# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'kayitliListe.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class Ui_Dialog_List(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Kayıtlı Öğrenci Listesi")
        Dialog.resize(400, 515)
        self.yoklamaListWidget = QtWidgets.QListWidget(Dialog)
        self.yoklamaListWidget.setGeometry(QtCore.QRect(70, 80, 256, 401))
        self.yoklamaListWidget.setObjectName("yoklamaListWidget")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 40, 251, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # VERİLERİ LİSTELEME
        try:
            # veritabanina baglandik
            baglanti = sqlite3.connect("veritabani.db")
            cursor = baglanti.cursor()
            print("Veritabanına başarılı bir şekilde bağlanıldı!")

            cursor.execute("SELECT * FROM uyeler")
            rows = cursor.fetchall()

            #for row in rows:
            #self.yoklamaListWidget = QtWidgets.QListWidget(Dialog)
            for row in rows:
                self.yoklamaListWidget.addItem(row[1])
            self.yoklamaListWidget.show();

            cursor.close()

        except sqlite3.Error as error:
            print("veritabanına bağlanırken sorun oluştu! SORUN : ", error)
        finally:
            if(baglanti):
                baglanti.close()
                #print("Veritabanı kapatıldı!")

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Kayıtlı Öğrenci Listesi"))
        self.label.setText(_translate("Dialog", "Kayıtlı Öğrenciler"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_List()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

