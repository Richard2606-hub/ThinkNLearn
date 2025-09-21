# dialogue.py

import google.generativeai as genai
import json, re

# 配置 Gemini
genai.configure(api_key="AIzaSyCxzO8G3M-pvipTrFHgkvL8aWfEj6nNPQY")
model = genai.GenerativeModel("gemini-2.5-flash")

def _clean_json(text: str) -> str:
    """去除 ```json 包裹，返回有效的 JSON 字符串。"""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n|\n```$", "", text, flags=re.S)
    return text

def generate_tutor_response(user_input, level="初学者", topic="日常生活"):
    """
    中文导师根据学习者输入生成下一句对话和教学提示。
    """
    prompt = f"""
    你是一名中文语言导师。
    水平: {level}。
    话题: {topic}。
    学习者刚刚说: "{user_input}"

    你的任务:
    - 用中文自然地回复 (导师的对话)。
    - 提供一个 'teacherNote'，对学习者的回答进行纠正或改进
      （语法、词汇、表达方式）。
    - 保持简短、口语化。

    只返回以下 JSON 格式：
    {{
      "tutor": "导师的回复",
      "teacherNote": "修改或提示"
    }}
    """
    response = model.generate_content(prompt)
    raw = _clean_json(response.text or "")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"tutor": "抱歉，我无法生成正确的回复。", "teacherNote": ""}

def run_dialogue(exchanges=10, min_required=5):
    """
    运行一个中文互动对话会话。
    本对话只能使用中文交流。
    导师先说，学习者回答，导师提供纠正并继续。
    学习者必须完成至少 `min_required` 轮对话后才能输入 'exit' 退出。
    """
    print("\n--- 中文对话练习 ---")
    user_input = "你好！"  # 初始触发导师开场白

    for i in range(exchanges):
        # 导师回复
        result = generate_tutor_response(user_input)

        # 显示导师回复
        print(f"\n👩‍🏫 导师: {result['tutor']}")
        if result['teacherNote']:
            print(f"   📝 教师提示: {result['teacherNote']}")

        # 学习者输入
        if i + 1 >= min_required:
            user_input = input("🧑 你 (输入 'exit' 退出): ").strip()
            if user_input.lower() == "exit":
                print(f"👋 你已完成 {i+1} 轮对话。退出并返回主菜单...")
                return
        else:
            user_input = input("🧑 你: ").strip()

    print(f"\n✅ 会话结束，共完成 {exchanges} 轮。做得好！")

def dialogue_menu():
    """
    中文对话练习菜单。
    """
    while True:
        print("\n===== 中文对话菜单 =====")
        print("1. 开始对话练习")
        print("2. 返回主菜单")
        choice = input("请选择: ").strip()

        if choice == "1":
            run_dialogue()
        elif choice == "2":
            print("⬅️ 返回主菜单...")
            break
        else:
            print("❌ 无效的选择，请输入 1 或 2。")

if __name__ == "__main__":
    dialogue_menu()
