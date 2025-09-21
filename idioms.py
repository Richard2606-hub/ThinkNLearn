import google.generativeai as genai

genai.configure(api_key="AIzaSyCxzO8G3M-pvipTrFHgkvL8aWfEj6nNPQY")

# Create model with temperature setting for more randomness
generation_config = {
    "temperature": 0.9,  # Higher temperature = more random/creative responses
    "top_p": 0.95,
    "top_k": 40,
}

model = genai.GenerativeModel("gemini-2.5-flash", generation_config=generation_config)

def generate_idioms(language="English", context="workplace", count=5):
    if language.lower() == "chinese":
        prompt = f"""
用中文提供{count}个关于{context}的常见成语。
对于每个成语，请以清晰易读的格式提供：成语、含义、例句和使用时机。
请使用以下格式：
1. [成语]
   含义: [解释]
   例句: [例句]
   使用时机: [使用场景]
"""
    elif language.lower() == "bahasa melayu":
        prompt = f"""
Berikan {count} pepatah umum dalam Bahasa Melayu mengenai {context}.
Untuk setiap pepatah, sertakan: frasa, maksud, contoh, dan bila untuk menggunakannya dalam format yang mudah dibaca.
Gunakan format berikut:
1. [Frasa]
   Maksud: [Penerangan]
   Contoh: [Contoh ayat]
   Bila digunakan: [Situasi penggunaan]
"""

    elif language.lower() == "french":
        prompt = f"""
Fournissez {count} expressions idiomatiques françaises courantes concernant {context}.
Pour chaque expression, incluez : l'expression, sa signification, un exemple et quand l'utiliser dans un format lisible.
Utilisez le format suivant :
1. [Expression]
   Signification: [Explication]
   Exemple: [Phrase exemple]
   Quand l'utiliser: [Situation d'utilisation]
"""
    elif language.lower() == "german":
        prompt = f"""
Bitte geben Sie {count} gebräuchliche deutsche Redewendungen zum Thema {context} an.
Für jede Redewendung geben Sie bitte an: die Redewendung, ihre Bedeutung, ein Beispiel und wann man sie verwendet in einem lesbaren Format.
Verwenden Sie das folgende Format:
1. [Redewendung]
   Bedeutung: [Erklärung]
   Beispiel: [Beispielsatz]
   Verwendung: [Verwendungssituation]
"""
    elif language == "tamil":
        prompt = f"""
{context} பற்றிய {count} பொதுவான தமிழ் பழமொழிகளை கொடுக்கவும்.
ஒவ்வொரு பழமொழிக்கும், பழமொழி, அர்த்தம், உதாரணம், மற்றும் பயன்படுத்தும் நேரம் ஆகியவற்றை வாசிக்க எளிதான வடிவத்தில் வழங்கவும்.
பின்வரும் வடிவத்தைப் பயன்படுத்தவும்:
1. [பழமொழி]
   அர்த்தம்: [விளக்கம்]
   உதாரணம்: [உதாரண வாக்கியம்]
   பயன்படுத்தும் நேரம்: [பயன்படுத்தும் சூழ்நிலை]
"""
    elif language == "japanese":
        prompt = f"""
{context}に関する{count}つの一般的な日本語の慣用句を提供してください。
各慣用句について、読みやすい形式で次のものを含めてください：表現、意味、例文、使用するタイミング。
次の形式を使用してください：
1. [表現]
   意味: [説明]
   例文: [例文]
   使用するタイミング: [使用場面]
"""
    elif language == "korean":
        prompt = f"""
{context}에 관한 {count}개의 일반적인 한국어 관용구를 제공해 주세요.
각 관용구에 대해 다음을 읽기 쉬운 형식으로 포함해 주세요: 관용구, 의미, 예문, 사용 시기.
다음 형식을 사용해 주세요:
1. [관용구]
   의미: [설명]
   예문: [예문]
   사용 시기: [사용 상황]
"""
    else:
        prompt = f"""
Provide {count} common {language} idioms for {context}.
For each idiom, include: phrase, meaning, example, and when to use in a readable format.
Use the following format:
1. [Phrase]
   Meaning: [Explanation]
   Example: [Example sentence]
   When to use: [Usage situation]
"""

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print("English Workplace Idioms:")
    print(generate_idioms("English", "workplace", 5))
    print("\n" + "="*50 + "\n")
    
    print("Chinese Idioms:")
    print(generate_idioms("Chinese", "general", 5))
    print("\n" + "="*50 + "\n")
    
    print("Malay Education Idioms:")
    print(generate_idioms("Bahasa Melayu", "education", 5))
    
    print("French Workplace Idioms:")
    print(generate_idioms("French", "workplace", 5))
    print("\n" + "="*50 + "\n")
    
    print("German Business Idioms:")
    print(generate_idioms("German", "business", 5))
    print("\n" + "="*50 + "\n")
    
    print("Tamil Life Idioms:")
    print(generate_idioms("Tamil", "life", 5))
    print("\n" + "="*50 + "\n")
    
    print("Japanese Work Idioms:")
    print(generate_idioms("Japanese", "work", 5))
    print("\n" + "="*50 + "\n")
    
    print("Korean Life Idioms:")
    print(generate_idioms("Korean", "life", 5))
    print("\n" + "="*50 + "\n")