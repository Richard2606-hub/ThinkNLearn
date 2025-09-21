import google.generativeai as genai
import json, re, datetime

# Configure Gemini
genai.configure(api_key="AIzaSyCxzO8G3M-pvipTrFHgkvL8aWfEj6nNPQY")
model = genai.GenerativeModel("gemini-2.5-flash")

# Tracking attempts
MAX_ATTEMPTS = 3
attempts_today = 0
last_attempt_date = None

def _clean_json(text: str) -> str:
    """Remove ```json fences and return valid JSON string."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n|\n```$", "", text, flags=re.S)
    return text

def _safe_json_loads(text: str):
    """Safely parse JSON, even if Gemini adds extra text."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if match:
            return json.loads(match.group(0))
        raise

def generate_quiz(n=5, level="Pemula"):
    """Minta Gemini buat soalan kuiz Bahasa Malaysia dalam format JSON."""
    prompt = f"""
    Anda ialah seorang tutor Bahasa Malaysia.
    Anda hanya boleh mengeluarkan soalan dan pilihan dalam Bahasa Melayu sahaja.
    Tugasan anda adalah memastikan pengguna boleh berkomunikasi dengan Bahasa Melayu.
    Hasilkan {n} soalan aneka pilihan (multiple-choice) untuk pelajar tahap {level}.
    Setiap soalan mesti ada 4 pilihan (A–D), jawapan yang betul, dan penjelasan ringkas.
    
    Pulangkan hanya dalam format JSON seperti ini:
    {{
      "questions":[
        {{"question":"...", "choices":["A) ...","B) ...","C) ...","D) ..."],
          "correct":"B", "explanation":"..."}}
      ]
    }}

    Topik: pilih secara rawak daripada topik menarik dalam kehidupan seharian.
    Peraturan:
    - Pelajar hanya boleh pilih SATU jawapan setiap kali.
    - Jika jawapan betul → tunjuk mesej tahniah.
    - Jika jawapan salah → beritahu jawapan salah, sertakan sebab, dan galakkan cuba lagi.
    Pulangkan dalam bentuk yang mudah dibaca oleh pengguna.
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    # Debug print if needed
    # print("DEBUG RAW:\n", raw)
    return _safe_json_loads(raw)

def run_quiz():
    """Jalankan kuiz secara interaktif di terminal dengan peraturan percubaan."""
    global attempts_today, last_attempt_date

    today = datetime.date.today()
    if last_attempt_date != today:
        # reset attempts for a new day
        attempts_today = 0
        last_attempt_date = today

    if attempts_today >= MAX_ATTEMPTS:
        print("🚫 Anda telah mencapai maksimum 3 percubaan untuk hari ini. Cuba lagi esok.")
        return False  # stop running

    attempts_today += 1
    print(f"\n▶️ Percubaan {attempts_today}/{MAX_ATTEMPTS}")

    quiz = generate_quiz()
    score = 0
    for i, q in enumerate(quiz["questions"], start=1):
        print(f"\nS{i}: {q['question']}")
        for choice in q["choices"]:
            print(choice)
        user_ans = input("Jawapan anda (A/B/C/D): ").strip().upper()
        if user_ans == q["correct"]:
            print("✅ Betul! 🎉 Tahniah!")
            score += 1
        else:
            print(f"❌ Salah. Jawapan yang betul ialah {q['correct']}. {q['explanation']}")

    percentage = (score / len(quiz["questions"])) * 100
    print(f"\nMarkah akhir anda: {score}/{len(quiz['questions'])} = {percentage:.1f}%")

    if percentage >= 70:
        print("🎉 BERJAYA! Anda lulus kuiz.")
        return False  # stop running
    else:
        left = MAX_ATTEMPTS - attempts_today
        if left > 0:
            print(f"❌ GAGAL. Markah anda kurang daripada 70%.")
            print(f"Anda ada {left} percubaan lagi hari ini.")
            choice = input("Adakah anda mahu cuba lagi? (y/n): ").strip().lower()
            if choice == "y":
                return True   # continue with another attempt
            else:
                print("👋 Keluar daripada kuiz. Jumpa lagi!")
                return False
        else:
            print("🚫 GAGAL. Tiada percubaan lagi untuk hari ini. Cuba lagi esok.")
            return False

if __name__ == "__main__":
    while True:
        cont = run_quiz()
        if not cont:
            break
