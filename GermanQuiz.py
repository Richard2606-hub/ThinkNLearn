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

def generate_quiz(n=5, level="Anfänger"):
    """Lässt Gemini ein Deutsch-Quiz im JSON-Format erstellen."""
    prompt = f"""
    Du bist ein Deutschlehrer.
    Erstelle alle Fragen und Antwortmöglichkeiten ausschließlich auf Deutsch.
    Dein Ziel ist es, den Lernenden beim Erlernen und Kommunizieren in deutscher Sprache zu unterstützen.
    Erstelle {n} Multiple-Choice-Fragen für Lernende auf dem Niveau {level}.
    Jede Frage muss 4 Antwortmöglichkeiten (A–D), die richtige Antwort und eine kurze Erklärung enthalten.

    Gib die Ausgabe ausschließlich im folgenden JSON-Format zurück:
    {{
      "questions":[
        {{"question":"...", "choices":["A) ...","B) ...","C) ...","D) ..."],
          "correct":"B", "explanation":"..."}}
      ]
    }}

    Thema: Wähle zufällig interessante Themen aus dem Alltag.
    Regeln:
    - Der Lernende darf jedes Mal nur EINE Antwort auswählen.
    - Wenn die Antwort richtig ist → zeige eine Glückwunsch-Nachricht.
    - Wenn die Antwort falsch ist → erkläre, warum sie falsch ist, und ermutige zum erneuten Versuch.
    Gib die Ausgabe in einem klaren und benutzerfreundlichen Format zurück.
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    return _safe_json_loads(raw)

def run_quiz():
    """Führt ein interaktives Deutsch-Quiz im Terminal mit Versuchsregeln aus."""
    global attempts_today, last_attempt_date

    today = datetime.date.today()
    if last_attempt_date != today:
        # Reset attempts for a new day
        attempts_today = 0
        last_attempt_date = today

    if attempts_today >= MAX_ATTEMPTS:
        print("🚫 Du hast heute schon 3 Versuche gemacht. Bitte versuche es morgen erneut.")
        return False

    attempts_today += 1
    print(f"\n▶️ Versuch {attempts_today}/{MAX_ATTEMPTS}")

    quiz = generate_quiz()
    score = 0
    for i, q in enumerate(quiz["questions"], start=1):
        print(f"\nFrage {i}: {q['question']}")
        for choice in q["choices"]:
            print(choice)
        user_ans = input("Deine Antwort (A/B/C/D): ").strip().upper()
        if user_ans == q["correct"]:
            print("✅ Richtig! 🎉 Glückwunsch!")
            score += 1
        else:
            print(f"❌ Falsch. Die richtige Antwort ist {q['correct']}. {q['explanation']}")

    percentage = (score / len(quiz["questions"])) * 100
    print(f"\nDein Endergebnis: {score}/{len(quiz['questions'])} = {percentage:.1f}%")

    if percentage >= 70:
        print("🎉 BESTANDEN! Du hast das Quiz erfolgreich abgeschlossen.")
        return False
    else:
        left = MAX_ATTEMPTS - attempts_today
        if left > 0:
            print(f"❌ NICHT BESTANDEN. Du brauchst mindestens 70%.")
            print(f"Du hast heute noch {left} Versuch(e).")
            choice = input("Möchtest du es noch einmal versuchen? (y/n): ").strip().lower()
            if choice == "y":
                return True
            else:
                print("👋 Quiz beendet. Bis zum nächsten Mal!")
                return False
        else:
            print("🚫 NICHT BESTANDEN. Keine Versuche mehr heute. Bitte versuche es morgen erneut.")
            return False

if __name__ == "__main__":
    while True:
        cont = run_quiz()
        if not cont:
            break
