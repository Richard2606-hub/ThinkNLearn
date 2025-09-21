import json
import os
import time
from collections import Counter
from typing import List, Dict, Any

_DB = "progress.json"

def _load() -> List[Dict[str, Any]]:
    """Load progress data from JSON file"""
    if not os.path.exists(_DB):
        return []
    try:
        with open(_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _save(items: List[Dict[str, Any]]) -> None:
    """Save progress data to JSON file"""
    with open(_DB, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def record(user_id: str, activity_type: str, topic: str = None, 
          score: float = None, mistakes: List[str] = None) -> None:
    """Record a new progress entry"""
    items = _load()
    items.append({
        "userId": user_id,
        "ts": int(time.time()),
        "type": activity_type,
        "topic": topic,
        "score": score,
        "mistakes": mistakes or []
    })
    _save(items)

def last_n(user_id: str, n: int = 10) -> List[Dict[str, Any]]:
    """Get last n entries for a user"""
    items = [x for x in _load() if x["userId"] == user_id]
    return sorted(items, key=lambda x: x["ts"], reverse=True)[:n]

def get_common_mistakes(user_id: str, limit: int = 5) -> List[str]:
    """Get most common mistakes for a user"""
    items = [x for x in _load() if x["userId"] == user_id]
    all_mistakes = []
    for item in items:
        all_mistakes.extend(item.get("mistakes", []))
    
    counter = Counter(all_mistakes)
    return [mistake for mistake, count in counter.most_common(limit)]

def generate_practice_prompt(user_id: str) -> str:
    """Generate practice prompt based on common mistakes"""
    common_mistakes = get_common_mistakes(user_id)
    if not common_mistakes:
        return "No mistakes found. Continue with regular practice."
    
    mistake_list = ", ".join(common_mistakes)
    return f"""
The learner struggles with: {mistake_list}
Create 3 practice questions focusing on these areas.
Return response in JSON format with keys: 'questions' (array of strings) and 'explanation' (string).
"""

if __name__ == "__main__":
    # Example usage
    record("student1", "quiz", "Grammar", 3.5, ["verb tense", "prepositions"])
    record("student1", "dialogue", "Food", 4.2, ["articles"])
    
    print("Last 5 entries:")
    print(json.dumps(last_n("student1", 5), indent=2))
    
    print("\nCommon mistakes:")
    print(get_common_mistakes("student1"))
    
    print("\nPractice prompt:")
    print(generate_practice_prompt("student1"))