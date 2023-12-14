import mysql.connector
import json
class Database:
    def __init__(self, config_file='db_conf.json'):
        self.config = self.load_config(config_file)
        self.connection = self.connect()

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            return json.load(f)

    def connect(self):
        return mysql.connector.connect(**self.config)

    def create_table(self, il_adi):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {il_adi} (eczane_adi VARCHAR(255), telefon VARCHAR(20), adres VARCHAR(255), ilce VARCHAR(50), konum VARCHAR(255), nobbastarih VARCHAR(255))")
            self.connection.commit()
        finally:
            cursor.close()

    def clear_and_insert_data(self, il_adi, data):
        self.create_table(il_adi)  # Tabloyu oluştur (varsa tekrar oluşturulmaz)
        
        cursor = self.connection.cursor()
        try:
            print(il_adi,"tablosuna işlem başlıyor")
            cursor.execute(f"DELETE FROM nobet_{il_adi}")  # Tablodaki eski verileri sil
            for uc_gunluk_eczane in data:
                for eczane in uc_gunluk_eczane:
                    print(eczane['eczane_adi'],"KAYIT EDILIYOR",eczane['tarih'])
                    cursor.execute(f"INSERT INTO nobet_{il_adi} (eczaneadi, telefonno, adres, ilce, konum, nobbastarih) VALUES (%s, %s, %s, %s, %s,%s)", (
                        eczane['eczane_adi'], eczane['telefon'], eczane['adres'], eczane['ilce'], eczane['konum'],eczane['tarih']))
            self.connection.commit()
        finally:
            cursor.close()
    def get_eczaneler_for_il(self, il_adi):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(f"SELECT eczaneadi, telefonno, adres, ilce, konum, nobbastarih FROM nobet_{il_adi}")
            eczaneler = cursor.fetchall()
            return eczaneler
        finally:
            cursor.close()
    def get_user_credentials(self, username, password):
        cursor = self.connection.cursor()

        # Kullanıcı adı ve şifreyi veritabanında kontrol etmek için sorguyu hazırlayın
        query = "SELECT * FROM nobet_users WHERE user_login=%s AND user_pass=%s"

        # Sorguyu çalıştırın
        cursor.execute(query, (username, password))

        # Sonucu alın
        user = cursor.fetchone()

        # Kullanıcı varsa True, yoksa False döndürün
        if user:
            return True  # Kullanıcı doğrulandı
        else:
            return False  # Kullanıcı doğrulanamadı
