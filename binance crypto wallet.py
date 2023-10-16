import requests
import hashlib
import hmac
import time
from decimal import Decimal
import threading

# Remplacez ces valeurs par vos propres clés d'API Binance
API_KEY = 'apikey'
SECRET_KEY = 'secretkey'
crypto = "PEPE"
# URL de l'API Binance
BASE_URL = 'https://api.binance.com/api/v3'

# Fonction pour générer une signature cryptographique pour les requêtes API
def generate_signature(data):
    signature = hmac.new(
        bytes(SECRET_KEY, 'utf-8'),
        bytes(data, 'utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature

# Fonction pour récupérer le prix actuel d'une crypto-monnaie
def get_price(crypto):
    url = f'{BASE_URL}/ticker/price'
    params = {'symbol': f'{crypto}USDT'}

    try:
        with requests.get(url, params=params) as response:
            response.raise_for_status()
            price = float(response.json()['price'])
            return price
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print(f"Erreur lors de la récupération du prix : {e}")
        return None

# Fonction pour récupérer le solde d'une crypto-monnaie dans votre compte Binance
def get_balance(crypto):
    timestamp = int(time.time() * 1000)
    data = f'timestamp={timestamp}'
    signature = generate_signature(data)
    account_info_url = f'{BASE_URL}/account'
    params = {'timestamp': timestamp, 'signature': signature}
    headers = {'X-MBX-APIKEY': API_KEY}

    try:
        with requests.get(account_info_url, params=params, headers=headers) as response:
            response.raise_for_status()
            account_data = response.json()
            balances = {asset['asset']: float(asset['free']) for asset in account_data.get('balances', [])}
            balance = balances.get(crypto, None)
            if balance is not None:
                return balance
            else:
                print(f'Aucun solde {crypto} trouvé dans le compte.')
                return None
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print(f"Erreur lors de la récupération des données du compte : {e}")
        return None

# Fonction pour récupérer et afficher le solde et la valeur d'une crypto-monnaie
def fetch_price_and_balance():
    balance = get_balance(crypto)
    if balance is not None:
        price = get_price(crypto)
        if price is not None:
            value = balance * price
            print(f'Votre solde est de {value:.4f} USDT, Prix du {symbol} : {price} USDT')
        else:
            print("Aucun prix disponible")
    else:
        print("Aucun fonds disponibles")

# Fonction principale pour récupérer en continu et afficher le solde et la valeur de la crypto-monnaie
def main():
    while True:
        threading.Thread(target=fetch_price_and_balance).start()
        time.sleep(1)

if __name__ == "__main__":
    symbol = input("Quelle crypto-monnaie souhaitez-vous voir ? ")
    main()