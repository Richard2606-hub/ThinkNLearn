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

def generate_tutor_response(user_input, level="Beginner", topic="random daily life"):
    """
    Tutor generates the next line of dialogue and a teacher note
    in response to the user's input.
    """
    prompt = f"""
    You are a language tutor. 
    Level: {level}.
    Topic: {topic}.
    The learner just said: "{user_input}"

    Your task:
    - Respond naturally in the target language (Tutor's line).
    - Provide a 'teacherNote' correcting or improving the learner’s reply
      (grammar, vocabulary, phrasing).
    - Keep response short and conversational.

    Return JSON ONLY in this format:
    {{
      "tutor": "Tutor’s reply here",
      "teacherNote": "Correction or tip here"
    }}
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"tutor": "Sorry, I could not parse response.", "teacherNote": ""}

def run_dialogue(exchanges=10, min_required=5):
    """
    Run an interactive dialogue session.
    Tutor starts, learner replies, tutor corrects and continues.
    Learner must complete at least `min_required` exchanges
    before being allowed to type 'exit'.
    """
    print("\n--- Dialogue Practice ---")
    user_input = "Hello!"  # starting dummy message to trigger tutor opening line

    for i in range(exchanges):
        # Tutor responds
        result = generate_tutor_response(user_input)

        # Show tutor's reply
        print(f"\n👩‍🏫 Tutor: {result['tutor']}")
        if result['teacherNote']:
            print(f"   📝 Teacher Note: {result['teacherNote']}")

        # Learner's response
        if i + 1 >= min_required:
            user_input = input("🧑 You (type 'exit' to quit): ").strip()
            if user_input.lower() == "exit":
                print(f"👋 You completed {i+1} exchanges. Exiting dialogue and returning to main menu...")
                return
        else:
            user_input = input("🧑 You: ").strip()

    print(f"\n✅ Session ended after {exchanges} exchanges. Well done!")

def dialogue_menu():
    """
    Menu for dialogue practice.
    """
    while True:
        print("\n===== Dialogue Menu =====")
        print("1. Start Dialogue Practice")
        print("2. Exit to Main")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_dialogue()
        elif choice == "2":
            print("⬅️ Returning to main menu...")
            break
        else:
            print("❌ Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    dialogue_menu()
