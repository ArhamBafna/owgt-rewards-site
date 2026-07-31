import os
import re
import json
import requests
from dotenv import load_dotenv

# Load .env from parent directory
load_dotenv('../.env')
api_key = os.getenv('OPENROUTER_API_KEY')

if not api_key:
    print("OPENROUTER_API_KEY not found!")
    exit(1)

def clean_filename(name):
    safe_name = name.lower()
    safe_name = re.sub(r'[^a-z0-9\-]', '-', safe_name)
    safe_name = re.sub(r'-+', '-', safe_name).strip('-')
    return safe_name[:60]

def extract_tools(text, model="openai/gpt-4o"):
    prompt = """You are an expert data extractor. I am giving you the raw text of a PDF that lists various AI Tools. 
Because the PDF had a multi-column layout, the text is a bit scrambled, but generally the tool names appear first, followed by their descriptions ('What it does:', 'Business outcome:', 'Best for:').
Your task is to carefully extract each tool mentioned and output a JSON list.

Output ONLY a valid JSON array of objects. Do NOT include markdown code blocks around the JSON.
Each object must have exactly these keys:
- "name": The name of the AI tool (e.g. "Perplexity", "Grok")
- "description": A concise, natural 1-2 sentence summary of what the tool is and its value.
- "content": A clean paragraph explaining what it does, workflows it replaces, and who it is best for. Do NOT include headers like 'What it does:' - just write it as a natural, readable text block.

Example output:
[
  {
    "name": "Perplexity",
    "description": "An AI-powered search engine that retrieves and synthesizes information from the web with citations for every claim.",
    "content": "Perplexity replaces the manual research briefing. Instead of reading dozens of sources and writing a summary, you ask a specific question and receive a sourced, synthesized answer in seconds. It is best for research, competitive intelligence, legal, and compliance functions."
  }
]
"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        "temperature": 0.1
    }
    
    print(f"Calling OpenRouter with model {model}...")
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return []
        
    result_text = response.json()['choices'][0]['message']['content'].strip()
    
    # Strip markdown if present
    if result_text.startswith("```json"):
        result_text = result_text[7:]
    if result_text.endswith("```"):
        result_text = result_text[:-3]
        
    try:
        tools = json.loads(result_text)
        return tools
    except Exception as e:
        print(f"JSON Parse Error: {e}")
        print(result_text[:500])
        return []

files_to_process = [
    'data/pdfs-to-text/(V1)21 AI TOOLS MOST FORTUNE 500 TEAMS ARE TESTING IN 2026  ## What Large Organisations Are Deploying, Why, and Which Function Each One Serves-text.txt',
    'data/pdfs-to-text/The 2026 AI Tool Stack The Best AI Tools for Every Business Function (1) (1)-text.txt',
    'data/pdfs-to-text/V1_41 AI TOOLS REPLACING ENTIRE WORKFLOWS IN 2026 The Business Leader\'s Guide to Which AI Tools Cut the Most Time From Your Team\'s Workflows, and What the Work Looks Like After-text.txt'
]

total_tools = 0

for filepath in files_to_process:
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
        
    # Chunk the text if it's too large, but 30KB is fine for GPT-4o
    tools = extract_tools(text)
    
    for tool in tools:
        name = tool.get('name', 'Unknown Tool')
        desc = tool.get('description', '')
        content = tool.get('content', '')
        
        safe_name = clean_filename(name)
        if not safe_name: continue
        
        md_content = f"### Name\n{name}\n\n### Description\n{desc}\n\n### Content\n\n{content}\n\n### Category\nTools\n\n### Tags\n- Tool\n- Workflow\n"
        
        out_path = f"organized-data/Tools/{safe_name}.md"
        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.write(md_content)
        total_tools += 1

print(f"Successfully extracted {total_tools} AI Tools.")
