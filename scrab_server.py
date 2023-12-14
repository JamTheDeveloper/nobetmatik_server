import asyncio
import json
from datetime import datetime
from database import Database
from citiscrabber import EczaneScraping


'''
YAPILACAKLAR
1. Nöbet ara saat değişiklileri işlenmesi gerekli
2. Hata kısmında telegram bildirileri eklenmeli
4. Kendisinin çalışıp çalışmadığını bildirip-gözlenmleyebilmeliyiz
'''
# Load JSON data
def load_json_data(json_file):
    with open(json_file, 'r') as json_dosyasi:
        return json.load(json_dosyasi)

# Load settings
veriler = load_json_data('ecodasi_ayarlar.json')
iller = list(veriler.keys())

# Initialize scraper and database
scraper = EczaneScraping(veriler)
db = Database()
if db:
    print("Veritabanı bağlantısı kuruldu.")
# Scheduled scraping function
async def scheduled_scraping(il_adi):
    while True:
        veriler = load_json_data('ecodasi_ayarlar.json')
        now = datetime.now()
        saat = now.strftime("%H:%M")
        if saat == veriler[il_adi].get("saat"):
            scraped_data = await scraper.scrape_il(il_adi)
            if scraped_data:
                db.clear_and_insert_data(il_adi, scraped_data)

        await asyncio.sleep(20)

# Start scheduled scraping for each city
async def start_scheduled_scraping():
    tasks = [scheduled_scraping(il_adi) for il_adi in iller]
    await asyncio.gather(*tasks)


def load_json_data(json_file):
    with open(json_file, 'r') as json_dosyasi:
        return json.load(json_dosyasi)


async def scheduled_check_and_update():
    while True:
        for il_adi in iller:
            db.check_and_update_eczane(il_adi)  # Veritabanını kontrol eder ve güncelleme yapar
        await asyncio.sleep(10)  # Her dakika kontrol edilir



# Endpointleri oluşturma


if __name__ == "__main__":
    # Run scheduled scraping in the background
    asyncio.run(start_scheduled_scraping())

    #asyncio.run(scheduled_check_and_update())

    # Run the web server
    