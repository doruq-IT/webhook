import json

# İşlem geçmişini bellekte saklamak için bir liste
transactions = []

def log_transaction(transaction):
    """
    İşlem geçmişine yeni bir işlem ekle ve dosyaya kaydet.
    """
    transactions.append(transaction)
    # İşlem geçmişini JSON dosyasına yaz
    with open("transaction_log.json", "w") as log_file:
        json.dump(transactions, log_file, indent=4)

def get_transaction_log():
    """
    İşlem geçmişini getir. Eğer dosya mevcutsa, bellekteki listeyi güncelle.
    """
    global transactions
    try:
        # Daha önce kaydedilen işlem geçmişini dosyadan yükle
        with open("transaction_log.json", "r") as log_file:
            transactions = json.load(log_file)
    except FileNotFoundError:
        # Eğer dosya yoksa boş bir liste döndür
        transactions = []
    return transactions
