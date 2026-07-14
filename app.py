@app.route('/api/chat', methods=['POST'])
def proxy_chat():
    try:
        data = request.get_json() or {}

        spoofed_headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://chat.dphn.ai",
            "Referer": "https://chat.dphn.ai/"
        }

        req_proxies = None
        if PROXIES_LIST:
            selected_proxy = random.choice(PROXIES_LIST)
            req_proxies = {"http": selected_proxy, "https": selected_proxy}

        # إرسال الطلب
        response = requests.post(
            TARGET_URL,
            json=data,
            headers=spoofed_headers,
            proxies=req_proxies,
            timeout=30  # زيادة المهلة لضمان استقرار البروكسي
        )

        # لمنع انكسار الشات: نتحقق إذا كانت الاستجابة JSON فعلاً، وإلا نرسلها كنص عادي
        try:
            response_data = response.json()
            return jsonify(response_data), response.status_code
        except ValueError:
            # إذا أرجع الموقع نصاً عادياً أو خطأ غير منسق
            return response.text, response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Proxy request failed: {e}")
        return jsonify({"error": "Render Proxy Timeout/Fetch Failed", "details": str(e)}), 502
