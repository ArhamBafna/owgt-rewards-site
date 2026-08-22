import re
import json

raw_path = r'C:\Users\bafna_sb19qr0\.gemini\antigravity-ide\brain\5239dcb5-4d60-45b4-8ec4-ee6838cb2d79\.system_generated\steps\12\content.md'
with open(raw_path, 'r', encoding='utf-8') as f:
    raw = f.read()

# Strip markdown header
idx = raw.find('window.HACKS = [')
js_code = raw[idx:]

# Let's find all entries in window.HACKS
# Extract each object
hack_matches = re.findall(r'\{\s*id:\s*"(.*?)",\s*title:\s*"(.*?)",\s*agents:\s*\[(.*?)],(?:\s*category:\s*"(.*?)",)?\s*summary:\s*"(.*?)",\s*body:\s*"(.*?)",\s*code:\s*`?(.*?)`?,\s*source:\s*"(.*?)",?\s*\}', js_code, re.DOTALL)

print(f"Total parsed by regex: {len(hack_matches)}")

# Let's also do a more robust manual bracket extraction
entries = []
start = js_code.find('[')
end = js_code.find('window.CATEGORIES')
array_content = js_code[start:end]

# Let's count how many { id: are in array_content
id_matches = re.findall(r'id:\s*"([^"]+)"', array_content)
print(f"Total IDs in array_content: {len(id_matches)}")
for i, hid in enumerate(id_matches):
    print(f"{i+1}: {hid}")
