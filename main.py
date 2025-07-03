from keep_alive import keep_alive
from threading import Thread
import requests
from bs4 import BeautifulSoup
import time

# 🔐 Telegram-Zugangsdaten
TOKEN = '7642753536:AAGvC7tCzTw2wYal9Ng2d0fvI5_AyCSaRIc'
CHAT_ID = '7934241910'

# 🌐 Deine Such-URL
URL = 'https://www.kleinanzeigen.de/s-80939/preis::100/motorroller/k0l16357r30'

# 🧠 Merkt sich gesendete Anzeigen
gesehene_urls = set()

def sende_telegram_nachricht(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': text}
    requests.get(url, params=payload)

def suche_neue_anzeigen():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    anzeigen = soup.select('.aditem')
    print(f'🔍 {len(anzeigen)} Anzeigen gefunden.')

    for ad in anzeigen:
        link_tag = ad.select_one('a[href]')
        if not link_tag:
            continue

        relative_url = link_tag['href']
        titel_tag = ad.select_one('.text-module-begin')
        titel = titel_tag.get_text(strip=True) if titel_tag else 'Keine Beschreibung'

        voll_url = 'https://www.kleinanzeigen.de' + relative_url

        if voll_url not in gesehene_urls:
            gesehene_urls.add(voll_url)
            nachricht = f'🛵 Neuer Motorroller:\n{titel}\n{voll_url}'
            sende_telegram_nachricht(nachricht)
            print(f'➡️ Neue Anzeige geschickt: {titel}')
            time.sleep(1)

def bot_loop():
    while True:
        try:
            suche_neue_anzeigen()
        except Exception as e:
            print(f'⚠️ Fehler: {e}')
        time.sleep(60)  # Alle 60 Sekunden neu prüfen

# 🔁 Start
keep_alive()
Thread(target=bot_loop).start()
