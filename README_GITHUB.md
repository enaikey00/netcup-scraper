# Netcup VPS ARM Availability Scraper 🤖

Scraper automatico che controlla ogni ora la disponibilità dei VPS ARM su netcup.com e invia notifiche Telegram quando trova disponibilità.

[![Check VPS Availability](https://github.com/TUO_USERNAME/netcup-scraper/actions/workflows/check-availability.yml/badge.svg)](https://github.com/TUO_USERNAME/netcup-scraper/actions/workflows/check-availability.yml)

## 🎯 Prodotti monitorati
- VPS 1000 ARM G11
- VPS 2000 ARM G11
- VPS 3000 ARM G11

## ⚡ Features
- ✅ Controlli automatici ogni ora tramite GitHub Actions
- 📱 Notifiche Telegram quando un prodotto diventa disponibile
- 📊 Storico completo salvato come artifact su GitHub
- 🆓 Completamente gratuito (GitHub Actions free tier)
- 🔔 Notifiche solo quando cambia lo stato (evita spam)

## 🚀 Setup

### 1. Crea il Bot Telegram

1. Apri Telegram e cerca `@BotFather`
2. Invia `/newbot`
3. Scegli un nome per il bot (es. "Netcup VPS Monitor")
4. Scegli uno username (es. "netcup_vps_bot")
5. **Copia il token** che ti viene dato (formato: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Ottieni il tuo Chat ID

**Metodo facile:**
1. Cerca il bot `@userinfobot` su Telegram
2. Invia `/start`
3. **Copia il tuo ID** (è un numero tipo `123456789`)

**Metodo alternativo:**
1. Invia un messaggio al tuo bot (quello creato con BotFather)
2. Vai su: `https://api.telegram.org/bot<TUO_TOKEN>/getUpdates`
3. Cerca `"chat":{"id":123456789}` nella risposta

### 3. Configura GitHub

1. **Fork questo repository** (o caricalo sul tuo GitHub)

2. Vai su **Settings** → **Secrets and variables** → **Actions**

3. Aggiungi questi secrets (click su "New repository secret"):
   - **Nome**: `TELEGRAM_BOT_TOKEN`  
     **Valore**: Il token del bot (es. `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
   
   - **Nome**: `TELEGRAM_CHAT_ID`  
     **Valore**: Il tuo chat ID (es. `123456789`)

### 4. Attiva GitHub Actions

1. Vai nella tab **Actions** del repository
2. Click su "I understand my workflows, go ahead and enable them"
3. Il workflow partirà automaticamente ogni ora!

## 🧪 Test manuale

Puoi testare il workflow manualmente:

1. Vai su **Actions** → **Check VPS Availability**
2. Click su "Run workflow" → "Run workflow"
3. Aspetta ~30 secondi
4. Riceverai un messaggio Telegram con i risultati!

## 📱 Esempio notifica Telegram

```
🔍 Netcup VPS ARM Check
📅 2026-01-18 14:30:00 UTC

✅ VPS 1000 ARM G11: AVAILABLE 🆕 ORA DISPONIBILE!
   🔗 Ordina ora!

❌ VPS 2000 ARM G11: SOLD OUT

❌ VPS 3000 ARM G11: SOLD OUT

🚀 AZIONE RICHIESTA: Prodotti disponibili!
```

## ⚙️ Personalizzazione

### Cambiare frequenza dei controlli

Modifica `.github/workflows/check-availability.yml`:

```yaml
schedule:
  - cron: '0 * * * *'  # Ogni ora
  # - cron: '*/30 * * * *'  # Ogni 30 minuti
  # - cron: '0 */2 * * *'  # Ogni 2 ore
  # - cron: '0 9-17 * * *'  # Solo dalle 9 alle 17
```

⚠️ **Nota**: GitHub Actions può avere ritardi di ~5-15 minuti nelle esecuzioni scheduled.

### Aggiungere/rimuovere prodotti

Modifica `scraper_github_actions.py`, sezione `PRODUCTS`:

```python
PRODUCTS = [
    {
        "name": "VPS 1000 ARM G11",
        "url": "https://www.netcup.com/en/server/arm-server/vps-1000-arm-g11-iv-mnz"
    },
    # Aggiungi altri prodotti qui
]
```

## 📊 Visualizzare lo storico

1. Vai su **Actions**
2. Click su un workflow completato
3. Scarica l'artifact `availability-log-XXX`
4. Apri `availability_log.json` per vedere tutti i check

## 🐛 Troubleshooting

### Non ricevo notifiche Telegram

1. Verifica che i secrets siano configurati correttamente
2. Assicurati di aver avviato il bot (invia `/start` al tuo bot)
3. Controlla i log in Actions per errori

### Il workflow non parte

1. Verifica che GitHub Actions sia abilitato (tab Actions)
2. Il primo run potrebbe richiedere fino a 1 ora
3. Usa "Run workflow" per testare manualmente

### Ricevo troppe notifiche

Lo scraper invia notifiche solo quando:
- Un prodotto diventa disponibile
- Cambia lo stato di un prodotto

Se ricevi troppe notifiche, potrebbe esserci un problema di rilevamento. Apri una issue!

## 🧑‍💻 Sviluppo locale

Per testare in locale:

```bash
# Installa dipendenze
pip install -r requirements_light.txt

# Configura variabili d'ambiente
export TELEGRAM_BOT_TOKEN="tuo_token"
export TELEGRAM_CHAT_ID="tuo_chat_id"

# Esegui
python scraper_github_actions.py
```

## 📝 Note

- Lo scraper fa richieste HTTP semplici (lightweight)
- GitHub Actions free tier: 2000 minuti/mese (più che sufficiente)
- I log vengono mantenuti per 30 giorni
- Rispetta il server di netcup con pause tra le richieste

## 🤝 Contributi

Pull requests sono benvenute! Per cambiamenti importanti, apri prima una issue.

## 📄 Licenza

MIT License - Usa liberamente!

---

**Made with ❤️ for VPS hunters** 🎯
