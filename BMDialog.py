# dialogue.py

import google.generativeai as genai
import json, re

# Configure Gemini
genai.configure(api_key="AIzaSyCxzO8G3M-pvipTrFHgkvL8aWfEj6nNPQY")
model = genai.GenerativeModel("gemini-2.5-flash")

def _clean_json(text: str) -> str:
    """Remove ```json fences and return valid JSON string."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n|\n```$", "", text, flags=re.S)
    return text

def generate_tutor_response(user_input, level="Pemula", topic="kehidupan harian"):
    """
    Tutor Bahasa Malaysia menghasilkan baris dialog seterusnya
    dan nota pembetulan berdasarkan input pelajar.
    """
    prompt = f"""
    Anda ialah seorang tutor Bahasa Malaysia.
    Tahap: {level}.
    Topik: {topic}.
    Pelajar baru sahaja berkata: "{user_input}"

    Tugas anda:
    - Balas secara semula jadi dalam Bahasa Malaysia (jawapan tutor).
    - Sertakan 'teacherNote' yang membetulkan atau menambah baik jawapan pelajar
      (tatabahasa, kosa kata, gaya bahasa).
    - Pastikan jawapan ringkas dan berbentuk perbualan.

    Pulangkan hanya dalam format JSON seperti ini:
    {{
      "tutor": "Jawapan tutor di sini",
      "teacherNote": "Pembetulan atau tip di sini"
    }}
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"tutor": "Maaf, saya tidak dapat menjana respons yang betul.", "teacherNote": ""}

def run_dialogue(exchanges=10, min_required=5):
    """
    Jalankan sesi dialog interaktif.
    Dialog ini cuma boleh mengguna Bahasa Melayu untuk berkomunikasi sahaja.
    Tutor mula bercakap, pelajar membalas, tutor beri pembetulan dan teruskan.
    Pelajar mesti melengkapkan sekurang-kurangnya `min_required` pertukaran
    sebelum dibenarkan untuk taip 'exit'.
    """
    print("\n--- Latihan Dialog ---")
    user_input = "Hai!"  # mesej permulaan untuk aktifkan baris pertama tutor

    for i in range(exchanges):
        # Respons tutor
        result = generate_tutor_response(user_input)

        # Papar balasan tutor
        print(f"\n👩‍🏫 Tutor: {result['tutor']}")
        if result['teacherNote']:
            print(f"   📝 Nota Guru: {result['teacherNote']}")

        # Balasan pelajar
        if i + 1 >= min_required:
            user_input = input("🧑 Anda (taip 'exit' untuk keluar): ").strip()
            if user_input.lower() == "exit":
                print(f"👋 Anda telah melengkapkan {i+1} baris. Keluar daripada dialog dan kembali ke menu utama...")
                return
        else:
            user_input = input("🧑 Anda: ").strip()

    print(f"\n✅ Sesi tamat selepas {exchanges} baris. Syabas!")

def dialogue_menu():
    """
    Menu untuk latihan dialog.
    """
    while True:
        print("\n===== Menu Dialog =====")
        print("1. Mula Latihan Dialog")
        print("2. Keluar ke Menu Utama")
        choice = input("Pilih satu pilihan: ").strip()

        if choice == "1":
            run_dialogue()
        elif choice == "2":
            print("⬅️ Kembali ke menu utama...")
            break
        else:
            print("❌ Pilihan tidak sah. Sila pilih 1 atau 2.")

if __name__ == "__main__":
    dialogue_menu()
