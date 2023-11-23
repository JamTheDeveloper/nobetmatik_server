FROM ubuntu

WORKDIR /app

# Gerekli paketleri yükle
RUN apt update && apt install -y git

# Depoyu klonla
RUN git clone https://github.com/JamTheDeveloper/nobetmatik_server.git nobetmatik_server

# Uygulama dizinine gir ve gereksinimleri yükle
WORKDIR /app/nobetmatik_server
RUN apt install -y python3-pip
RUN pip install -r requirements.txt

# Uygulamayı çalıştır
CMD [ "python3", "scrab_server.py" ]
