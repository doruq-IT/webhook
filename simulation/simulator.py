from config.settings import LEVERAGE, COMMISSION_RATE

class Simulator:
    def __init__(self, starting_balance):
        self.balance = starting_balance  # Mevcut bakiye
        self.current_position = None  # Long veya Short
        self.entry_price = None  # İşlem açılış fiyatı

    def close_position(self, exit_price):
        """
        Mevcut pozisyonu kapat ve kar/zararı hesapla.
        """
        if self.current_position is None:
            return 0  # Açık işlem yoksa kar/zarar sıfırdır

        # Kar/zarar hesaplama
        if self.current_position == "long":
            profit = (exit_price - self.entry_price) * (self.balance * LEVERAGE) / self.entry_price
        elif self.current_position == "short":
            profit = (self.entry_price - exit_price) * (self.balance * LEVERAGE) / self.entry_price

        # Komisyon hesaplama (pozisyon açma ve kapatma)
        total_commission = 2 * (self.balance * LEVERAGE) * COMMISSION_RATE

        # Kar/zarar komisyonu düşerek güncelle
        profit -= total_commission

        # Kar/zararı bakiyeye ekle
        self.balance += profit

        # Pozisyonu sıfırla
        self.current_position = None
        self.entry_price = None

        return profit

    def open_position(self, position_type, entry_price):
        """
        Yeni bir pozisyon aç.
        """
        # Pozisyon açma komisyonu
        opening_commission = (self.balance * LEVERAGE) * COMMISSION_RATE

        # Pozisyonu başlatırken komisyonu düş
        self.balance -= opening_commission
        self.current_position = position_type
        self.entry_price = entry_price
