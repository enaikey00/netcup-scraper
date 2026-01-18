# 🚀 Guida Setup GitHub Actions + Telegram

Segui questi passi per configurare il monitoring automatico.

## Parte 1️⃣: Crea il Bot Telegram (5 minuti)

### Step 1: Apri Telegram e cerca BotFather

1. Apri Telegram (app o web)
2. Cerca `@BotFather` nella barra di ricerca
3. Clicca su START

### Step 2: Crea il bot

Invia questi messaggi a BotFather:

```
/newbot
```

BotFather ti chiederà il nome del bot. Rispondi con:
```
Netcup VPS Monitor
```

Poi ti chiederà lo username. Deve finire con "bot". Esempio:
```
netcup_vps_monitor_bot
```

### Step 3: Salva il Token

BotFather ti darà un messaggio tipo:

```
Done! Congratulations on your new bot...
Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
```

**✏️ COPIA QUESTO TOKEN** e salvalo in un file di testo temporaneo.

---

## Parte 2️⃣: Ottieni il tuo Chat ID (2 minuti)

### Metodo 1 (più facile):

1. Cerca `@userinfobot` su Telegram
2. Invia `/start`
3. Ti risponderà con il tuo ID (un numero tipo `123456789`)
4. **✏️ COPIA QUESTO NUMERO** e salvalo

### Metodo 2 (alternativo):

1. Invia un messaggio qualsiasi al tuo bot (quello creato prima)
2. Apri nel browser: `https://api.telegram.org/bot<IL_TUO_TOKEN>/getUpdates`
   (sostituisci `<IL_TUO_TOKEN>` con il token che hai copiato)
3. Cerca nel JSON la parte `"chat":{"id":123456789}`
4. **✏️ COPIA IL NUMERO** (il tuo Chat ID)

---

## Parte 3️⃣: Carica su GitHub (10 minuti)

### Step 1: Crea un nuovo repository

1. Vai su https://github.com/new
2. Nome repository: `netcup-scraper` (o quello che vuoi)
3. **Importante**: Metti PRIVATO se non vuoi che altri vedano i tuoi check
4. Click su "Create repository"

### Step 2: Carica il codice

**Opzione A - Da terminale** (se hai git installato):

```bash
cd /Users/miniops/Desktop/Universe/netcup-scraper

# Inizializza git se non l'hai fatto
git init
git add .
git commit -m "Initial commit"

# Collega al repository (sostituisci TUO_USERNAME)
git remote add origin https://github.com/TUO_USERNAME/netcup-scraper.git
git branch -M main
git push -u origin main
```

**Opzione B - Dalla UI di GitHub**:

1. Sul tuo repository appena creato, click su "uploading an existing file"
2. Trascina tutti i file dalla cartella `netcup-scraper`
3. Click su "Commit changes"

### Step 3: Configura i Secrets

1. Nel tuo repository, vai su **Settings** (in alto)
2. Nella barra laterale: **Secrets and variables** → **Actions**
3. Click su **New repository secret**

**Primo secret:**
- Name: `TELEGRAM_BOT_TOKEN`
- Secret: Incolla il token del bot (quello che hai salvato)
- Click "Add secret"

**Secondo secret:**
- Click di nuovo su "New repository secret"
- Name: `TELEGRAM_CHAT_ID`
- Secret: Incolla il tuo Chat ID (quello che hai salvato)
- Click "Add secret"

### Step 4: Attiva GitHub Actions

1. Vai sulla tab **Actions** (in alto nel repository)
2. Se vedi "Workflows aren't being run on this forked repository"
   → Click su "I understand my workflows, go ahead and enable them"

---

## Parte 4️⃣: Test! (2 minuti)

### Test manuale

1. Vai su **Actions**
2. Nella barra laterale sinistra, click su "Check VPS Availability"
3. Click sul bottone "Run workflow" (a destra)
4. Click su "Run workflow" (verde)
5. Aspetta 30-60 secondi
6. **Dovresti ricevere un messaggio Telegram!** 🎉

### Controlla i risultati

1. Click sul workflow che è appena partito (nella lista)
2. Click su "check-availability"
3. Espandi i vari step per vedere i log
4. Se vedi errori, controlla che i secrets siano corretti

---

## ✅ Fatto!

Da ora in poi:
- ⏰ Il check partirà **automaticamente ogni ora**
- 📱 Riceverai notifiche **solo quando cambia qualcosa**
- 📊 Puoi vedere lo storico scaricando gli artifacts

---

## 🐛 Problemi comuni

### "Error: HttpError: Not Found"
→ I secrets non sono configurati. Torna allo Step 3 della Parte 3.

### "Unauthorized" nel messaggio Telegram
→ Il token del bot è sbagliato. Verifica lo Step 3 della Parte 3.

### "Chat not found"
→ Non hai avviato il bot. Cerca il tuo bot su Telegram e invia `/start`.

### Non ricevo notifiche
→ Lo scraper invia messaggi solo quando:
   - Un prodotto diventa disponibile (da SOLD OUT → AVAILABLE)
   - Un prodotto si esaurisce (da AVAILABLE → SOLD OUT)
   
   Se sono tutti SOLD OUT e rimangono tali, non ricevi messaggi (per evitare spam).

---

## 📞 Bisogno di aiuto?

Dimmi dove ti sei bloccato e ti aiuto! 🚀
