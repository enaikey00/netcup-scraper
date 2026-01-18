#!/usr/bin/env python3
"""
Bot Telegram Command Handler
Controlla se l'utente ha inviato comandi e li processa
"""

import requests
import json
import os
import sys
from datetime import datetime

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# File per salvare l'ultimo update_id processato
LAST_UPDATE_FILE = 'last_update_id.txt'


def get_last_update_id():
    """Legge l'ultimo update_id processato"""
    try:
        with open(LAST_UPDATE_FILE, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_last_update_id(update_id):
    """Salva l'ultimo update_id processato"""
    with open(LAST_UPDATE_FILE, 'w') as f:
        f.write(str(update_id))


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
        return True
    except Exception as e:
        print(f"❌ Errore nell'invio del messaggio Telegram: {e}")
        return False


def get_new_messages():
    """Recupera i nuovi messaggi da Telegram"""
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️ Token Telegram non configurato")
        return []
    
    last_update_id = get_last_update_id()
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    params = {
        'offset': last_update_id + 1,
        'timeout': 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data['ok'] and data['result']:
            return data['result']
        return []
    except Exception as e:
        print(f"❌ Errore nel recupero dei messaggi: {e}")
        return []


def process_commands():
    """Processa i comandi ricevuti"""
    messages = get_new_messages()
    
    if not messages:
        print("ℹ️ Nessun nuovo messaggio")
        return False
    
    print(f"📬 Trovati {len(messages)} nuovi messaggi")
    
    check_requested = False
    last_update_id = get_last_update_id()
    
    for update in messages:
        update_id = update['update_id']
        
        # Aggiorna l'ultimo update_id
        if update_id > last_update_id:
            last_update_id = update_id
        
        # Controlla se è un messaggio
        if 'message' not in update:
            continue
        
        message = update['message']
        
        # Verifica che sia dal chat_id corretto
        if str(message['chat']['id']) != str(TELEGRAM_CHAT_ID):
            print(f"⚠️ Messaggio ignorato da chat_id diverso: {message['chat']['id']}")
            continue
        
        # Estrai il testo del messaggio
        text = message.get('text', '').strip().lower()
        
        print(f"💬 Messaggio ricevuto: '{text}'")
        
        # Processa i comandi
        if text == '/check':
            print("✅ Comando /check ricevuto!")
            check_requested = True
            send_telegram_message("🔍 Controllo disponibilità in corso...\nRiceverai i risultati tra pochi secondi.")
        
        elif text == '/help':
            help_message = """
🤖 <b>Comandi disponibili:</b>

/check - Controlla subito la disponibilità dei VPS
/help - Mostra questo messaggio
/status - Mostra lo stato del monitoraggio

Il bot controlla automaticamente ogni ora e ti notifica quando cambia qualcosa!
"""
            send_telegram_message(help_message)
        
        elif text == '/status':
            status_message = f"""
📊 <b>Status del Bot</b>

✅ Bot attivo e funzionante
⏰ Controllo automatico: ogni ora
🔔 Notifiche: attive

Ultimo controllo messaggi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Usa /check per un controllo immediato.
"""
            send_telegram_message(status_message)
        
        elif text.startswith('/'):
            send_telegram_message(f"❓ Comando '{text}' non riconosciuto.\n\nUsa /help per vedere i comandi disponibili.")
    
    # Salva l'ultimo update_id processato
    if last_update_id > get_last_update_id():
        save_last_update_id(last_update_id)
        print(f"💾 Salvato update_id: {last_update_id}")
    
    return check_requested


def main():
    """Funzione principale"""
    print("=" * 60)
    print("🤖 Telegram Command Handler")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    check_requested = process_commands()
    
    print()
    print("=" * 60)
    
    if check_requested:
        print("✅ COMANDO /check RICEVUTO - Triggerando controllo VPS")
        print("=" * 60)
        # Ritorna exit code 0 per successo (GitHub Actions userà questo per decidere)
        sys.exit(0)
    else:
        print("ℹ️ Nessun comando /check ricevuto")
        print("=" * 60)
        # Ritorna exit code 1 per indicare "nessun comando"
        sys.exit(1)


if __name__ == "__main__":
    main()
