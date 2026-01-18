#!/bin/bash

echo "==================================================="
echo "Netcup Scraper - Setup Script"
echo "==================================================="
echo ""

# Controlla se Python è installato
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 non trovato. Installalo prima di continuare."
    exit 1
fi

echo "✅ Python3 trovato: $(python3 --version)"
echo ""

# Chiedi quale versione installare
echo "Quale versione vuoi installare?"
echo "1. Versione Leggera (HTTP + BeautifulSoup) - Consigliata per primo test"
echo "2. Versione Selenium (più pesante ma più affidabile)"
echo "3. Entrambe"
echo ""
read -p "Scegli (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "Installazione versione leggera..."
        pip3 install -r requirements_light.txt
        echo ""
        echo "✅ Installazione completata!"
        echo "Esegui: python3 scraper_light.py"
        ;;
    2)
        echo ""
        echo "Installazione versione Selenium..."
        pip3 install -r requirements_selenium.txt
        echo ""
        echo "✅ Installazione completata!"
        echo "Esegui: python3 scraper_selenium.py"
        ;;
    3)
        echo ""
        echo "Installazione di entrambe le versioni..."
        pip3 install -r requirements_light.txt
        pip3 install -r requirements_selenium.txt
        echo ""
        echo "✅ Installazione completata!"
        echo "Testa prima: python3 scraper_light.py"
        echo "Se non funziona: python3 scraper_selenium.py"
        ;;
    *)
        echo "❌ Opzione non valida"
        exit 1
        ;;
esac

echo ""
echo "==================================================="
echo "Setup completato! Buon monitoraggio! 🚀"
echo "==================================================="
