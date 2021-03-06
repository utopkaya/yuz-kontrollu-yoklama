# yuz-kontrollu-yoklama
Python ile yüz kontrollü kayıt ve yoklama uygulaması

Uyglamayı çalıştırmadan yüklenmesi gereken paketler şu şekilde kurulabilir.

  * pip install opencv-python
  * pip install pyqt5
  * pip install cmake
  * pip install dlib
  * pip install face_recognition
  
bitis.py'de kayıt yaptırılarak aynı aynda fotoğraf çekilir ve veritabananı.db'ye girilen bilgiler doğrultusunda veriler ve akabinde çekilen görüntünün yolu kaydedilir.
çekilen fotoğraf images klasörü altında girilen isim şeklinde jpg uzantı olacak biçimde kaydedilir.
yoklama alınmak istendiğinde görüntü tanımlanır ve veritabanın'daki kayıtla eşleştiğinde yoklama veritabanına kaydedilir. Eğer görüntü tanımlamaz ise bilinmiyor mesajını alırız ve yoklamayı alamayız.

Önemli not : projenin dizininde images adlı klasör oluşturmalısınız. (Kayıt edilen görüntüler bu klasör içerisinde barınacaktır)
Diğer not : Hem kamera penceresi hem de tasarım ile ilgili ilerleyen zamanda güncelleme gelecktir.
