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

def generate_quiz(n=5, level="初学者"):
    """请Gemini生成中文语言测验题，并以JSON格式返回。"""
    prompt = f"""
    你是一位中文语言导师。
    你只能使用中文来编写问题和选项。
    你的任务是帮助学习者提高中文交流能力。
    请为{level}学习者生成{n}道选择题（multiple-choice）。
    每道题必须包含 4 个选项（A–D）、正确答案和简要解释。

    只返回以下JSON格式：
    {{
      "questions":[
        {{"question":"...", "choices":["A) ...","B) ...","C) ...","D) ..."],
          "correct":"B", "explanation":"..."}}
      ]
    }}

    题目主题：从日常生活中随机选择有趣的话题。
    规则：
    - 学习者每次只能选择一个答案。
    - 如果答案正确 → 显示祝贺信息。
    - 如果答案错误 → 告诉学习者答案错误，说明原因，并鼓励再次尝试。
    请返回清晰、易于用户阅读的格式。
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    return _safe_json_loads(raw)

def run_quiz():
    """运行终端交互式测验，并遵守尝试次数规则。"""
    global attempts_today, last_attempt_date

    today = datetime.date.today()
    if last_attempt_date != today:
        # reset attempts for a new day
        attempts_today = 0
        last_attempt_date = today

    if attempts_today >= MAX_ATTEMPTS:
        print("🚫 今天的3次尝试次数已用完，请明天再来。")
        return False  # stop running

    attempts_today += 1
    print(f"\n▶️ 第 {attempts_today}/{MAX_ATTEMPTS} 次尝试")

    quiz = generate_quiz()
    score = 0
    for i, q in enumerate(quiz["questions"], start=1):
        print(f"\n题目{i}: {q['question']}")
        for choice in q["choices"]:
            print(choice)
        user_ans = input("你的答案 (A/B/C/D): ").strip().upper()
        if user_ans == q["correct"]:
            print("✅ 正确！🎉 恭喜你！")
            score += 1
        else:
            print(f"❌ 错误。正确答案是 {q['correct']}。{q['explanation']}")

    percentage = (score / len(quiz["questions"])) * 100
    print(f"\n你的最终得分: {score}/{len(quiz['questions'])} = {percentage:.1f}%")

    if percentage >= 70:
        print("🎉 恭喜！你通过了测验。")
        return False  # stop running
    else:
        left = MAX_ATTEMPTS - attempts_today
        if left > 0:
            print(f"❌ 未通过。你的得分低于70%。")
            print(f"今天还剩 {left} 次尝试机会。")
            choice = input("是否要继续尝试？(y/n): ").strip().lower()
            if choice == "y":
                return True   # continue with another attempt
            else:
                print("👋 尝试机会已用完，下次见！")
                return False
        else:
            print("🚫 未通过。今天的尝试次数已用完，请明天再来。")
            return False

if __name__ == "__main__":
    while True:
        cont = run_quiz()
        if not cont:
            break
