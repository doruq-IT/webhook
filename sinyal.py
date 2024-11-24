from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

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
        price = data.get('price')
        action = data.get('action')
        timestamp = data.get('timestamp')  # ISO 8601 formatında zaman

        # Zaman etiketini işleme
        if timestamp:
            try:
                # ISO 8601 formatındaki zamanı insan okunabilir hale getir
                human_readable_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                human_readable_time = f"Zaman bilgisini dönüştürürken hata oluştu: {str(e)}"
        else:
            human_readable_time = "Zaman bilgisi mevcut değil"

        # Gelen sinyale göre işlem yap
        if action == "buy":
            print(f"{ticker} için BUY sinyali alındı. Fiyat: {price}. Zaman: {human_readable_time}")
        elif action == "sell":
            print(f"{ticker} için SELL sinyali alındı. Fiyat: {price}. Zaman: {human_readable_time}")
        elif action == "test":
            print(f"{ticker} için TEST sinyali alındı. Fiyat: {price}. Zaman: {human_readable_time}")
        else:
            print(f"Bilinmeyen işlem tipi: {action}. Zaman: {human_readable_time}")
        
        return "Webhook başarıyla işlendi!", 200
    else:
        return "Unsupported content type! Lütfen JSON formatında veri gönderin.", 400

@app.route('/', methods=['GET'])
def index():
    return "Flask uygulaması çalışıyor! Webhook endpoint'i '/webhook' adresindedir.", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
