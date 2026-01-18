#!/usr/bin/env python3
"""
Netcup VPS ARM Availability Scraper - Approccio Leggero (HTTP + BeautifulSoup)
Controlla la disponibilità dei VPS ARM usando semplici richieste HTTP
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import logging
import sys

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class NetcupScraperLight:
    def __init__(self, config_file='config.json'):
        """Inizializza lo scraper con la configurazione"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.log_file = self.config['log_file']
        self.products = self.config['products']
        self.check_interval = self.config['check_interval_minutes'] * 60
        
        # Headers per sembrare un browser normale
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        # Inizializza il file di log se non esiste
        self._init_log_file()
    
    def _init_log_file(self):
        """Inizializza il file di log JSON"""
        try:
            with open(self.log_file, 'r') as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.log_file, 'w') as f:
                json.dump([], f, indent=2)
    
    def check_availability(self, product):
        """Controlla la disponibilità di un singolo prodotto"""
        try:
            logger.info(f"Controllando {product['name']}...")
            
            response = requests.get(product['url'], headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Cerca il pulsante di acquisto
            # Possibili selettori da testare:
            # 1. Cerca il testo "product is sold out" o "add to shopping cart"
            # 2. Cerca button con classe o attributo specifico
            
            # Strategia 1: Cerca il testo direttamente
            page_text = soup.get_text().lower()
            
            if 'sold out' in page_text or 'product is sold out' in page_text:
                available = False
                status = "SOLD OUT"
            elif 'add to shopping cart' in page_text or 'order now' in page_text:
                available = True
                status = "AVAILABLE"
            else:
                available = None
                status = "UNKNOWN"
            
            # Strategia 2: Cerca button specifici
            buttons = soup.find_all('button')
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
            
            logger.info(f"  → {product['name']}: {status}")
            return {
                'name': product['name'],
                'url': product['url'],
                'available': available,
                'status': status,
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.RequestException as e:
            logger.error(f"Errore durante il controllo di {product['name']}: {e}")
            return {
                'name': product['name'],
                'url': product['url'],
                'available': None,
                'status': "ERROR",
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def save_results(self, results):
        """Salva i risultati nel file di log"""
        try:
            # Leggi i dati esistenti
            with open(self.log_file, 'r') as f:
                log_data = json.load(f)
            
            # Aggiungi i nuovi risultati
            log_entry = {
                'check_time': datetime.now().isoformat(),
                'results': results
            }
            log_data.append(log_entry)
            
            # Salva tutto
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
            
            logger.info(f"Risultati salvati in {self.log_file}")
            
        except Exception as e:
            logger.error(f"Errore nel salvare i risultati: {e}")
    
    def run_check(self):
        """Esegue un singolo ciclo di controllo per tutti i prodotti"""
        logger.info("=" * 60)
        logger.info(f"Inizio controllo disponibilità - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        results = []
        for product in self.products:
            result = self.check_availability(product)
            results.append(result)
            time.sleep(2)  # Pausa tra le richieste per non sovraccaricare il server
        
        self.save_results(results)
        
        # Mostra riepilogo
        logger.info("\n" + "=" * 60)
        logger.info("RIEPILOGO:")
        for result in results:
            status_emoji = "✅" if result['available'] else "❌" if result['available'] is False else "❓"
            logger.info(f"  {status_emoji} {result['name']}: {result['status']}")
        logger.info("=" * 60 + "\n")
        
        return results
    
    def run_continuous(self):
        """Esegue controlli continui ogni intervallo specificato"""
        logger.info(f"Avvio monitoraggio continuo (controllo ogni {self.config['check_interval_minutes']} minuti)")
        logger.info("Premi Ctrl+C per fermare\n")
        
        try:
            while True:
                self.run_check()
                logger.info(f"Prossimo controllo tra {self.config['check_interval_minutes']} minuti...\n")
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            logger.info("\nMonitoraggio interrotto dall'utente")


def main():
    """Funzione principale"""
    scraper = NetcupScraperLight()
    
    # Chiedi all'utente cosa vuole fare
    print("\nNetcup VPS ARM Availability Scraper (Light)")
    print("=" * 50)
    print("1. Controllo singolo")
    print("2. Monitoraggio continuo (ogni ora)")
    print("=" * 50)
    
    choice = input("\nScegli un'opzione (1 o 2): ").strip()
    
    if choice == "1":
        scraper.run_check()
    elif choice == "2":
        scraper.run_continuous()
    else:
        print("Opzione non valida. Eseguo un controllo singolo.")
        scraper.run_check()


if __name__ == "__main__":
    main()
