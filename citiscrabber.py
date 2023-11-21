import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import html
import re
#from database import VeritabaniIslemleri

class EczaneScraping:
    def __init__(self, il_data):
        self.il_data = il_data

    async def scrape_il(self, il_adi):
        print(il_adi)
        url = self.il_data.get(il_adi, {}).get('adres')  # İl için özel URL'yi alın
        print("# Site adresi : ",url)
        data = self.prepare_data(il_adi)  # İl için özel JSON verisini alın ve formatını düzenleyin
        element_tag = self.il_data.get(il_adi, {}).get('element_tag')  # İl için özel element_tag'ı alın
        element_class = self.il_data.get(il_adi, {}).get('element_class')
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
        if url:
            print(data)
            response = requests.post(url, data=data,headers=headers)  # Veriyi POST olarak gönderin
            print("# Nöbetcileri almak icin istek yapıldı...")
            decoded_text = html.unescape(response.text)
            soup = BeautifulSoup(decoded_text, "html.parser")
            eczane_raw_data = soup.find_all(element_tag, {"class": element_class})
            try:
                print("# Fonksiyona data yönlendiriliyor")
                fonksiyon = getattr(self, il_adi.lower())
                sonuc = fonksiyon(eczane_raw_data)
                return sonuc
            except AttributeError:
                return f"{il_adi} için geçerli bir fonksiyon bulunamadı"
            # İlgili ilin scraping işlemini burada devam ettirin
            # soup nesnesini kullanarak gerekli verileri çıkartabilirsiniz
            #print(stringler)

    def prepare_data(self, il_adi):
        il_verisi = self.il_data.get(il_adi, {})
        yeni_json = {}
        yeni_json = {key: value for key, value in il_verisi.items() if key not in ["adres", "element_tag", "element_class"]}
        city_request_data = {}
        for key, value in yeni_json.items():
            if key.startswith("tarih"):
                # Tarih formatlarını alıp gerçek tarihe çeviriyoruz
                tarih_format = re.sub(r'\bYYYY\b', r'%Y', value)
                tarih_format = re.sub(r'\bMM\b', r'%m', tarih_format)
                tarih_format = re.sub(r'\bDD\b', r'%d', tarih_format)
                tarih = datetime.now().strftime(tarih_format)
                
                # Oluşturulan tarih verisini request datasına ekliyoruz
                city_request_data[key] = tarih
            else:
                city_request_data[key] = value
        
        # İstenmeyen anahtarları temizliyoruz
            unwanted_keys = ['adres', 'element_tag', 'div', 'element_class', 'saat', 'url']
            cleaned_data = {key: value for key, value in city_request_data.items() if key not in unwanted_keys}
            request_data = cleaned_data
    
        return request_data

#scraping = EczaneScraping(il_urls)
#scraping.scrape_il("izmir")
    def izmir(self,scrabed_data):
        def replace_chars(s, chars_to_replace):
            for char, replacement in chars_to_replace.items():
                s = s.replace(char, replacement)
            return s
        pharma_data =[]
        for i in scrabed_data:
            eczane_isimleri = i.find("h4",{"class":"red"})
            telefonlar = i.find("a")
            bilgiler = i.find_all("p")
            ecza_adi,tarih_ilce = str(eczane_isimleri.text).split("-",1)
            link_konum = i.find("a",{"target":"_blank"},href=True)
            konum = link_konum['href']
            tarih,ilce = tarih_ilce.split("/")
            telefon=telefonlar.text

            for bilgi in bilgiler:
                ecz_bilgiler = str(bilgi.text).strip().replace("\t","").strip().splitlines()
                if len(ecz_bilgiler)>1:
                    adres=ecz_bilgiler[0]

            konum=konum[(konum.find("?q=")+3):]       
            il = "İzmir"
            chars_to_replace = {"ý": "i", "'": "", "Ð": "Ğ", "Ý": "İ", "Þ": "Ş", "þ": "ş", "ð": "ğ"}
            ecza_adi = replace_chars(ecza_adi, chars_to_replace)
            adres = replace_chars(adres, chars_to_replace)
            ilce = replace_chars(ilce,chars_to_replace)
            try:
                telefon = telefon.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
            except:
                print ("HATA VAR")
                pass
            if len(telefon)<10:
                telefon='232'+telefon
            if len(telefon)==11:
                telefon=telefon[1:]
            ilce=ilce.upper()
            print(telefon)
            print(ecza_adi.strip())
            print(adres)
            print(ilce.strip())
            print(konum)
            print(" ")
            pharma_data.append({"eczane_adi":ecza_adi.strip(),"telefon": telefon,"adres":adres, "ilce":ilce.strip(), "konum":konum.strip()})
        return pharma_data 
    def edirne(self,scrabed_data):
        def replace_chars(s, chars_to_replace):
            for char, replacement in chars_to_replace.items():
                s = s.replace(char, replacement)
            return s
        pharma_data =[]
        for i in scrabed_data:
            eczaneIsimleri,tarih = i.find("strong").text.split("-")
            telefon = i.find("i",{"class":"icon-phone"}).next_sibling.strip()
            adresler = i.find("i",{"class":"icon-home"}).next_sibling.strip().replace('\r', '').replace('\n', '')
            link_konum = i.find("a",{"target":"_blank"},href=True)
            ilceler = i.find("i",{"class":"icon-hand-right"}).next_sibling.strip()
            konum = link_konum['href']
            konum=konum[(konum.find("?q=")+3):]
            chars_to_replace = {"ý": "i", "'": "", "Ð": "Ğ", "Ý": "İ", "Þ": "Ş", "þ": "ş", "ð": "ğ"}
            ecza_adi = replace_chars(eczaneIsimleri, chars_to_replace)
            adresler = replace_chars(adresler, chars_to_replace)
            ilce = replace_chars(ilceler,chars_to_replace)
            print("# Edirne Dataları işleniyor.")
            try:
                telefon = telefon.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
            except:
                print ("HATA VAR")
                pass
            if len(telefon)<10:
                telefon='284'+telefon
            if len(telefon)==11:
                telefon=telefon[1:]
            print(tarih)
            if tarih.find("23:59") != -1:
                tarih = tarih[:tarih.find("23:59")]
                adresler = "23:59'A KADAR NÖBETÇİDİR " + adresler
            else:
                pass
            print(ecza_adi.strip())
            print(telefon)
            print(adresler)
            print(konum)
            print(ilce)
            print("------------------------")
            pharma_data.append({"eczane_adi":ecza_adi.strip(),"telefon": telefon,"adres":adresler, "ilce":ilce.strip(), "konum":konum.strip()})
        return pharma_data
    
    
    def denizli(self,scrabed_data,ilce):
        def replace_chars(s, chars_to_replace):
            for char, replacement in chars_to_replace.items():
                s = s.replace(char, replacement)
            return s
        pharma_data=[]
        for i in scrabed_data:
            eczane_isimleri = i.find("strong").text
            telefonlar = i.find("a")
            bilgiler = i.find_all("p")
            #ecza_adi,tarih_ilce = str(eczane_isimleri.text).split("-",1)
            link_konum = i.find("a",{"target":"_blank"},href=True)
            konum = link_konum['href']
            #tarih,ilce = tarih_ilce.split("/")
            telefon=telefonlar.text
            ilce="MERKEZ" #TODO: BU DISARDAN GELECEK
            for bilgi in bilgiler:
                ecz_bilgiler = str(bilgi.text).strip().replace("\t","").strip().splitlines()
                if len(ecz_bilgiler)>1:
                    adres=ecz_bilgiler[0]

            konum=konum[(konum.find("?q=")+3):konum.find("&ll=")]       
            il = "Denizli"
            chars_to_replace = {"ý": "i", "'": "", "Ð": "Ğ", "Ý": "İ", "Þ": "Ş", "þ": "ş", "ð": "ğ"}
            #eczane_isimleri = replace_chars(eczane_isimleri, chars_to_replace)
            #adres = replace_chars(adres, chars_to_replace)
            try:
                telefon = telefon.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
            except:
                print ("HATA VAR")
                pass
            if len(telefon)<10:
                telefon='258'+telefon
            if len(telefon)==11:
                telefon=telefon[1:]
            #ilce=ilce.upper()
            print(telefon)
            print(eczane_isimleri.strip())
            print(adres)
            #print(ilce.strip())
            print(konum)
            print(" ")
            #TODO: ILCE VERISI EKLENMELI
            pharma_data.append({"eczane_adi":eczane_isimleri.strip(),"telefon": telefon,"adres":adres, "ilce":ilce.strip(), "konum":konum.strip()})
        return pharma_data