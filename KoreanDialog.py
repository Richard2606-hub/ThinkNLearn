# dialogue.py

import google.generativeai as genai
import json, re

# Gemini 설정
genai.configure(api_key="AIzaSyCxzO8G3M-pvipTrFHgkvL8aWfEj6nNPQY")
model = genai.GenerativeModel("gemini-2.5-flash")

def _clean_json(text: str) -> str:
    """```json 감싸기를 제거하고 유효한 JSON 문자열 반환"""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n|\n```$", "", text, flags=re.S)
    return text

def generate_tutor_response(user_input, level="초급", topic="일상생활"):
    """
    한국어 튜터가 학습자의 입력에 따라 다음 대화문과 교정 메모를 생성.
    """
    prompt = f"""
    당신은 한국어 튜터입니다.
    수준: {level}.
    주제: {topic}.
    학습자가 방금 이렇게 말했습니다: "{user_input}"

    당신의 역할:
    - 한국어로 자연스럽게 대답합니다 (튜터의 대사).
    - 학습자의 답변을 교정하거나 개선할 수 있는 'teacherNote'를 제공합니다
      (문법, 어휘, 표현 방식).
    - 짧고 대화체로 유지하세요.

    반드시 다음 JSON 형식으로만 출력하세요:
    {{
      "tutor": "튜터의 답변",
      "teacherNote": "교정 또는 팁"
    }}
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"tutor": "죄송합니다. 올바른 응답을 생성할 수 없습니다.", "teacherNote": ""}

def run_dialogue(exchanges=10, min_required=5):
    """
    한국어 대화 연습 세션 실행.
    이 대화는 한국어로만 진행됩니다.
    튜터가 먼저 말하고, 학습자가 대답하며, 튜터가 교정을 제공하고 계속 이어갑니다.
    학습자는 최소 `min_required` 회 이상 대화를 완료해야 'exit'로 종료할 수 있습니다.
    """
    print("\n--- 한국어 대화 연습 ---")
    user_input = "안녕하세요!"  # 첫 튜터 발화를 유도하는 시작 메시지

    for i in range(exchanges):
        # 튜터 응답
        result = generate_tutor_response(user_input)

        # 튜터 발화 표시
        print(f"\n👩‍🏫 튜터: {result['tutor']}")
        if result['teacherNote']:
            print(f"   📝 교사 노트: {result['teacherNote']}")

        # 학습자 입력
        if i + 1 >= min_required:
            user_input = input("🧑 당신 (종료하려면 'exit' 입력): ").strip()
            if user_input.lower() == "exit":
                print(f"👋 당신은 {i+1} 회의 대화를 완료했습니다. 대화를 종료하고 메인 메뉴로 돌아갑니다...")
                return
        else:
            user_input = input("🧑 당신: ").strip()

    print(f"\n✅ 세션이 {exchanges} 회 대화 후 종료되었습니다. 수고하셨습니다!")

def dialogue_menu():
    """
    한국어 대화 연습 메뉴.
    """
    while True:
        print("\n===== 한국어 대화 메뉴 =====")
        print("1. 대화 연습 시작")
        print("2. 메인 메뉴로 돌아가기")
        choice = input("옵션을 선택하세요: ").strip()

        if choice == "1":
            run_dialogue()
        elif choice == "2":
            print("⬅️ 메인 메뉴로 돌아갑니다...")
            break
        else:
            print("❌ 잘못된 선택입니다. 1 또는 2를 입력하세요.")

if __name__ == "__main__":
    dialogue_menu()
