
import json

def add_questions(new_items_list):
    try:
        with open('questions.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
        
    seen_keys = set()
    for item in data:
        q_text = item['question'].lower().strip()
        ans_text = item['answer'].lower().strip()
        seen_keys.add((q_text, ans_text))
        
    added_count = 0
    for item in new_items_list:
        q_text = item['question'].lower().strip()
        ans_text = item['answer'].lower().strip()
        key = (q_text, ans_text)
        
        if key not in seen_keys:
            seen_keys.add(key)
            # Find max id
            max_id = max([q['id'] for q in data]) if data else 0
            item['id'] = max_id + 1
            data.append(item)
            added_count += 1
            
    with open('questions.json', 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"Added {added_count} unique questions. Total now: {len(data)}")

if __name__ == "__main__":
    import sys
    # This script will be called with a json file containing the new items
    with open(sys.argv[1], 'r') as f:
        new_items = json.load(f)
    add_questions(new_items)
