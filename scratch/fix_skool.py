import os
import glob
import re
import shutil

source_dir = 'data/skool-communites/guides'
dest_dir = 'organized-data/Guides'
os.makedirs(dest_dir, exist_ok=True)

# Delete the old ones that were badly generated just to be clean
old_files = glob.glob("organized-data/Guides/*.md")
for f in old_files:
    if os.path.basename(f) in [
        'avoid-chat-limits.md', 'Build-$10,000-Websites-with-AI.md',
        'Build-3-AI-Agents-in-Base44.md', 'build-an-award-worthy-f1-landing-page.md',
        'Build-Insane-Animated-Websites.md', 'Motion-Graphics-in-AI.md',
        'Raw-Footage-to-Finished-Video-in-AI.md', 'Top-AI-Courses-for-Beginners.md'
    ]:
        os.remove(f)

descriptions = {
    'avoid-chat-limits.md': 'Learn how to avoid context rot and chat limits by editing messages, batching requests, and starting fresh chats often.',
    'Build-$10,000-Websites-with-AI.md': 'A guide on using AI Opus 5 and the Higgsfield MCP connector to build a fully animated luxury real estate marketing site.',
    'Build-3-AI-Agents-in-Base44.md': 'A complete prompt pack and setup guide for building 3 AI superagents (Inbox, Publisher, Analyst) in Base44.',
    'build-an-award-worthy-f1-landing-page.md': 'Step-by-step instructions for using AI Web Builder and AI Media Generator to scaffold a premium Formula 1 landing page with cinematic visuals.',
    'Build-Insane-Animated-Websites.md': 'A full setup guide for connecting Higgsfield MCP to your AI to generate custom visual assets and iterative feedback for animated websites.',
    'Motion-Graphics-in-AI.md': 'A 3-step workflow for creating custom, high-quality motion graphics directly inside your AI workspace using an MCP connector.',
    'Raw-Footage-to-Finished-Video-in-AI.md': 'An AI setup guide utilizing open-source tools and HyperFrames to automatically edit, score, and caption raw video footage without Premiere.',
    'Top-AI-Courses-for-Beginners.md': 'A curated list of foundational AI and Machine Learning courses from top platforms, ideal for absolute beginners wanting to learn generative AI and ethics.'
}

files = glob.glob(f"{source_dir}/*.md")

for filepath in files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        
    name = filename.replace('.md', '').replace('-', ' ').title()
    desc = descriptions.get(filename, "A comprehensive AI guide from Skool community.")
    
    # Check if file has # Title, we might want to strip it to avoid duplicate titles
    lines = content.split('\n')
    if lines[0].startswith('# '):
        name = lines[0].replace('# ', '').strip()
        content = '\n'.join(lines[1:]).strip()
        
    new_content = f"### Name\n{name}\n\n### Description\n{desc}\n\n### Content\n\n{content}\n\n### Category\nGuides\n\n### Tags\n- Skool\n- Community\n- Guide\n"
    
    # We will save them with a safe filename
    safe_name = filename.lower()
    safe_name = re.sub(r'[^a-z0-9\-]', '-', safe_name)
    safe_name = re.sub(r'-+', '-', safe_name).strip('-')
    
    dest_path = os.path.join(dest_dir, f"{safe_name}.md")
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

print(f"Reprocessed {len(files)} skool guides accurately.")
