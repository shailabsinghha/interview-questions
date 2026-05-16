
import json
import collections

def deduplicate():
    with open('questions.json', 'r') as f:
        data = json.load(f)
    
    seen_questions = {}
    unique_data = []
    duplicates_count = 0
    
    for item in data:
        # Normalize question for comparison
        q_text = item['question'].lower().strip()
        # Some duplicates have suffixes like " in a distributed system"
        # We can try to catch those by looking at the core question or answer
        ans_text = item['answer'].lower().strip()
        
        key = (q_text, ans_text)
        
        if key not in seen_questions:
            seen_questions[key] = item
            unique_data.append(item)
        else:
            duplicates_count += 1
            
    print(f"Total questions: {len(data)}")
    print(f"Unique questions: {len(unique_data)}")
    print(f"Duplicates removed: {duplicates_count}")
    
    # Analyze topics and difficulties of removed items
    removed_counts = collections.Counter()
    for item in data:
        q_text = item['question'].lower().strip()
        ans_text = item['answer'].lower().strip()
        key = (q_text, ans_text)
        if key in seen_questions and seen_questions[key] != item:
             removed_counts[(item['topic'], item['difficulty'])] += 1
             
    print("\nRemoved counts by (Topic, Difficulty) sorted:")
    for k, v in sorted(removed_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{k}: {v}")

    # Analyze unique counts by topic
    unique_topic_counts = collections.Counter()
    for item in unique_data:
        unique_topic_counts[item['topic']] += 1
    
    print("\nUnique counts by Topic:")
    for k, v in unique_topic_counts.items():
        print(f"{k}: {v}")

    return unique_data, duplicates_count

if __name__ == "__main__":
    deduplicate()
