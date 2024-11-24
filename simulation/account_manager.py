import json

# Durum dosyasının adı
STATUS_FILE = "account_status.json"

def save_account_status(balance, position=None, entry_price=None):
    """
    Mevcut durumu JSON dosyasına kaydet.
    """
    status = {
        "balance": balance,
        "position": position,
        "entry_price": entry_price
    }
    with open(STATUS_FILE, "w") as file:
        json.dump(status, file, indent=4)

def load_account_status():
    """
    JSON dosyasından durumu yükle.
    Eğer dosya yoksa varsayılan durum döndür.
    """
    try:
        with open(STATUS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Dosya yoksa varsayılan değerler döndür
        return {"balance": 100, "position": None, "entry_price": None}
