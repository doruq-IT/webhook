from flask import Flask, request

app = Flask(__name__)

# Webhook endpoint'i
@app.route('/webhook', methods=['POST'])
def webhook():
    # Content-Type başlığını kontrol edin
    content_type = request.headers.get('Content-Type')
    if content_type in ['application/json', 'text/plain']:
        try:
            # JSON formatındaki veriyi al
            data = request.json
        except Exception as e:
            # Eğer JSON formatında değilse hata döndür
            return f"Gönderilen veri JSON formatında değil! Hata: {str(e)}", 400

        # JSON verisinden bilgileri al
        ticker = data.get('ticker')
        price = data.get('price')
        action = data.get('action')

        # Gelen sinyale göre işlem yap
        if action == "buy":
            print(f"{ticker} için BUY sinyali alındı. Fiyat: {price}")
        elif action == "sell":
            print(f"{ticker} için SELL sinyali alındı. Fiyat: {price}")
        elif action == "test":
            print(f"{ticker} için TEST sinyali alındı. Fiyat: {price}")
        else:
            print(f"Bilinmeyen işlem tipi: {action}")
        
        # İşlem tamamlandığında başarılı yanıt döndür
        return "Webhook başarıyla işlendi!", 200
    else:
        # Eğer desteklenmeyen bir Content-Type başlığı geldiyse hata döndür
        return "Unsupported content type! Lütfen JSON formatında veri gönderin.", 400

# Ana dizin endpoint'i (tarayıcıdan kontrol için)
@app.route('/', methods=['GET'])
def index():
    return "Flask uygulaması çalışıyor! Webhook endpoint'i '/webhook' adresindedir.", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Port 80'de çalıştır
