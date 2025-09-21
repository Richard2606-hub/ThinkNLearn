# dialogue.py

import google.generativeai as genai
import json, re

# Gemini konfigurieren
genai.configure(api_key="AIzaSyCxzO8G3M-pvipTrFHgkvL8aWfEj6nNPQY")
model = genai.GenerativeModel("gemini-2.5-flash")

def _clean_json(text: str) -> str:
    """Entfernt ```json-Markierungen und gibt einen gültigen JSON-String zurück."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n|\n```$", "", text, flags=re.S)
    return text

def generate_tutor_response(user_input, level="Anfänger", topic="Alltagsleben"):
    """
    Deutsch-Tutor erzeugt die nächste Dialogzeile
    und eine Korrektur-Notiz basierend auf der Eingabe des Lerners.
    """
    prompt = f"""
    Du bist ein Deutsch-Tutor.
    Niveau: {level}.
    Thema: {topic}.
    Der Lerner hat gerade gesagt: "{user_input}"

    Deine Aufgaben:
    - Antworte natürlich auf Deutsch (Antwort des Tutors).
    - Füge eine 'teacherNote' hinzu, die die Antwort des Lerners korrigiert oder verbessert
      (Grammatik, Wortschatz, Ausdrucksweise).
    - Halte die Antwort kurz und gesprächsorientiert.

    Gib NUR im folgenden JSON-Format zurück:
    {{
      "tutor": "Antwort des Tutors hier",
      "teacherNote": "Korrektur oder Tipp hier"
    }}
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"tutor": "Entschuldigung, ich konnte keine gültige Antwort generieren.", "teacherNote": ""}

def run_dialogue(exchanges=10, min_required=5):
    """
    Führe eine interaktive Deutsch-Dialog-Sitzung durch.
    Der Dialog darf nur auf Deutsch geführt werden.
    Der Tutor beginnt, der Lerner antwortet, der Tutor gibt Feedback und fährt fort.
    Der Lerner muss mindestens `min_required` Austauschzeilen absolvieren,
    bevor er mit 'exit' beenden darf.
    """
    print("\n--- Deutsch Dialogübung ---")
    user_input = "Hallo!"  # Startnachricht, um die erste Tutor-Antwort auszulösen

    for i in range(exchanges):
        # Tutor-Antwort
        result = generate_tutor_response(user_input)

        # Ausgabe des Tutors
        print(f"\n👩‍🏫 Tutor: {result['tutor']}")
        if result['teacherNote']:
            print(f"   📝 Hinweis des Tutors: {result['teacherNote']}")

        # Antwort des Lerners
        if i + 1 >= min_required:
            user_input = input("🧑 Du (tippe 'exit' zum Beenden): ").strip()
            if user_input.lower() == "exit":
                print(f"👋 Du hast {i+1} Zeilen abgeschlossen. Dialog wird beendet und zum Hauptmenü zurückgekehrt...")
                return
        else:
            user_input = input("🧑 Du: ").strip()

    print(f"\n✅ Sitzung beendet nach {exchanges} Zeilen. Gut gemacht!")

def dialogue_menu():
    """
    Menü für die Dialogübung.
    """
    while True:
        print("\n===== Deutsch Dialog-Menü =====")
        print("1. Dialogübung starten")
        print("2. Zurück zum Hauptmenü")
        choice = input("Wähle eine Option: ").strip()

        if choice == "1":
            run_dialogue()
        elif choice == "2":
            print("⬅️ Zurück zum Hauptmenü...")
            break
        else:
            print("❌ Ungültige Auswahl. Bitte wähle 1 oder 2.")

if __name__ == "__main__":
    dialogue_menu()
