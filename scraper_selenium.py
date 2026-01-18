#!/usr/bin/env python3
"""
Netcup VPS ARM Availability Scraper - Approccio Selenium
Controlla la disponibilità dei VPS ARM usando Selenium per gestire JavaScript
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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


class NetcupScraperSelenium:
    def __init__(self, config_file='config.json', headless=True):
        """Inizializza lo scraper con Selenium"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.log_file = self.config['log_file']
        self.products = self.config['products']
        self.check_interval = self.config['check_interval_minutes'] * 60
        self.headless = headless
        
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
    
    def _create_driver(self):
        """Crea un'istanza del WebDriver"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver
    
    def check_availability(self, product, driver):
        """Controlla la disponibilità di un singolo prodotto"""
        try:
            logger.info(f"Controllando {product['name']}...")
            
            driver.get(product['url'])
            
            # Aspetta che la pagina si carichi
            time.sleep(3)
            
            # Strategia 1: Cerca il testo "sold out" o "add to shopping cart"
            page_source = driver.page_source.lower()
            
            available = None
            status = "UNKNOWN"
            
            if 'sold out' in page_source or 'product is sold out' in page_source:
                available = False
                status = "SOLD OUT"
            elif 'add to shopping cart' in page_source or 'add to cart' in page_source:
                available = True
                status = "AVAILABLE"
            
            # Strategia 2: Cerca button specifici tramite XPath/CSS
            try:
                # Cerca button con testo "sold out"
                sold_out_buttons = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sold out')]")
                if sold_out_buttons:
                    available = False
                    status = "SOLD OUT"
                
                # Cerca button con testo "add to cart" o "order"
                cart_buttons = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cart')]")
                if cart_buttons and available is None:
                    available = True
                    status = "AVAILABLE"
            except Exception as e:
                logger.warning(f"Errore nella ricerca dei button: {e}")
            
            # Strategia 3: Controlla la proprietà cursor dei button
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for button in buttons:
                    cursor = button.value_of_css_property('cursor')
                    button_text = button.text.lower()
                    
                    if cursor == 'not-allowed' or 'sold out' in button_text:
                        available = False
                        status = "SOLD OUT"
                        break
                    elif (cursor == 'pointer' or cursor == 'default') and ('cart' in button_text or 'order' in button_text):
                        available = True
                        status = "AVAILABLE"
            except Exception as e:
                logger.warning(f"Errore nel controllo cursor: {e}")
            
            logger.info(f"  → {product['name']}: {status}")
            
            return {
                'name': product['name'],
                'url': product['url'],
                'available': available,
                'status': status,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
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
        
        driver = None
        try:
            driver = self._create_driver()
            results = []
            
            for product in self.products:
                result = self.check_availability(product, driver)
                results.append(result)
                time.sleep(2)  # Pausa tra le richieste
            
            self.save_results(results)
            
            # Mostra riepilogo
            logger.info("\n" + "=" * 60)
            logger.info("RIEPILOGO:")
            for result in results:
                status_emoji = "✅" if result['available'] else "❌" if result['available'] is False else "❓"
                logger.info(f"  {status_emoji} {result['name']}: {result['status']}")
            logger.info("=" * 60 + "\n")
            
            return results
            
        finally:
            if driver:
                driver.quit()
    
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
    scraper = NetcupScraperSelenium(headless=True)
    
    # Chiedi all'utente cosa vuole fare
    print("\nNetcup VPS ARM Availability Scraper (Selenium)")
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
