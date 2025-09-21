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

def generate_quiz(n=5, level="초급"):
    """Gemini에게 한국어 퀴즈를 생성하도록 요청 (JSON 형식 반환)."""
    prompt = f"""
    당신은 한국어 튜터입니다.
    문제와 선택지는 반드시 한국어로 작성하세요.
    목표는 학습자가 한국어로 의사소통할 수 있도록 돕는 것입니다.
    {level} 학습자를 위해 {n} 개의 객관식 문제(multiple-choice)를 만들어 주세요.
    각 문제에는 4개의 선택지(A–D), 정답, 그리고 간단한 해설이 포함되어야 합니다.

    출력은 오직 다음 JSON 형식으로만 반환하세요:
    {{
      "questions":[
        {{"question":"...", "choices":["A) ...","B) ...","C) ...","D) ..."],
          "correct":"B", "explanation":"..."}}
      ]
    }}

    주제: 일상생활에서 흥미로운 주제를 무작위로 선택하세요.
    규칙:
    - 학습자는 매번 하나의 답만 선택할 수 있습니다.
    - 정답일 경우 → 축하 메시지를 보여주세요.
    - 오답일 경우 → 왜 틀렸는지 이유를 알려주고, 다시 시도하도록 격려하세요.
    사용자가 읽기 쉽게 출력하세요.
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    return _safe_json_loads(raw)

def run_quiz():
    """터미널에서 한국어 퀴즈 실행 (시도 횟수 제한 포함)."""
    global attempts_today, last_attempt_date

    today = datetime.date.today()
    if last_attempt_date != today:
        attempts_today = 0
        last_attempt_date = today

    if attempts_today >= MAX_ATTEMPTS:
        print("🚫 오늘의 3번 시도 기회를 모두 사용했습니다. 내일 다시 시도해 주세요.")
        return False

    attempts_today += 1
    print(f"\n▶️ {attempts_today}/{MAX_ATTEMPTS} 번째 시도")

    quiz = generate_quiz()
    score = 0
    for i, q in enumerate(quiz["questions"], start=1):
        print(f"\n문제 {i}: {q['question']}")
        for choice in q["choices"]:
            print(choice)
        user_ans = input("당신의 답 (A/B/C/D): ").strip().upper()
        if user_ans == q["correct"]:
            print("✅ 정답입니다! 🎉 축하합니다!")
            score += 1
        else:
            print(f"❌ 오답입니다. 정답은 {q['correct']} 입니다. {q['explanation']}")

    percentage = (score / len(quiz["questions"])) * 100
    print(f"\n최종 점수: {score}/{len(quiz['questions'])} = {percentage:.1f}%")

    if percentage >= 70:
        print("🎉 합격! 퀴즈를 통과했습니다.")
        return False
    else:
        left = MAX_ATTEMPTS - attempts_today
        if left > 0:
            print(f"❌ 불합격. 70% 이상이 필요합니다.")
            print(f"오늘은 {left} 번의 기회가 남아 있습니다.")
            choice = input("다시 도전하시겠습니까? (y/n): ").strip().lower()
            if choice == "y":
                return True
            else:
                print("👋 퀴즈를 종료합니다. 다음에 또 만나요!")
                return False
        else:
            print("🚫 불합격. 오늘의 시도 기회를 모두 사용했습니다. 내일 다시 시도해 주세요.")
            return False

if __name__ == "__main__":
    while True:
        cont = run_quiz()
        if not cont:
            break
