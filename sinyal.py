from flask import Flask, request

app = Flask(__name__)

# Ana dizin (tarayıcıdan erişim için)
@app.route('/', methods=['GET'])
def index():
    return "Flask uygulaması çalışıyor! Webhook endpoint'i '/webhook' adresindedir.", 200

# Webhook sinyallerini işleyen fonksiyon
def process_signal(action, ticker, price):
    if action == "sell":
        return f"{ticker} için SELL sinyali alındı. Fiyat: {price}"
    elif action == "buy":
        return f"{ticker} için BUY sinyali alındı. Fiyat: {price}"
    else:
        return f"Bilinmeyen işlem tipi: {action}"

# Webhook endpoint'i
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('Content-Type') == 'application/json':
        data = request.json  # JSON formatındaki veriyi al
        # Eksik veya hatalı veri kontrolü
        if not all([data.get('ticker'), data.get('price'), data.get('action')]):
            return "Eksik veya hatalı veri alındı!", 400

        # Veriyi işleyin
        ticker = data.get('ticker')
        price = data.get('price')
        action = data.get('action')
        message = process_signal(action, ticker, price)

        # Terminale yazdır ve log dosyasına kaydet
        print("Webhook POST verisi alındı:")
        print(message)
        with open("webhook_logs.txt", "a") as log_file:
            log_file.write(message + "\n")

        return "Webhook POST isteği başarıyla alındı!", 200
    else:
        return "Unsupported content type! Lütfen JSON formatında veri gönderin.", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Port 80'de çalıştır
