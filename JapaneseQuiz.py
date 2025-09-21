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

def generate_quiz(n=5, level="初級"):
    """日本語のクイズ問題をJSON形式で生成する。"""
    prompt = f"""
    あなたは日本語のチューターです。
    問題文と選択肢はすべて日本語で作成してください。
    学習者が日本語でコミュニケーションできるようにすることが目的です。
    {level} 学習者向けに {n} 問の多肢選択式（multiple-choice）問題を作成してください。
    各問題には4つの選択肢（A–D）、正解、および簡単な解説を含めてください。

    出力は次のJSON形式のみで返してください：
    {{
      "questions":[
        {{"question":"...", "choices":["A) ...","B) ...","C) ...","D) ..."],
          "correct":"B", "explanation":"..."}}
      ]
    }}

    トピック: 日常生活の中からランダムに面白いテーマを選んでください。
    ルール:
    - 学習者は1回につき1つの答えしか選べません。
    - 正解の場合 → おめでとうメッセージを表示してください。
    - 不正解の場合 → 不正解であることを伝え、理由を説明し、再挑戦を促してください。
    出力はユーザーが読みやすい形式にしてください。
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    return _safe_json_loads(raw)

def run_quiz():
    """端末で日本語のクイズを実行し、試行回数のルールを適用する。"""
    global attempts_today, last_attempt_date

    today = datetime.date.today()
    if last_attempt_date != today:
        # reset attempts for a new day
        attempts_today = 0
        last_attempt_date = today

    if attempts_today >= MAX_ATTEMPTS:
        print("🚫 今日の3回の挑戦回数を使い切りました。明日もう一度挑戦してください。")
        return False  # stop running

    attempts_today += 1
    print(f"\n▶️ 第 {attempts_today}/{MAX_ATTEMPTS} 回目の挑戦")

    quiz = generate_quiz()
    score = 0
    for i, q in enumerate(quiz["questions"], start=1):
        print(f"\n問題{i}: {q['question']}")
        for choice in q["choices"]:
            print(choice)
        user_ans = input("あなたの答え (A/B/C/D): ").strip().upper()
        if user_ans == q["correct"]:
            print("✅ 正解！🎉 おめでとう！")
            score += 1
        else:
            print(f"❌ 不正解。正しい答えは {q['correct']} です。{q['explanation']}")

    percentage = (score / len(quiz["questions"])) * 100
    print(f"\n最終スコア: {score}/{len(quiz['questions'])} = {percentage:.1f}%")

    if percentage >= 70:
        print("🎉 合格！クイズに合格しました。")
        return False  # stop running
    else:
        left = MAX_ATTEMPTS - attempts_today
        if left > 0:
            print(f"❌ 不合格。70%以上が必要です。")
            print(f"今日はあと {left} 回挑戦できます。")
            choice = input("もう一度挑戦しますか？ (y/n): ").strip().lower()
            if choice == "y":
                return True   # continue with another attempt
            else:
                print("👋 クイズを終了します。また次回！")
                return False
        else:
            print("🚫 不合格。本日の挑戦回数を使い切りました。明日もう一度挑戦してください。")
            return False

if __name__ == "__main__":
    while True:
        cont = run_quiz()
        if not cont:
            break
