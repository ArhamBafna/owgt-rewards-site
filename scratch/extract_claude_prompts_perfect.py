import os
import glob
import re

# 1. Delete all existing Claude Prompts
existing = glob.glob('organized-data/Prompts/*.md')
for f in existing:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    if '### Category\nPrompts' in content or 'Extracted from' in content:
        os.remove(f)

def clean_filename(name):
    safe_name = name.lower()
    safe_name = re.sub(r'[^a-z0-9\-]', '-', safe_name)
    safe_name = re.sub(r'-+', '-', safe_name).strip('-')
    return safe_name[:60]

def write_prompt(title, prompt_text):
    prompt_text = re.sub(r'(Pro tip:.*|3 years covering AI.*|Also in this situation:.*)', '', prompt_text, flags=re.IGNORECASE|re.DOTALL).strip()
    
    if len(prompt_text.split()) < 10:
        return 0
        
    safe_name = clean_filename(title)
    if not safe_name:
        return 0
        
    sentences = re.split(r'(?<=[.!?])\s+', prompt_text)
    first_sentence = sentences[0].strip()
    if len(first_sentence) > 100:
        first_sentence = first_sentence[:100] + "..."
    desc = f"A ready-to-use prompt that instructs the AI to: {first_sentence}"
    
    md_content = f"### Name\n{title.title()}\n\n### Description\n{desc}\n\n### Prompt\n```text\n{prompt_text}\n```\n\n### Category\nPrompts\n\n### Tags\n- Prompt\n- Workflow\n"
    
    out_path = f"organized-data/Prompts/{safe_name}.md"
    # To avoid overwriting existing ones from prompts.txt that might share a name
    if os.path.exists(out_path):
        out_path = f"organized-data/Prompts/claude-{safe_name}.md"
        
    with open(out_path, 'w', encoding='utf-8') as out_f:
        out_f.write(md_content)
    return 1

total_extracted = 0

# 37 Prompts
with open('data/pdfs-to-text/(V1) 37 CLAUDE PROMPTS THAT SAVE MANAGERS 10+ HOURS PER WEEK Organised by the 8 Situations Every Manager Faces-text.txt', 'r', encoding='utf-8') as f:
    text = f.read()
matches = re.findall(r'Prompt #\d+:\s*(.*?)\n(.*?)(?=\nPro tip:|\nAlso in this situation:|\nPrompt #\d+:|\Z)', text, re.DOTALL)
for m in matches:
    total_extracted += write_prompt(m[0].strip(), m[1].strip())

# 25 Prompts
with open('data/pdfs-to-text/V1 -  The AI Decision Playbook 25 Claude Prompts for Better Business Decisions-text.txt', 'r', encoding='utf-8') as f:
    text = f.read()
matches = re.findall(r'\d+\.\s+([A-Z][^\n]*?)\s*\n"([^"]+)"', text, re.DOTALL)
for m in matches:
    total_extracted += write_prompt(m[0].strip(), m[1].strip())

# 50 Prompts
with open('data/pdfs-to-text/V1 - 50 Claude Prompts Every Founder Should Bookmark-text.txt', 'r', encoding='utf-8') as f:
    text = f.read()
matches = re.findall(r'\d+\.\s+([A-Z][^\n]*?)\s*\n"([^"]+)"', text, re.DOTALL)
for m in matches:
    total_extracted += write_prompt(m[0].strip(), m[1].strip())

# 75 Prompts
with open('data/pdfs-to-text/THE AI REPORT - 75 CLAUDE PROMPTS-text.txt', 'r', encoding='utf-8') as f:
    text = f.read()
matches = re.findall(r'([A-Z][^\[]*?\[[^\]]+\])', text, re.DOTALL)
verbs = ['Rewrite', 'Draft', 'Summarize', 'Write', 'Turn', 'Create', 'Compare', 'Analyze', 'Give', 'Edit', 'What', 'Identify', 'Build', 'Act', 'Generate', 'List', 'Explain', 'Review', 'Critique', 'Extract', 'Format', 'Translate']
for m in matches:
    m = m.replace('\n', ' ').strip()
    m = re.sub(r'^\d+\.\s*', '', m) # remove numbers
    first_word = m.split(' ')[0]
    if first_word in verbs or first_word.rstrip(':') in verbs:
        title_words = m.split(' ')[:5]
        title = " ".join(title_words).strip(':.,')
        total_extracted += write_prompt(title, m)

print(f"Perfect Claude Extraction: {total_extracted} prompts extracted.")
