import os
import webbrowser
from threading import Timer
from flask import Flask, request, render_template_string, redirect, url_for, flash, get_flashed_messages
from sentence_transformers import SentenceTransformer, util
import requests

app = Flask(__name__)
app.secret_key = "change_this_secret_key"
# برای flash/session الزامی است

# ==== مدل تبدیل متن به بردار ====
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

# ==== دانشنامه داخلی (FAQ) ====
faq = {
    "ساعات کاری": "شرکت ما شنبه تا چهارشنبه از ساعت ۸ صبح تا ۵ عصر فعال است.",
    "آدرس شرکت": "تهران، خیابان ولیعصر، کوچه فلان، پلاک ۱۰",
    "محصولات": "ما محصولات A، B و C را ارائه می‌دهیم.",
    "پشتیبانی": "برای پشتیبانی با شماره ********021 تماس بگیرید."
}

# تبدیل سوالات FAQ به بردار
faq_embeddings = {q: model.encode(q, convert_to_tensor=True) for q in faq.keys()}

# ==== تنظیمات Gemini API ====
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# باید قبلاً با setx تنظیم کرده باشی
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def ask_gemini(question: str):
    if not GEMINI_API_KEY:
        return "❌ کلید API پیدا نشد. لطفاً متغیر محیطی GEMINI_API_KEY را ست کنید."

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": question}]}
        ]
    }
    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()

        # استخراج جواب
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Gemini API Error:", e)
        return "متاسفم، نتونستم پاسخی از Gemini دریافت کنم."

# ==== روت اصلی ====
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_question = request.form.get("question", "").strip()
        if not user_question:
            return redirect(url_for("home"))

        # امبد سوال کاربر
        user_emb = model.encode(user_question, convert_to_tensor=True)

        # پیدا کردن نزدیک‌ترین سوال در FAQ
        best_match, best_score = None, -1
        for q, emb in faq_embeddings.items():
            score = util.pytorch_cos_sim(user_emb, emb).item()
            if score > best_score:
                best_score, best_match = score, q

        # پاسخ
        if best_score > 0.5:
            answer = faq[best_match]
        else:
            # اگر نبود → از Gemini بپرس
            answer = ask_gemini(user_question)
            # اضافه کردن سوال و جواب به FAQ و بردار جدید
            faq[user_question] = answer
            faq_embeddings[user_question] = model.encode(user_question, convert_to_tensor=True)

        # flash برای یک بار نمایش
        flash(user_question, "q")
        flash(answer, "a")

        return redirect(url_for("home"))

    # GET: برداشت flash‌ها
    question, answer = None, None
    for category, msg in get_flashed_messages(with_categories=True):
        if category == "q":
            question = msg
        elif category == "a":
            answer = msg

    return render_template_string(html, question=question, answer=answer)

# ==== باز کردن خودکار مرورگر ====
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# ==== قالب HTML ====
html = """
<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>پرسش و پاسخ شرکت</title>
    <style>
        body {
            margin: 0; padding: 0;
            font-family: Tahoma, sans-serif;
            background: linear-gradient(135deg, #74ABE2, #5563DE);
            height: 100vh; display: flex;
            justify-content: center; align-items: center;
        }
        .card {
            background: #fff; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            padding: 40px 30px; max-width: 500px; width: 90%; text-align: center;
        }
        h2 { color: #333; margin-bottom: 25px; }
        input[type="text"] {
            width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #ccc;
            margin-bottom: 15px; font-size: 16px;
        }
        button { background: #5563DE; color: #fff; border: none; padding: 12px 20px; border-radius: 8px;
                 font-size: 16px; cursor: pointer; transition: all 0.3s ease; }
        button:hover { background: #74ABE2; }
        .result { margin-top: 20px; background: #f1f1f1; padding: 15px; border-radius: 10px; }
        .controls button { background: #FF6B6B; margin-top: 10px; }
        .controls button:hover { background: #FF8787; }
        h3 { margin: 10px 0; color: #333; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🤖 سامانه پرسش و پاسخ شرکت</h2>
        <form method="POST">
            <input type="text" name="question" placeholder="سوال خود را وارد کنید..." required>
            <button type="submit">بپرس</button>
        </form>
        <div id="result" class="result">
            {% if answer %}
                <h3>❓ سوال: {{ question }}</h3>
                <h3>✅ پاسخ: {{ answer }}</h3>
                <div class="controls">
                    <button type="button" onclick="document.getElementById('result').innerHTML=''">
                        پاک کردن
                    </button>
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

# ==== اجرای برنامه ====
if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)
