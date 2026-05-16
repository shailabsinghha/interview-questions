#!/usr/bin/env python3
import json
import re
import html
from collections import Counter

QUESTIONS_PATH = "/Users/shailabsingh/Desktop/interviewQues/questions.json"

def load_existing():
    with open(QUESTIONS_PATH) as f:
        data = json.load(f)
    return data

def save_questions(data):
    with open(QUESTIONS_PATH, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open(QUESTIONS_PATH) as f:
        json.load(f)

def normalize(s):
    return re.sub(r'\s+', ' ', s.lower().strip())

def is_duplicate(q_text, existing_qs):
    q_norm = normalize(q_text)[:100]
    for eq in existing_qs:
        eq_norm = normalize(eq['question'])[:100]
        if q_norm == eq_norm:
            return True
        if len(q_norm) > 25 and (q_norm in eq_norm or eq_norm in q_norm):
            return True
    return False

def assign_difficulty(question, answer):
    text = (question + " " + answer).lower()
    easy_words = ['basic', 'fundamental', 'define', 'what is', 'list', 'explain briefly',
                  'introduction', 'simple', 'overview', 'purpose of']
    hard_words = ['design', 'implement', 'optimize', 'architecture', 'complex', 'advanced',
                  'challenge', 'trade-off', 'production', 'large-scale', 'distributed',
                  'deep', 'tricky', 'critical', 'under the hood']
    easy_count = sum(1 for w in easy_words if w in text)
    hard_count = sum(1 for w in hard_words if w in text)
    if hard_count > easy_count and hard_count >= 1:
        return "Hard"
    elif easy_count > hard_count and easy_count >= 1:
        return "Easy"
    return "Medium"

def parse_gen_ai(filepath):
    with open(filepath) as f:
        content = f.read()
    questions = []
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)
    for section in sections:
        if not section.strip():
            continue
        lines = section.strip().split('\n')
        current_q = None
        current_a_lines = []
        in_answer = False
        for line in lines:
            q_match = re.match(r'^(\d+)\.\s+\*{0,2}(.+?)\*{0,2}\s*$', line)
            if q_match:
                if current_q:
                    answer = ' '.join(current_a_lines).strip()
                    if answer:
                        questions.append((current_q, answer))
                current_q = q_match.group(2).strip()
                current_a_lines = []
                in_answer = False
                continue
            if re.match(r'^-\s*Answer', line):
                in_answer = True
                ans_text = re.sub(r'^-\s*Answer:?\s*', '', line).strip()
                if ans_text:
                    current_a_lines.append(ans_text)
                continue
            if in_answer:
                if re.match(r'^\s*!\[', line):
                    continue
                if re.match(r'^\s*Image Source:', line, re.IGNORECASE):
                    continue
                if re.match(r'^\s*read this article:', line, re.IGNORECASE):
                    continue
                stripped = line.strip()
                if stripped:
                    stripped = re.sub(r'\*{1,2}', '', stripped)
                    current_a_lines.append(stripped)
        if current_q:
            answer = ' '.join(current_a_lines).strip()
            if answer:
                questions.append((current_q, answer))
    seen = set()
    unique = []
    for q, a in questions:
        key = normalize(q)[:80]
        if key not in seen:
            seen.add(key)
            unique.append((q, a))
    return unique

def parse_ml_gh(filepath):
    with open(filepath) as f:
        content = f.read()
    questions = []
    sections = re.split(r'\n####\s+\d+\)\s*', content)
    for i, section in enumerate(sections):
        if i == 0:
            continue
        lines = section.strip().split('\n')
        if not lines:
            continue
        question = lines[0].strip()
        question = re.sub(r'\[{2}src\]{2}\([^)]+\)', '', question).strip()
        question = re.sub(r'\s*\[{2}Answer\]{2}\([^)]+\)', '', question).strip()
        answer_lines = []
        for line in lines[1:]:
            stripped = line.strip()
            if re.match(r'^!\[', stripped):
                continue
            if stripped == '---':
                continue
            if re.match(r'^\[{2}src\]{2}', stripped):
                continue
            if stripped:
                answer_lines.append(stripped)
        answer = ' '.join(answer_lines).strip()
        if question and len(question) > 5:
            questions.append((question, answer if answer else "See the linked reference for answer."))
    return questions

def parse_gfg_ml(filepath):
    with open(filepath) as f:
        content = f.read()
    content = html.unescape(content)
    content = re.sub(r'<[^>]+>', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    questions = []
    q_matches = list(re.finditer(
        r'(\d+)\.\s+(What|Explain|Define|How|Why|Describe|Differentiate|List|What\'s|Is|When|What are|What is)([^?]*\?)',
        content, re.IGNORECASE))
    for i, match in enumerate(q_matches):
        q_text = match.group(0).strip()
        start = match.end()
        end = q_matches[i+1].start() if i + 1 < len(q_matches) else len(content)
        raw_answer = content[start:end].strip()
        if len(raw_answer) > 2000:
            raw_answer = raw_answer[:2000]
        if q_text and raw_answer:
            questions.append((q_text, raw_answer))
    return questions

def parse_js_questions(filepath):
    with open(filepath) as f:
        content = f.read()
    m = re.search(r'<!-- QUESTIONS_START -->(.*?)<!-- QUESTIONS_END -->', content, re.DOTALL)
    if not m:
        return []
    qa_section = m.group(1)
    qa_blocks = re.findall(
        r'(\d+)\.\s+###\s+(.+?)(?=\n\d+\.\s+###|\Z)',
        qa_section, re.DOTALL
    )
    questions = []
    for num, block in qa_blocks:
        lines = block.strip().split('\n')
        q_text = lines[0].strip()
        answer_lines = []
        for line in lines[1:]:
            stripped = line.strip()
            if stripped.startswith('```'):
                continue
            if '[⬆ Back to Top]' in stripped:
                continue
            if stripped:
                answer_lines.append(stripped)
        answer = '\n'.join(answer_lines).strip()
        if q_text and answer:
            questions.append((q_text, answer))
    return questions

def parse_react_questions(filepath):
    with open(filepath) as f:
        content = f.read()
    questions = []
    sections = re.split(r'\n##\s+', content)
    for section in sections:
        if not section.strip():
            continue
        first_line = section.strip().split('\n')[0]
        if first_line in ('Miscellaneous', 'Old Q&A', 'Disclaimer'):
            continue
        qa_blocks = re.findall(
            r'\n\s*(\d+)\.\s+###\s+(.+?)(?=\n\s*\d+\.\s+###|\n##|\Z)',
            section, re.DOTALL
        )
        for num, block in qa_blocks:
            lines = block.strip().split('\n')
            q_text = lines[0].strip()
            answer_lines = []
            for line in lines[1:]:
                stripped = line.strip()
                if stripped.startswith('```'):
                    continue
                if '[⬆ Back to Top]' in stripped:
                    continue
                if stripped:
                    answer_lines.append(stripped)
            answer = '\n'.join(answer_lines).strip()
            if q_text and answer:
                questions.append((q_text, answer))
    return questions

def parse_css_questions(filepath):
    with open(filepath) as f:
        content = f.read()
    questions = []
    sections = re.split(r'\n##\s+(\d+)\.\s+', content)
    if len(sections) < 2:
        return questions
    for i in range(1, len(sections), 2):
        if i+1 >= len(sections):
            break
        block = sections[i+1]
        lines = block.strip().split('\n')
        q_text = lines[0].strip()
        answer_lines = []
        for line in lines[1:]:
            stripped = line.strip()
            if stripped.startswith('```'):
                continue
            if stripped:
                answer_lines.append(stripped)
        answer = '\n'.join(answer_lines).strip()
        if q_text and answer:
            questions.append((q_text, answer))
    return questions

def parse_backend_questions(filepath):
    with open(filepath) as f:
        content = f.read()
    questions = []
    # Format: #### Question Topic\nQuestion text... (no answers in this source)
    # Find all #### headings followed by question text
    sections = re.split(r'\n####\s+', content)
    for section in sections[1:]:  # skip preamble
        lines = section.strip().split('\n')
        topic = lines[0].strip()
        # Build question text from remaining lines
        q_lines = []
        for line in lines[1:]:
            stripped = line.strip()
            if stripped.startswith('[Resources]'):
                continue
            if stripped.startswith('<br/>'):
                continue
            if stripped.startswith('###'):
                continue
            if stripped:
                q_lines.append(stripped)
        q_text = ' '.join(q_lines).strip()
        if q_text and len(q_text) > 20:
            # Combine topic and question
            full_q = f"{topic}: {q_text}" if not q_text.lower().startswith(topic.lower()) else q_text
            questions.append((full_q, "Open-ended discussion question. No single correct answer - intended to assess the candidate's depth of understanding and experience."))
    return questions

def parse_gfg_css(filepath):
    with open(filepath) as f:
        content = f.read()
    content = html.unescape(content)
    content = re.sub(r'<[^>]+>', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    questions = []
    q_matches = list(re.finditer(
        r'(\d+)\.\s+(What|How|Explain|Define|Why|Describe|List|What\'s|When|Which|Can|Suggest|Is|What are)([^?]*\?)',
        content, re.IGNORECASE))
    for i, match in enumerate(q_matches):
        q_text = match.group(0).strip()
        start = match.end()
        end = q_matches[i+1].start() if i + 1 < len(q_matches) else len(content)
        raw_answer = content[start:end].strip()
        if len(raw_answer) > 2000:
            raw_answer = raw_answer[:2000]
        if q_text and raw_answer:
            questions.append((q_text, raw_answer))
    return questions

def parse_angular_greatfrontend(filepath):
    """GreatFrontend Angular questions - same format as JS sudheerj with QUESTIONS_START/END markers."""
    with open(filepath) as f:
        content = f.read()
    m = re.search(r'<!-- QUESTIONS:START -->(.*?)<!-- QUESTIONS:END -->', content, re.DOTALL)
    if not m:
        return []
    qa_section = m.group(1)
    qa_blocks = re.findall(
        r'(\d+)\.\s+###\s+(.+?)(?=\n\d+\.\s+###|\Z)',
        qa_section, re.DOTALL
    )
    questions = []
    for num, block in qa_blocks:
        lines = block.strip().split('\n')
        q_text = lines[0].strip()
        answer_lines = []
        for line in lines[1:]:
            stripped = line.strip()
            if stripped.startswith('```'):
                continue
            if '[Back to top ↑]' in stripped or '[Back to Top]' in stripped:
                continue
            if stripped.startswith('<!--') and stripped.endswith('-->'):
                continue
            if stripped.startswith('> Try out'):
                continue
            if stripped:
                answer_lines.append(stripped)
        answer = '\n'.join(answer_lines).strip()
        if q_text and answer:
            questions.append((q_text, answer))
    return questions

def parse_angular_sudheerj(filepath):
    """Sudheerj Angular questions - same format as React."""
    with open(filepath) as f:
        content = f.read()
    questions = []
    qa_blocks = re.findall(
        r'\n\s*(\d+)\.\s+###\s+(.+?)(?=\n\s*\d+\.\s+###|\Z)',
        content, re.DOTALL
    )
    for num, block in qa_blocks:
        lines = block.strip().split('\n')
        q_text = lines[0].strip()
        answer_lines = []
        for line in lines[1:]:
            stripped = line.strip()
            if stripped.startswith('```'):
                continue
            if '[⬆ Back to Top]' in stripped:
                continue
            if stripped:
                answer_lines.append(stripped)
        answer = '\n'.join(answer_lines).strip()
        if q_text and answer:
            questions.append((q_text, answer))
    return questions

def parse_gfg_angular(filepath):
    """GFG Angular questions - same as other GFG sources."""
    with open(filepath) as f:
        content = f.read()
    content = html.unescape(content)
    content = re.sub(r'<[^>]+>', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    questions = []
    q_matches = list(re.finditer(
        r'(\d+)\.\s+(What|How|Explain|Define|Why|Describe|List|What\'s|When|Which|Can|Is|What are|What is|Name|Differentiate|Suggest)([^?]*\?)',
        content, re.IGNORECASE))
    for i, match in enumerate(q_matches):
        q_text = match.group(0).strip()
        start = match.end()
        end = q_matches[i+1].start() if i + 1 < len(q_matches) else len(content)
        raw_answer = content[start:end].strip()
        if len(raw_answer) > 2000:
            raw_answer = raw_answer[:2000]
        if q_text and raw_answer:
            questions.append((q_text, raw_answer))
    return questions

def parse_devto_css(filepath):
    with open(filepath) as f:
        content = f.read()
    text = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html.unescape(text)
    text = re.sub(r'\n\s*\n', '\n', text)
    questions = []
    lines = text.split('\n')
    current_q = None
    current_a_lines = []
    in_answer = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_answer:
                current_a_lines.append('')
            continue
        q_match = re.match(r'^(\d+)\.\s+(What|How|Explain|Define|Why|Describe|List|Can|When|Which|Is|What are|What is)\b', stripped, re.IGNORECASE)
        if q_match:
            if current_q and current_a_lines:
                answer = ' '.join(current_a_lines).strip()
                if answer:
                    questions.append((current_q, answer))
            current_q = stripped
            current_a_lines = []
            in_answer = True
        elif in_answer and current_q:
            if stripped.startswith('Learn more') or stripped.startswith('Learn More'):
                continue
            if stripped.startswith('http') or stripped.startswith('www'):
                continue
            current_a_lines.append(stripped)
    if current_q and current_a_lines:
        answer = ' '.join(current_a_lines).strip()
        if answer:
            questions.append((current_q, answer))
    return questions

def parse_perfmatrix(filepath):
    with open(filepath) as f:
        content = f.read()
    text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html.unescape(text)
    text = re.sub(r'\n\s*\n+', '\n', text)
    questions = []
    lines = text.split('\n')
    current_q = None
    current_a = []
    collecting = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        q_match = re.match(r'^Q\.?\s*(\d+)\s+(.*)', stripped)
        if q_match:
            if current_q and current_a:
                answer = ' '.join(current_a).strip()
                answer = re.sub(r'^\s*Ans[.:]?\s*', '', answer).strip()
                if answer:
                    questions.append((current_q, answer))
            current_q = q_match.group(2).strip()
            current_a = []
            collecting = True
        elif collecting:
            if (stripped.startswith('Read More') or stripped.startswith('You may be interested')
                or stripped.startswith('Advertisements') or stripped.startswith('Share this')
                or stripped.startswith('Tags:') or stripped.startswith('Categories')
                or 'Recent Posts' in stripped or 'Follow Us' in stripped
                or 'PerfMatrix Academy' in stripped):
                continue
            current_a.append(stripped)
    if current_q and current_a:
        answer = ' '.join(current_a).strip()
        answer = re.sub(r'^\s*Ans[.:]?\s*', '', answer).strip()
        if answer:
            questions.append((current_q, answer))
    return questions

def parse_devinterview(filepath):
    with open(filepath) as f:
        content = f.read()
    if '\\n' in content:
        content = content.replace('\\n', '\n')
    questions = []
    lines = content.split('\n')
    current_q = None
    current_a = []
    collecting = False
    expect_question_text = False
    in_answer = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('Sign in to unlock') or stripped.startswith('Get unlimited access'):
            break
        if stripped in ('Question', 'Answer', 'Answer:'):
            if stripped in ('Answer', 'Answer:'):
                in_answer = True
            continue
        if any(s in stripped for s in ['Track progress', 'Save time', 'Simple interface', 'Land a six-figure',
                                        'Ready to nail', 'Stand out', 'Kickstart', 'Blog', 'Terms of use',
                                        'Privacy policy', 'Pricing', 'FAQs', 'Contact Us', '© 20', 'Go up',
                                        'Huge timesaver', "It's an excellent tool", "Fantastic catalogue",
                                        'Ace your next', 'Explore our carefully', 'Start preparing', 'Web & Mobile Dev',
                                        'Data Structures & Algorithms', 'System Design', 'Machine Learning',
                                        'Behavioral Questions', 'ADO.NET', 'Agile & Scrum', 'Android', 'Angular',
                                        'AngularJS', 'ASP.NET', 'AWS', 'Azure', 'C++', 'C#', 'CSS', 'DevOps',
                                        'Django', 'Docker', 'Flutter', 'GIT', 'Golang', 'GraphQL', 'HTML5',
                                        'Ionic', 'Java', 'JavaScript', 'jQuery', 'Kotlin', 'Laravel', 'MongoDB',
                                        '.NET Core', 'Next.js', 'Node.js', 'Python', 'React', 'Redis', 'Redux',
                                        'Ruby', 'Rust', 'SQL', 'Swift', 'TypeScript', 'Vue.js']):
            continue
        # Handle "N." on its own line
        num_match = re.match(r'^(\d+)\.$', stripped)
        if num_match:
            if current_q and current_a:
                answer_text = '\n'.join(current_a).strip()
                if len(answer_text) > 10:
                    questions.append((current_q, answer_text))
            current_q = None
            current_a = []
            collecting = True
            expect_question_text = True
            in_answer = False
            continue
        # If we just saw "N.", the next non-trivial line is the question text
        if expect_question_text and collecting:
            current_q = stripped
            expect_question_text = False
            in_answer = False
            continue
        if in_answer and current_q:
            current_a.append(stripped)
    if current_q and current_a:
        answer_text = '\n'.join(current_a).strip()
        if len(answer_text) > 10:
            questions.append((current_q, answer_text))
    return questions

def parse_gfg(filepath):
    with open(filepath) as f:
        content = f.read()
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<br\s*/?>', '\n', content)
    content = re.sub(r'<p[^>]*>', '\n', content)
    content = re.sub(r'</p>', '\n', content)
    content = re.sub(r'<li[^>]*>', '\n', content)
    content = re.sub(r'</li>', '\n', content)
    content = re.sub(r'<h[1-6][^>]*>', '\n', content)
    content = re.sub(r'</h[1-6]>', '\n', content)
    content = re.sub(r'<strong[^>]*>', '', content)
    content = re.sub(r'</strong>', '', content)
    content = re.sub(r'<[^>]+>', '\n', content)
    content = html.unescape(content)
    questions = []
    lines = content.split('\n')
    current_q = None
    current_a = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        q_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if q_match:
            if current_q and current_a:
                answer = ' '.join(current_a).strip()
                if len(answer) > 10:
                    questions.append((current_q, answer))
            current_q = q_match.group(2).strip().rstrip('.')
            current_a = []
        elif current_q:
            current_a.append(stripped)
    if current_q and current_a:
        answer = ' '.join(current_a).strip()
        if len(answer) > 10:
            questions.append((current_q, answer))
    return questions

def parse_security_headers(filepath):
    with open(filepath) as f:
        content = f.read()
    questions = []
    lines = content.split('\n')
    current_q = None
    current_a = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        q_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if q_match:
            if current_q and current_a:
                answer = '\n'.join(current_a).strip()
                if answer:
                    questions.append((current_q, answer))
            current_q = q_match.group(2).strip()
            current_a = []
        elif current_q:
            current_a.append(stripped)
    if current_q and current_a:
        answer = '\n'.join(current_a).strip()
        if answer:
            questions.append((current_q, answer))
    return questions

def main():
    print("Loading existing questions...")
    data = load_existing()
    print(f"Existing: {len(data)} entries, last ID: {data[-1]['id']}")
    next_id = data[-1]['id'] + 1
    total_added = 0
    results = {}

    sources = [
        ("Generative AI", parse_gen_ai, "/tmp/gen_ai_questions.md"),
        ("Machine Learning", parse_ml_gh, "/tmp/ml_questions_gh.md"),
        ("Machine Learning", parse_gfg_ml, "/tmp/gfg_ml_questions.txt"),
        ("JavaScript", parse_js_questions, "/tmp/js_questions.md"),
        ("React", parse_react_questions, "/tmp/react_questions.md"),
        ("CSS", parse_css_questions, "/tmp/css_questions.md"),
        ("CSS", parse_gfg_css, "/tmp/gfg_css_questions.txt"),
        ("Backend Development", parse_backend_questions, "/tmp/backend_questions.md"),
        ("CSS", parse_devto_css, "/tmp/devto_css.md"),
        ("Angular", parse_angular_greatfrontend, "/tmp/angular_greatfrontend.md"),
        ("Angular", parse_angular_sudheerj, "/tmp/angular_sudheerj.md"),
        ("Angular", parse_gfg_angular, "/tmp/gfg_angular_questions.txt"),
        ("Performance", parse_perfmatrix, "/tmp/perfmatrix_questions.html"),
        ("Spring Boot", parse_devinterview, "/tmp/devinterview_spring.txt"),
        ("React", parse_devinterview, "/tmp/devinterview_react.txt"),
        ("JavaScript", parse_devinterview, "/tmp/devinterview_javascript.txt"),
        ("Spring Boot", parse_gfg, "/tmp/gfg_spring_security.txt"),
    ]

    for topic, parser, filepath in sources:
        name = filepath.split('/')[-1]
        print(f"\nParsing {name}...")
        try:
            parsed = parser(filepath)
            print(f"  Parsed {len(parsed)} raw question pairs")
        except Exception as e:
            print(f"  ERROR parsing: {e}")
            results[name] = 0
            continue
        new_items = []
        for q, a in parsed:
            if not is_duplicate(q, data):
                entry = {
                    "id": next_id,
                    "topic": topic,
                    "question": q,
                    "answer": a,
                    "difficulty": assign_difficulty(q, a)
                }
                new_items.append(entry)
                data.append(entry)
                next_id += 1
        results[name] = len(new_items)
        total_added += len(new_items)
        print(f"  Added {len(new_items)} new questions (topic: {topic})")

    print(f"\nSaving {len(data)} entries...")
    save_questions(data)

    print("\n" + "="*60)
    print("MERGE SUMMARY")
    print("="*60)
    for name, count in results.items():
        print(f"  {name}: {count} questions added")
    print(f"  Total new questions added: {total_added}")
    print(f"  Final total in questions.json: {len(data)}")

    c = Counter(q['topic'] for q in data)
    print("\nTopic counts:")
    for topic, count in sorted(c.items(), key=lambda x: -x[1]):
        print(f"  {topic}: {count}")

    try:
        with open(QUESTIONS_PATH) as f:
            json.load(f)
        print(f"\nAll entries valid JSON: Yes")
    except:
        print(f"\nAll entries valid JSON: NO - INVALID JSON!")

if __name__ == "__main__":
    main()
