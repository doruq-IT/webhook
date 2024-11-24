# simulation/transaction_log.py

transactions = []  # İşlem geçmişini saklamak için bir liste

def log_transaction(transaction):
    """
    İşlem geçmişine yeni bir işlem ekle.
    """
    transactions.append(transaction)

def get_transaction_log():
    """
    İşlem geçmişini getir.
    """
    return transactions
