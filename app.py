import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# تفعيل الـ CORS للسماح لـ Netlify بالاتصال بالسيرفر دون قيود
CORS(app, resources={r"/api/*": {"origins": "*"}})

# الهدف الافتراضي (يمكنك تعديله أو تمريره عبر متغيرات البيئة)
TARGET_URL = os.environ.get("TARGET_API_URL", "https://api.example.com/api/chat")

# قائمة البروكسيات العامة (HTTP / SOCKS5)
# تأكد من تحديث هذه القائمة ببروكسيات نشطة وصالحة للعمل
PROXIES_LIST = [
    "http://username:password@proxy_ip1:port",
    "http://username:password@proxy_ip2:port",
    "socks5://username:password@proxy_ip3:port",
    # يمكنك إضافة بروكسيات مجانية أو مدفوعة هنا
]

# قائمة بمتصفحات مختلفة لتزييف البصمة بشكل عشوائي
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
]

@app.route('/api/chat', methods=['POST'])
def proxy_chat():
    try:
        # 1. الحصول على البيانات القادمة من Netlify
        data = request.get_json() or {}

        # 2. تزييف الرأسيات (Headers Spoofing)
        spoofed_headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://example.com",
            "Referer": "https://example.com/",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site"
        }

        # 3. اختيار بروكسي عشوائي إذا كانت القائمة ممتلئة
        req_proxies = None
        if PROXIES_LIST:
            selected_proxy = random.choice(PROXIES_LIST)
            req_proxies = {
                "http": selected_proxy,
                "https": selected_proxy
            }

        # 4. إرسال الطلب إلى الهدف
        response = requests.post(
            TARGET_URL,
            json=data,
            headers=spoofed_headers,
            proxies=req_proxies,
            timeout=15  # مهلة زمنية لتفادي تعليق السيرفر عند ضعف البروكسي
        )

        # 5. إرجاع الاستجابة إلى Netlify
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Proxy request failed: {e}")
        return jsonify({"error": "Failed to connect to the target API", "details": str(e)}), 502
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    # الاستماع على المنفذ المخصص من Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
