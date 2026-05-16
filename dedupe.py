
import json

def perform_deduplication():
    with open('questions.json', 'r') as f:
        data = json.load(f)
    
    seen_keys = set()
    unique_data = []
    
    for item in data:
        # Normalize for deduplication
        q_text = item['question'].lower().strip()
        ans_text = item['answer'].lower().strip()
        key = (q_text, ans_text)
        
        if key not in seen_keys:
            seen_keys.add(key)
            unique_data.append(item)
    
    # Re-index IDs
    for i, item in enumerate(unique_data):
        item['id'] = i + 1
        
    with open('questions_unique.json', 'w') as f:
        json.dump(unique_data, f, indent=2)
    
    print(f"Original: {len(data)}")
    print(f"Unique: {len(unique_data)}")

if __name__ == "__main__":
    perform_deduplication()
