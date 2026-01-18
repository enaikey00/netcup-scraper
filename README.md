# Netcup VPS ARM Availability Scraper

Scraper per controllare automaticamente la disponibilità dei VPS ARM su netcup.com.

## Prodotti monitorati
- VPS 1000 ARM G11
- VPS 2000 ARM G11
- VPS 3000 ARM G11

## Installazione

### Approccio 1: Versione Leggera (HTTP + BeautifulSoup)
Più veloce e meno pesante, ma potrebbe non funzionare se il contenuto è caricato dinamicamente con JavaScript.

```bash
pip install -r requirements_light.txt
```

### Approccio 2: Versione Selenium
Più pesante ma garantisce il funzionamento anche con contenuti JavaScript dinamici.

```bash
pip install -r requirements_selenium.txt
```

## Utilizzo

### Test Versione Leggera
```bash
python scraper_light.py
```

### Test Versione Selenium
```bash
python scraper_selenium.py
```

Entrambi gli script offrono due modalità:
1. **Controllo singolo**: Esegue un solo controllo e termina
2. **Monitoraggio continuo**: Controlla ogni ora automaticamente

## Configurazione

Modifica `config.json` per personalizzare:
- URL dei prodotti da monitorare
- Intervallo di controllo (in minuti)
- Nome del file di log

```json
{
  "check_interval_minutes": 60,
  "log_file": "availability_log.json"
}
```

## Output

### Log sul terminale
Lo scraper mostra i risultati in tempo reale con emoji:
- ✅ Prodotto disponibile
- ❌ Prodotto esaurito
- ❓ Stato sconosciuto

### File di log
I risultati vengono salvati in:
- `availability_log.json` - Storico completo di tutte le verifiche
- `scraper.log` - Log dettagliato delle operazioni

## Struttura File

```
netcup-scraper/
├── config.json                    # Configurazione
├── scraper_light.py               # Versione leggera (HTTP)
├── scraper_selenium.py            # Versione Selenium
├── requirements_light.txt         # Dipendenze versione leggera
├── requirements_selenium.txt      # Dipendenze Selenium
├── availability_log.json          # Log disponibilità (auto-generato)
└── scraper.log                    # Log operazioni (auto-generato)
```

## Testing

### Passo 1: Testa la versione leggera
```bash
python scraper_light.py
# Scegli opzione 1 per un test rapido
```

Se vedi status "UNKNOWN" per tutti i prodotti, significa che il contenuto è caricato con JavaScript e devi usare Selenium.

### Passo 2: Se necessario, testa Selenium
```bash
python scraper_selenium.py
# Scegli opzione 1 per un test rapido
```

### Passo 3: Verifica i risultati
Controlla `availability_log.json` per vedere lo storico delle verifiche.

## Note
- Lo scraper fa pause di 2 secondi tra le richieste per non sovraccaricare il server
- Usa User-Agent realistici per sembrare un browser normale
- I log vengono salvati sia su file che stampati sul terminale
