import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# 1. تعريف التطبيق وتفعيل الـ CORS أولاً وقبل أي شيء!
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# الهدف الافتراضي (API الداخلي لموقع dphn)
TARGET_URL = os.environ.get("TARGET_API_URL", "https://chat.dphn.ai/api/chat")

# قائمة البروكسيات العامة (تأكد من إضافتها أو تركها فارغة مؤقتاً لتجربة الاتصال)
PROXIES_LIST = []

# قائمة بمتصفحات مختلفة لتزييف البصمة
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

@app.route('/api/chat', methods=['POST'])
def proxy_chat():
    try:
        data = request.get_json() or {}

        # تزييف البصمة بالكامل
        spoofed_headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://chat.dphn.ai",
            "Referer": "https://chat.dphn.ai/"
        }

        # اختيار بروكسي عشوائي في حال وجود بروكسيات بالقائمة
        req_proxies = None
        if PROXIES_LIST:
            selected_proxy = random.choice(PROXIES_LIST)
            req_proxies = {
                "http": selected_proxy,
                "https": selected_proxy
            }

        # توجيه الطلب إلى dphn
        response = requests.post(
            TARGET_URL,
            json=data,
            headers=spoofed_headers,
            proxies=req_proxies,
            timeout=30
        )

        # استرجاع الإجابة
        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            return response.text, response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Proxy connection failed: {e}")
        return jsonify({"error": "Failed to connect to target API", "details": str(e)}), 502
    except Exception as e:
        print(f"Internal Error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    except requests.exceptions.RequestException as e:
        print(f"Proxy request failed: {e}")
        return jsonify({"error": "Render Proxy Timeout/Fetch Failed", "details": str(e)}), 502
    except requests.exceptions.RequestException as e:
        print(f"Proxy request failed: {e}")
        return jsonify({"error": "Render Proxy Timeout/Fetch Failed", "details": str(e)}), 502
