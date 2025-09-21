# dialogue.py

import google.generativeai as genai
import json, re

# Geminiの設定
genai.configure(api_key="AIzaSyCxzO8G3M-pvipTrFHgkvL8aWfEj6nNPQY")
model = genai.GenerativeModel("gemini-2.5-flash")

def _clean_json(text: str) -> str:
    """```json の囲みを削除して有効な JSON 文字列を返す。"""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n|\n```$", "", text, flags=re.S)
    return text

def generate_tutor_response(user_input, level="初級", topic="日常生活"):
    """
    日本語チューターが学習者の入力に基づいて次の発話と指導メモを生成。
    """
    prompt = f"""
    あなたは日本語のチューターです。
    レベル: {level}。
    トピック: {topic}。
    学習者が次のように言いました: "{user_input}"

    あなたのタスク:
    - 日本語で自然に返答してください（チューターの発話）。
    - 学習者の返答を修正・改善する 'teacherNote' を提供してください
      （文法、語彙、表現など）。
    - 短く、会話的にしてください。

    以下のJSON形式のみで返してください:
    {{
      "tutor": "チューターの返答",
      "teacherNote": "修正やヒント"
    }}
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"tutor": "すみません、正しい返答を生成できませんでした。", "teacherNote": ""}

def run_dialogue(exchanges=10, min_required=5):
    """
    日本語の対話練習を実行。
    この対話は日本語のみで行います。
    チューターが話し始め、学習者が答え、チューターが修正し会話を続けます。
    学習者は少なくとも `min_required` 回のやり取りを完了しなければ、
    'exit' と入力して終了することはできません。
    """
    print("\n--- 日本語対話練習 ---")
    user_input = "こんにちは！"  # チューターの最初の発話を引き出すダミーメッセージ

    for i in range(exchanges):
        # チューターの返答
        result = generate_tutor_response(user_input)

        # 表示
        print(f"\n👩‍🏫 チューター: {result['tutor']}")
        if result['teacherNote']:
            print(f"   📝 教師のメモ: {result['teacherNote']}")

        # 学習者の入力
        if i + 1 >= min_required:
            user_input = input("🧑 あなた (終了するには 'exit' と入力): ").strip()
            if user_input.lower() == "exit":
                print(f"👋 あなたは {i+1} 回のやり取りを完了しました。対話を終了し、メインメニューに戻ります...")
                return
        else:
            user_input = input("🧑 あなた: ").strip()

    print(f"\n✅ セッション終了。合計 {exchanges} 回のやり取りを行いました。お疲れ様でした！")

def dialogue_menu():
    """
    日本語対話練習メニュー。
    """
    while True:
        print("\n===== 日本語対話メニュー =====")
        print("1. 対話練習を始める")
        print("2. メインメニューに戻る")
        choice = input("選択してください: ").strip()

        if choice == "1":
            run_dialogue()
        elif choice == "2":
            print("⬅️ メインメニューに戻ります...")
            break
        else:
            print("❌ 無効な選択です。1 または 2 を入力してください。")

if __name__ == "__main__":
    dialogue_menu()
