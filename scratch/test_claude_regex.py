import re

def test_37():
    with open('data/pdfs-to-text/(V1) 37 CLAUDE PROMPTS THAT SAVE MANAGERS 10+ HOURS PER WEEK Organised by the 8 Situations Every Manager Faces-text.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    matches = re.findall(r'Prompt #\d+:\s*(.*?)\n(.*?)(?=\nPro tip:|\nAlso in this situation:|\nPrompt #\d+:|\Z)', text, re.DOTALL)
    print(f"37 Prompts: Found {len(matches)}")
    for m in matches:
        print(f" - {m[0]}")

test_37()
