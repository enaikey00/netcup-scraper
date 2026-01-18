# 🤖 Comandi Bot Telegram - Guida Rapida

Il bot ora supporta comandi interattivi! Puoi richiedere controlli manuali quando vuoi.

## 📱 Comandi Disponibili

### `/check`
Richiede un controllo immediato della disponibilità VPS.

**Esempio:**
```
Tu: /check

Bot: 🔍 Controllo disponibilità in corso...
     Riceverai i risultati tra pochi secondi.

[dopo ~30 secondi]

Bot: 🔍 Netcup VPS ARM Check (richiesto manualmente)
     📅 2026-01-18 15:30:00 UTC
     
     ❌ VPS 1000 ARM G11: SOLD OUT
     ❌ VPS 2000 ARM G11: SOLD OUT
     ❌ VPS 3000 ARM G11: SOLD OUT
```

### `/help`
Mostra la lista dei comandi disponibili.

### `/status`
Mostra lo stato del bot e dell'ultimo controllo.

---

## ⚙️ Come Funziona

### 🕐 Polling ogni 5 minuti
- GitHub Actions controlla ogni 5 minuti se hai inviato comandi
- Se trova `/check`, esegue immediatamente il controllo VPS
- Ti risponde su Telegram con i risultati

### ⏰ Monitoraggio automatico continua
- Il controllo orario automatico continua normalmente
- I comandi manuali sono in aggiunta, non sostituiscono il monitoraggio

---

## 🧪 Test in Locale

Puoi testare i comandi prima di fare il push:

```bash
# Test interattivo
python test_commands_local.py

# Segui le istruzioni:
# 1. Invia /check al bot su Telegram
# 2. Premi INVIO nello script
# 3. Lo script controllerà e eseguirà il check
```

---

## 🚀 Deploy su GitHub

### 1. Fai commit e push dei nuovi file:

```bash
git add .
git commit -m "Add Telegram commands support (/check, /help, /status)"
git push
```

### 2. Verifica che il workflow sia attivo:

1. Vai su **Actions** nel tuo repository
2. Dovresti vedere un nuovo workflow: **"Check Telegram Commands"**
3. Questo partirà automaticamente ogni 5 minuti

### 3. Test del comando:

1. Invia `/check` al tuo bot su Telegram
2. Aspetta massimo 5 minuti (il tempo del prossimo polling)
3. Riceverai prima: "🔍 Controllo disponibilità in corso..."
4. Poi riceverai i risultati del check!

---

## ⚡ Test Immediato (senza aspettare 5 minuti)

Puoi forzare il check manualmente:

1. Vai su **Actions** → **Check Telegram Commands**
2. Click **Run workflow** → **Run workflow**
3. In ~30 secondi il bot controllerà i comandi e risponderà

---

## 📊 Differenze tra Check Automatico e Manuale

### Check Automatico (ogni ora)
- ⏰ Parte automaticamente ogni ora
- 🔕 Notifica SOLO se cambia qualcosa o c'è disponibilità
- 📝 Log salvato come artifact normale

### Check Manuale (comando /check)
- 👆 Parte quando invii `/check`
- 📱 Notifica SEMPRE (anche se tutto è sold out)
- ⚡ Risposta in max 5 minuti
- 📝 Log salvato come artifact separato

---

## 🐛 Troubleshooting

### Il bot non risponde al comando /check

**Controlla:**
1. Hai aspettato almeno 5 minuti dopo l'invio del comando?
2. Il workflow "Check Telegram Commands" è abilitato in Actions?
3. I secrets sono configurati correttamente?

**Soluzione rapida:**
- Vai su Actions → Check Telegram Commands → Run workflow
- Questo forza un check immediato

### Il bot dice "comando non riconosciuto"

Assicurati di:
- Scrivere il comando esattamente: `/check` (con lo slash)
- Non aggiungere spazi o altro testo
- Usare minuscole

### Ricevo notifiche duplicate

È normale se:
- Invii `/check` vicino all'orario del check automatico
- In questo caso riceverai sia la notifica manuale che quella automatica

---

## 💡 Tips & Tricks

### Quando usare /check?
- 📢 Quando senti parlare di un restock imminente
- 🌙 Prima di andare a dormire (per un check rapido)
- ☕ Durante la giornata se sei ansioso di controllare

### I comandi sono privati?
- ✅ Sì! Solo tu (il tuo Chat ID) puoi inviare comandi
- Il bot ignora messaggi da altri utenti

### Posso cambiare la frequenza del polling?
Sì! Modifica `.github/workflows/check-commands.yml`:

```yaml
schedule:
  - cron: '*/5 * * * *'  # Ogni 5 minuti (attuale)
  # - cron: '*/10 * * * *'  # Ogni 10 minuti
  # - cron: '*/3 * * * *'  # Ogni 3 minuti (più frequente)
```

⚠️ **Attenzione**: Frequenze < 5 minuti potrebbero esaurire i minuti gratuiti di GitHub Actions.

---

## 📈 Monitoraggio

### Vedere i log dei comandi

1. Actions → Check Telegram Commands
2. Click sull'ultima esecuzione
3. Espandi "Check for commands" per vedere i comandi processati

### Scaricare lo storico

Gli artifact dei check manuali sono salvati separatamente:
- Nome: `availability-log-manual-XXX`
- Retention: 30 giorni

---

## 🎯 Prossimi Step (Opzionali)

Vuoi aggiungere altre funzionalità? Possiamo implementare:

- 🔔 `/subscribe <prodotto>` - Notifiche solo per VPS specifici
- 📊 `/stats` - Statistiche sulla disponibilità storica
- ⏰ `/schedule <orario>` - Controlli a orari specifici
- 🎨 Messaggi con grafici e trend

Fammi sapere se ti interessa! 🚀
