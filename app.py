import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# 1. تعريف التطبيق وتفعيل الـ CORS أولاً وقبل أي شيء!
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# الهدف الافتراضي المصحح بناءً على تحليل kk.py
TARGET_URL = os.environ.get("TARGET_API_URL", "https://chat.dphn.ai/api/chat")[span_10](start_span)[span_10](end_span)

# قائمة البروكسيات العامة
PROXIES_LIST = []

# متصفح الهاتف الذي نجح في kk.py لتفادي الحظر
SPOOFED_USER_AGENT = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36[span_11](start_span)"[span_11](end_span)

@app.route('/api/chat', methods=['POST'])
def proxy_chat():
    try:
        data = request.get_json() or {}
        messages = data.get("messages", [])

        # ─── معالجة ودمج رسائل الـ system لتجنب خطأ E4 ───[span_12](start_span)[span_12](end_span)
        dphn_messages = []
        pending_system = []
        for m in messages:
            if m.get("role") == "system":
                pending_system.append(m.get("content", ""))[span_13](start_span)[span_13](end_span)
                continue
            if pending_system and m.get("role") == "user":
                merged_content = (
                    "[تعليمات ثابتة يجب اتباعها]:\n"
                    + "\n\n".join(pending_system)
                    + "\n\n[رسالة المستخدم]:\n"
                    + m.get("content", "")
                )[span_14](start_span)[span_14](end_span)
                dphn_messages.append({"role": "user", "content": merged_content})[span_15](start_span)[span_15](end_span)
                pending_system = []
            else:
                dphn_messages.append(m)[span_16](start_span)[span_16](end_span)
                
        if pending_system:
            dphn_messages.append({"role": "user", "content": "\n\n".join(pending_system)})[span_17](start_span)[span_17](end_span)

        # تحديث مصفوفة البيانات بالرسائل المهيكلة الجديدة
        data["messages"] = dphn_messages

        # تزييف البصمة بالكامل بناءً على الرأسيات التي نجحت في kk.py[span_18](start_span)[span_18](end_span)
        spoofed_headers = {
            "User-Agent": SPOOFED_USER_AGENT,[span_19](start_span)[span_19](end_span)
            "Accept": "application/json, text/plain, */*",[span_20](start_span)[span_20](end_span)
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",[span_21](start_span)[span_21](end_span)
            "Origin": "https://dphn.ai",[span_22](start_span)[span_22](end_span)
            "Referer": "https://dphn.ai/[span_23](start_span)"[span_23](end_span)
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
