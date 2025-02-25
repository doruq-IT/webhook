from flask import Flask, request
from datetime import datetime
import pytz
from simulation.simulator import Simulator
from simulation.transaction_log import log_transaction
from simulation.account_manager import save_account_status, load_account_status
from config.settings import STARTING_BALANCE

app = Flask(__name__)

# Durumu yükle
account_status = load_account_status()
simulator = Simulator(account_status["balance"])

# Eğer açık bir pozisyon varsa yükle
if account_status["position"]:
    simulator.current_position = account_status["position"]
    simulator.entry_price = account_status["entry_price"]

@app.route('/webhook', methods=['POST'])
def webhook():
    content_type = request.headers.get('Content-Type', '').lower()
    if 'application/json' in content_type:
        try:
            data = request.json
        except Exception as e:
            return f"Gönderilen veri JSON formatında değil! Hata: {str(e)}", 400

        # JSON verisinden bilgileri al
        ticker = data.get('ticker')
        price = float(data.get('price'))
        action = data.get('action')
        timestamp = data.get('timestamp')  # ISO 8601 formatında zaman

        # Zaman etiketini işleme
        if timestamp:
            try:
                utc_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                local_timezone = pytz.timezone("Europe/Istanbul")
                local_time = utc_time.astimezone(local_timezone)
                human_readable_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                human_readable_time = f"Zaman bilgisini dönüştürürken hata oluştu: {str(e)}"
        else:
            human_readable_time = "Zaman bilgisi mevcut değil"

        # Mevcut pozisyonu kapat ve kar/zarar hesapla
        if simulator.current_position:
            profit = simulator.close_position(price)
            log_transaction({
                "type": "close",
                "profit": profit,
                "exit_price": price,
                "time": human_readable_time
            })
            print(f"Pozisyon kapatıldı. Kar/Zarar: {profit}. Zaman: {human_readable_time}")

        # Yeni pozisyon aç
        simulator.open_position("long" if action == "buy" else "short", price)
        log_transaction({
            "type": action,
            "entry_price": price,
            "balance": simulator.balance,
            "time": human_readable_time
        })
        print(f"{ticker} için {'LONG' if action == 'buy' else 'SHORT'} pozisyon açıldı. Fiyat: {price}. Zaman: {human_readable_time}")

        # Güncel durumu kaydet
        save_account_status(simulator.balance, simulator.current_position, simulator.entry_price)

        return {"balance": simulator.balance}, 200
    else:
        return "Unsupported content type! Lütfen JSON formatında veri gönderin.", 400

@app.route('/log', methods=['GET'])
def get_log():
    from simulation.transaction_log import get_transaction_log
    return {"transactions": get_transaction_log()}, 200

@app.route('/', methods=['GET'])
def index():
    return "Flask uygulaması çalışıyor! Webhook endpoint'i '/webhook' adresindedir.", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
