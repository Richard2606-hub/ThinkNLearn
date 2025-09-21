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
    """Supprime les balises ```json et renvoie une chaîne JSON valide."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n|\n```$", "", text, flags=re.S)
    return text

def _safe_json_loads(text: str):
    """Analyse JSON en toute sécurité, même si Gemini ajoute du texte supplémentaire."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if match:
            return json.loads(match.group(0))
        raise

def generate_quiz(n=5, level="Débutant"):
    """Demander à Gemini de générer un quiz de français en JSON."""
    prompt = f"""
    Tu es un tuteur de langue française.
    Rédige toutes les questions et options uniquement en français.
    Ta mission est d’aider les apprenants à améliorer leur communication en français.
    Génère {n} questions à choix multiples (QCM) pour un apprenant de niveau {level}.
    Chaque question doit avoir 4 options (A–D), la bonne réponse et une explication simple.

    Retourne UNIQUEMENT dans ce format JSON :
    {{
      "questions":[
        {{"question":"...", "choices":["A) ...","B) ...","C) ...","D) ..."],
          "correct":"B", "explanation":"..."}}
      ]
    }}

    Thème : choisis au hasard des sujets intéressants de la vie quotidienne.
    Règles :
    - L’apprenant ne peut choisir QU’UNE seule réponse à chaque fois.
    - Si la réponse est correcte → affiche un message de félicitations.
    - Si la réponse est incorrecte → explique pourquoi c’est faux et encourage à réessayer.
    Retourne dans un format clair et facile à lire pour l’utilisateur.
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    return _safe_json_loads(raw)

def run_quiz():
    """Exécute un quiz interactif en français avec règle de tentatives."""
    global attempts_today, last_attempt_date

    today = datetime.date.today()
    if last_attempt_date != today:
        attempts_today = 0
        last_attempt_date = today

    if attempts_today >= MAX_ATTEMPTS:
        print("🚫 Tu as déjà utilisé tes 3 tentatives pour aujourd’hui. Réessaie demain.")
        return False

    attempts_today += 1
    print(f"\n▶️ Tentative {attempts_today}/{MAX_ATTEMPTS}")

    quiz = generate_quiz()
    score = 0
    for i, q in enumerate(quiz["questions"], start=1):
        print(f"\nQuestion {i}: {q['question']}")
        for choice in q["choices"]:
            print(choice)
        user_ans = input("Ta réponse (A/B/C/D) : ").strip().upper()
        if user_ans == q["correct"]:
            print("✅ Correct ! 🎉 Félicitations !")
            score += 1
        else:
            print(f"❌ Faux. La bonne réponse est {q['correct']}. {q['explanation']}")

    percentage = (score / len(quiz["questions"])) * 100
    print(f"\nTon score final : {score}/{len(quiz['questions'])} = {percentage:.1f}%")

    if percentage >= 70:
        print("🎉 BRAVO ! Tu as réussi le quiz.")
        return False
    else:
        left = MAX_ATTEMPTS - attempts_today
        if left > 0:
            print(f"❌ ÉCHEC. Ton score est inférieur à 70%.")
            print(f"Il te reste {left} tentative(s) aujourd’hui.")
            choice = input("Veux-tu réessayer ? (y/n) : ").strip().lower()
            if choice == "y":
                return True
            else:
                print("👋 Fin du quiz. À bientôt !")
                return False
        else:
            print("🚫 ÉCHEC. Tu as épuisé toutes tes tentatives pour aujourd’hui. Réessaie demain.")
            return False

if __name__ == "__main__":
    while True:
        cont = run_quiz()
        if not cont:
            break
