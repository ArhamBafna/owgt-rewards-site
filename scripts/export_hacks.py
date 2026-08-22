import json
import re

raw_path = r'C:\Users\bafna_sb19qr0\.gemini\antigravity-ide\brain\5239dcb5-4d60-45b4-8ec4-ee6838cb2d79\.system_generated\steps\12\content.md'
with open(raw_path, 'r', encoding='utf-8') as f:
    raw = f.read()

idx = raw.find('window.HACKS = [')
end_idx = raw.find('window.CATEGORIES = [')
js_array = raw[idx + len('window.HACKS = '):end_idx].strip().rstrip(';')

# Let's parse with node via quick one-liner or node script since it's valid JS object
with open('temp_hacks.js', 'w', encoding='utf-8') as f:
    f.write('const fs = require("fs");\n')
    f.write(f'const hacks = {js_array};\n')
    f.write('fs.writeFileSync("temp_hacks.json", JSON.stringify(hacks, null, 2));\n')

