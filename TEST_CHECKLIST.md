# Test Checklist

Segui questi passi per testare lo scraper:

## Test 1: Versione Leggera

```bash
cd /Users/miniops/Desktop/Universe/netcup-scraper
pip3 install -r requirements_light.txt
python3 scraper_light.py
```

Scegli opzione **1** (controllo singolo)

### Risultati attesi:
- ✅ **Se funziona**: Vedrai status "AVAILABLE" o "SOLD OUT" per i prodotti
- ❌ **Se NON funziona**: Vedrai status "UNKNOWN" → passa al Test 2

## Test 2: Versione Selenium (se Test 1 fallisce)

```bash
pip3 install -r requirements_selenium.txt
python3 scraper_selenium.py
```

Scegli opzione **1** (controllo singolo)

### Risultati attesi:
- Dovresti vedere lo status corretto per ogni prodotto

## Test 3: Verifica Log

```bash
cat availability_log.json
```

Dovresti vedere un file JSON con i risultati del controllo.

## Test 4: Monitoraggio Continuo

Una volta che hai trovato la versione che funziona, testala in modalità continua:

```bash
# Con la versione che funziona
python3 scraper_light.py    # oppure scraper_selenium.py
```

Scegli opzione **2** (monitoraggio continuo)

Lascialo girare per 5-10 minuti per verificare che funzioni correttamente, poi fermalo con `Ctrl+C`.

## Cosa comunicarmi dopo i test

Mandami un messaggio con:
1. Quale versione funziona (light o selenium)?
2. Gli status che hai visto (AVAILABLE, SOLD OUT, o UNKNOWN)
3. Eventuali errori nel log

Così posso ottimizzare il codice in base ai risultati reali! 🚀
