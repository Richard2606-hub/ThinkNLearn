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

def generate_quiz(n=5, level="Beginner"):
    """Ask Gemini to create quiz questions and return as Python dict."""
    prompt = f"""
    You are an English language tutor.
    Make {n} multiple-choice questions for a {level} learner.
    Each question must have 4 choices (A–D), correct answer key, and explanation.
    Return JSON ONLY in this format:
    {{
      "questions":[
        {{"question":"...", "choices":["A) ...","B) ...","C) ...","D) ..."],
          "correct":"B", "explanation":"..."}}
      ]
    }}

    Topic: randomly give interesting daily life topics.
    The user must only choose one option each time.If the question answer correctly, show correct answer with congratulation to the user, if not tell the user the answer is incorrect, reason incorrect Aand try again.
    Return as visuable output.
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    return json.loads(raw)

def run_quiz():
    """Run the quiz interactively in terminal with attempt rules."""
    global attempts_today, last_attempt_date

    today = datetime.date.today()
    if last_attempt_date != today:
        # reset attempts for a new day
        attempts_today = 0
        last_attempt_date = today

    if attempts_today >= MAX_ATTEMPTS:
        print("🚫 You have reached the maximum of 3 attempts for today. Try again tomorrow.")
        return False  # stop running

    attempts_today += 1
    print(f"\n▶️ Attempt {attempts_today}/{MAX_ATTEMPTS}")

    quiz = generate_quiz()
    score = 0
    for i, q in enumerate(quiz["questions"], start=1):
        print(f"\nQ{i}: {q['question']}")
        for choice in q["choices"]:
            print(choice)
        user_ans = input("Your answer (A/B/C/D): ").strip().upper()
        if user_ans == q["correct"]:
            print("✅ Correct! 🎉")
            score += 1
        else:
            print(f"❌ Wrong. The correct answer is {q['correct']}. {q['explanation']}")

    percentage = (score / len(quiz["questions"])) * 100
    print(f"\nYour final score: {score}/{len(quiz['questions'])} = {percentage:.1f}%")

    if percentage >= 70:
        print("🎉 SUCCESSFUL! You passed the quiz.")
        return False  # stop running
    else:
        left = MAX_ATTEMPTS - attempts_today
        if left > 0:
            print(f"❌ FAIL. You scored below 70%.")
            print(f"You have {left} attempt(s) left today.")
            choice = input("Do you want to try again? (y/n): ").strip().lower()
            if choice == "y":
                return True   # continue with another attempt
            else:
                print("👋 Exiting quiz. See you next time!")
                return False
        else:
            print("🚫 FAIL. No attempts left today. Try again tomorrow.")
            return False

if __name__ == "__main__":
    while True:
        cont = run_quiz()
        if not cont:
            break



