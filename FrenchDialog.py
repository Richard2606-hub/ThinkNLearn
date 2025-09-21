# dialogue.py

import google.generativeai as genai
import json, re

# Configurer Gemini
genai.configure(api_key="AIzaSyCxzO8G3M-pvipTrFHgkvL8aWfEj6nNPQY")
model = genai.GenerativeModel("gemini-2.5-flash")

def _clean_json(text: str) -> str:
    """Supprimer les balises ```json et retourner une chaîne JSON valide."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n|\n```$", "", text, flags=re.S)
    return text

def generate_tutor_response(user_input, level="Débutant", topic="vie quotidienne"):
    """
    Le tuteur de français génère la prochaine réplique
    et une note de correction basée sur la réponse de l’apprenant.
    """
    prompt = f"""
    Vous êtes un tuteur de français.
    Niveau: {level}.
    Thème: {topic}.
    L’apprenant vient de dire: "{user_input}"

    Votre tâche:
    - Répondre naturellement en français (réplique du tuteur).
    - Fournir une 'teacherNote' qui corrige ou améliore la réponse de l’apprenant
      (grammaire, vocabulaire, formulation).
    - Garder la réponse courte et conversationnelle.

    Retournez uniquement ce format JSON :
    {{
      "tutor": "Réponse du tuteur ici",
      "teacherNote": "Correction ou conseil ici"
    }}
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"tutor": "Désolé, je n’ai pas pu générer une réponse valide.", "teacherNote": ""}

def run_dialogue(exchanges=10, min_required=5):
    """
    Lancer une session de dialogue interactif.
    La conversation se fait uniquement en français.
    Le tuteur commence, l’apprenant répond, le tuteur corrige et continue.
    L’apprenant doit compléter au moins `min_required` échanges
    avant de pouvoir taper 'exit'.
    """
    print("\n--- Pratique de dialogue en français ---")
    user_input = "Bonjour !"  # message initial pour lancer la première réplique du tuteur

    for i in range(exchanges):
        # Réponse du tuteur
        result = generate_tutor_response(user_input)

        # Afficher la réplique du tuteur
        print(f"\n👩‍🏫 Tuteur: {result['tutor']}")
        if result['teacherNote']:
            print(f"   📝 Note du professeur: {result['teacherNote']}")

        # Réponse de l’apprenant
        if i + 1 >= min_required:
            user_input = input("🧑 Vous (tapez 'exit' pour quitter): ").strip()
            if user_input.lower() == "exit":
                print(f"👋 Vous avez complété {i+1} échanges. Fin du dialogue et retour au menu principal...")
                return
        else:
            user_input = input("🧑 Vous: ").strip()

    print(f"\n✅ Session terminée après {exchanges} échanges. Bravo !")

def dialogue_menu():
    """
    Menu pour la pratique de dialogue.
    """
    while True:
        print("\n===== Menu Dialogue =====")
        print("1. Commencer la pratique de dialogue")
        print("2. Retourner au menu principal")
        choice = input("Choisissez une option: ").strip()

        if choice == "1":
            run_dialogue()
        elif choice == "2":
            print("⬅️ Retour au menu principal...")
            break
        else:
            print("❌ Choix invalide. Veuillez sélectionner 1 ou 2.")

if __name__ == "__main__":
    dialogue_menu()
