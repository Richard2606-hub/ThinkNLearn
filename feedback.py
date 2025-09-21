# feedback.py
from gemini_utils import ask_json
import json

def generate_feedback(text: str, level="Beginner"):
    prompt = f"""
Correct the learner text and explain simply for a {level} learner.
Text: "{text}"

Return JSON exactly in this format:
{{
  "corrected": "...",
  "explanation": "...",
  "quickTips": ["...","..."],
  "tags": ["verb_tense","articles"]
}}

Use tags to label common mistakes (e.g., "verb_tense", "articles", "word_choice").
""".strip()

    result = ask_json(prompt)
    
    # Debug: Print the raw response
    print(f"DEBUG: Raw response type: {type(result)}")
    print(f"DEBUG: Raw response content: {result}")
    
    # If result is a string, try to parse it as JSON
    if isinstance(result, str):
        try:
            parsed = json.loads(result)
            return parsed
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON response: {e}")
            # Try to extract JSON from the response if it's wrapped in text
            if "```json" in result:
                # Try to extract JSON from markdown code blocks
                try:
                    json_start = result.find("```json") + 7
                    json_end = result.find("```", json_start)
                    json_str = result[json_start:json_end].strip()
                    return json.loads(json_str)
                except:
                    pass
            return None
    return result

def main():
    print("⚡ Language Feedback Generator")
    print("Type 'quit' to exit.\n")
    
    while True:
        # Get user input
        text = input("Enter your text: ").strip()
        if text.lower() == 'quit':
            break
            
        level = input("Enter proficiency level (Beginner/Intermediate/Advanced) [Default: Beginner]: ").strip()
        if not level:
            level = "Beginner"
            
        # Generate feedback
        print("\nGenerating feedback...")
        result = generate_feedback(text, level)
        
        # Check if result is valid before accessing its properties
        if result and isinstance(result, dict):
            print("\nCorrected Text:", result.get("corrected", "N/A"))
            print("Explanation:", result.get("explanation", "N/A"))
            print("Quick Tips:")
            for tip in result.get("quickTips", []):
                print("  -", tip)
            print("Tags:", ", ".join(result.get("tags", [])))
        else:
            print("Failed to generate feedback. Please try again.")
        print("-" * 50 + "\n")

if __name__ == "__main__":
    main()