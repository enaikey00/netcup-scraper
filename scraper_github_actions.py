#!/usr/bin/env python3
"""
Netcup VPS ARM Availability Scraper - GitHub Actions Version
Controlla la disponibilità e invia notifiche Telegram
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import sys

# Configurazione
PRODUCTS = [
    {
        "name": "VPS 1000 ARM G11",
        "url": "https://www.netcup.com/en/server/arm-server/vps-1000-arm-g11-iv-mnz"
    },
    {
        "name": "VPS 2000 ARM G11",
        "url": "https://www.netcup.com/en/server/arm-server/vps-2000-arm-g11-iv-mnz"
    },
    {
        "name": "VPS 3000 ARM G11",
        "url": "https://www.netcup.com/en/server/arm-server/vps-3000-arm-g11-mnz"
    }
]

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def send_telegram_message(message, parse_mode='HTML'):
    """Invia un messaggio su Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Token Telegram o Chat ID non configurati")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': parse_mode,
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Messaggio Telegram inviato con successo")
        return True
    except Exception as e:
        print(f"❌ Errore nell'invio del messaggio Telegram: {e}")
        return False


def check_availability(product):
    """Controlla la disponibilità di un singolo prodotto"""
    try:
        print(f"Controllando {product['name']}...")
        
        response = requests.get(product['url'], headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        page_text = soup.get_text().lower()
        
        # Determina disponibilità
        if 'sold out' in page_text or 'product is sold out' in page_text:
            available = False
            status = "SOLD OUT"
        elif 'add to shopping cart' in page_text or 'order now' in page_text:
            available = True
            status = "AVAILABLE"
        else:
            # Cerca nei button
            buttons = soup.find_all('button')
            available = None
            status = "UNKNOWN"
            
            for button in buttons:
                button_text = button.get_text().strip().lower()
                if 'sold out' in button_text:
                    available = False
                    status = "SOLD OUT"
                    break
                elif 'add to' in button_text or 'cart' in button_text:
                    available = True
                    status = "AVAILABLE"
                    break
        
        print(f"  → {product['name']}: {status}")
        
        return {
            'name': product['name'],
            'url': product['url'],
            'available': available,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        return {
            'name': product['name'],
            'url': product['url'],
            'available': None,
            'status': "ERROR",
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def load_previous_results():
    """Carica i risultati precedenti se esistono"""
    try:
        with open('availability_log.json', 'r') as f:
            data = json.load(f)
            if data:
                return data[-1]['results']  # Ritorna l'ultimo check
    except (FileNotFoundError, json.JSONDecodeError, IndexError, KeyError):
        pass
    return None


def save_results(results):
    """Salva i risultati nel file di log"""
    try:
        # Leggi dati esistenti
        try:
            with open('availability_log.json', 'r') as f:
                log_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            log_data = []
        
        # Aggiungi nuovi risultati
        log_entry = {
            'check_time': datetime.now().isoformat(),
            'results': results
        }
        log_data.append(log_entry)
        
        # Mantieni solo gli ultimi 100 check per non far crescere troppo il file
        if len(log_data) > 100:
            log_data = log_data[-100:]
        
        # Salva
        with open('availability_log.json', 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print("✅ Risultati salvati in availability_log.json")
        
    except Exception as e:
        print(f"❌ Errore nel salvare i risultati: {e}")


def format_telegram_message(results, previous_results=None):
    """Formatta il messaggio per Telegram"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    message = f"🔍 <b>Netcup VPS ARM Check</b>\n"
    message += f"📅 {now}\n\n"
    
    any_available = False
    changes_detected = False
    
    for result in results:
        emoji = "✅" if result['available'] else "❌" if result['available'] is False else "❓"
        
        # Controlla se c'è stato un cambio di stato
        status_change = ""
        if previous_results:
            prev = next((p for p in previous_results if p['name'] == result['name']), None)
            if prev and prev.get('available') != result['available']:
                if result['available']:
                    status_change = " 🆕 <b>ORA DISPONIBILE!</b>"
                    changes_detected = True
                elif result['available'] is False and prev.get('available'):
                    status_change = " ⚠️ Tornato esaurito"
                    changes_detected = True
        
        message += f"{emoji} <b>{result['name']}</b>: {result['status']}{status_change}\n"
        
        if result['available']:
            any_available = True
            message += f"   🔗 <a href='{result['url']}'>Ordina ora!</a>\n"
        
        message += "\n"
    
    # Aggiungi footer
    if any_available:
        message += "🚀 <b>AZIONE RICHIESTA: Prodotti disponibili!</b>"
    elif changes_detected:
        message += "ℹ️ Cambio di stato rilevato"
    
    return message, any_available, changes_detected


def main():
    """Funzione principale"""
    print("=" * 60)
    print(f"🤖 Netcup VPS ARM Availability Check - GitHub Actions")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Carica risultati precedenti
    previous_results = load_previous_results()
    
    # Esegui check
    results = []
    for product in PRODUCTS:
        result = check_availability(product)
        results.append(result)
    
    # Salva risultati
    save_results(results)
    
    # Prepara messaggio Telegram
    message, any_available, changes_detected = format_telegram_message(results, previous_results)
    
    # Invia notifica Telegram solo se:
    # 1. C'è almeno un prodotto disponibile, OPPURE
    # 2. C'è stato un cambio di stato
    should_notify = any_available or changes_detected
    
    if should_notify:
        print("\n📱 Invio notifica Telegram...")
        send_telegram_message(message)
    else:
        print("\n⏭️  Nessun cambio di stato, notifica saltata")
        print(f"💬 Messaggio che sarebbe stato inviato:\n{message}")
    
    # Mostra riepilogo
    print("\n" + "=" * 60)
    print("📊 RIEPILOGO:")
    for result in results:
        emoji = "✅" if result['available'] else "❌" if result['available'] is False else "❓"
        print(f"  {emoji} {result['name']}: {result['status']}")
    print("=" * 60)
    
    # Exit code: 0 se tutto ok, 1 se ci sono errori
    has_errors = any(r['status'] == 'ERROR' for r in results)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
