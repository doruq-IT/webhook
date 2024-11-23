from flask import Flask, request

app = Flask(__name__)

# Ana dizin (tarayıcıdan erişim için)
@app.route('/', methods=['GET'])
def index():
    return "Flask uygulaması çalışıyor! Webhook endpoint'i '/webhook' adresindedir.", 200

# Webhook endpoint'i
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('Content-Type') == 'application/json':
        data = request.json  # JSON formatındaki veriyi al
        # Gelen veriyi terminalde yazdır
        print("Webhook POST verisi alındı:")
        print(f"Ticker: {data.get('ticker')}")
        print(f"Price: {data.get('price')}")
        print(f"Action: {data.get('action')}")

        # İşlem mantığını burada ekleyebilirsiniz
        action = data.get("action")
        ticker = data.get("ticker")
        price = data.get("price")

        if action == "sell":
            print(f"{ticker} için SELL sinyali alındı. Fiyat: {price}")
        elif action == "buy":
            print(f"{ticker} için BUY sinyali alındı. Fiyat: {price}")
        else:
            print(f"Bilinmeyen işlem tipi: {action}")
    else:
        return "Unsupported content type! Lütfen JSON formatında veri gönderin.", 400

    return "Webhook POST isteği başarıyla alındı!", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Port 80'de çalıştır
