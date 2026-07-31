import os
import json

bookmarks = [
    {"name": "Hexta UI", "url": "https://www.hextaui.com/", "desc": "Extended Components & Blocks for shadcn/ui.", "cat": "Tools", "tags": ["UI", "Components", "shadcn"]},
    {"name": "21st.dev", "url": "https://21st.dev/community/components", "desc": "Discover community-made UI components.", "cat": "Resources", "tags": ["UI", "Community"]},
    {"name": "Taste Skill", "url": "https://www.tasteskill.dev/", "desc": "The Anti-Slop Frontend Framework for AI Agents.", "cat": "Frameworks", "tags": ["Frontend", "AI", "Design"]},
    {"name": "Hallmark", "url": "https://www.usehallmark.com/", "desc": "A design skill that refuses to look AI-generated.", "cat": "Tools", "tags": ["Design", "AI", "Skill"]},
    {"name": "Impeccable", "url": "https://impeccable.style/", "desc": "The missing upgrade to Anthropic's impeccable skill.", "cat": "Tools", "tags": ["Design", "Anthropic", "Skill"]},
    {"name": "AnimeJS", "url": "https://animejs.com/documentation/getting-started/", "desc": "Lightweight JavaScript animation library.", "cat": "Tools", "tags": ["Animation", "JavaScript", "Library"]},
    {"name": "Uiverse", "url": "https://uiverse.io/", "desc": "The Largest Library of Open-Source UI elements Animated.", "cat": "Resources", "tags": ["UI", "Animation", "Open Source"]},
    {"name": "Hover.dev", "url": "https://www.hover.dev/components", "desc": "Prebuilt UI animations and interactions for React, Tailwind CSS, Framer Motion.", "cat": "Tools", "tags": ["UI", "React", "Animation"]},
    {"name": "React Bits", "url": "https://reactbits.dev/", "desc": "Animated UI Components For React.", "cat": "Tools", "tags": ["UI", "React", "Animation"]},
    {"name": "Mobbin", "url": "https://mobbin.com/", "desc": "UI & UX design inspiration for mobile & web apps.", "cat": "Resources", "tags": ["Design", "Inspiration", "UI"]},
    {"name": "Landbook", "url": "https://land-book.com/", "desc": "Website design inspiration gallery.", "cat": "Resources", "tags": ["Design", "Inspiration", "Web"]},
    {"name": "Ideogram 4.0", "url": "https://ideogram.ai/models/4.0/", "desc": "Advanced AI image generation model.", "cat": "Tools", "tags": ["AI", "Images", "Generation"]},
    {"name": "Parker", "url": "https://heyparker.ai/", "desc": "AI tool for automation and productivity.", "cat": "Tools", "tags": ["AI", "Productivity"]},
    {"name": "Kokonut UI", "url": "https://kokonutui.com/", "desc": "Open Source UI Components.", "cat": "Tools", "tags": ["UI", "Open Source", "Components"]},
    {"name": "Motion.dev", "url": "https://motion.dev/", "desc": "JavaScript & React animation library.", "cat": "Tools", "tags": ["Animation", "JavaScript", "React"]},
    {"name": "Rive", "url": "https://rive.app/", "desc": "The interactive experience engine for fast, animated graphics.", "cat": "Tools", "tags": ["Animation", "Interactive", "Graphics"]},
    {"name": "MagicUI", "url": "https://magicui.design/docs/components", "desc": "React Components & Templates for beautiful web apps.", "cat": "Tools", "tags": ["UI", "React", "Templates"]},
    {"name": "Stitch", "url": "https://stitch.withgoogle.com/", "desc": "Design with AI by Google.", "cat": "Tools", "tags": ["Design", "AI", "Google"]},
    {"name": "here.now", "url": "https://here.now/", "desc": "Instant web hosting for AI agents.", "cat": "Tools", "tags": ["Hosting", "AI", "Agents"]},
    {"name": "Prism", "url": "https://prism.openai.com/", "desc": "AI LaTeX Editor by OpenAI.", "cat": "Tools", "tags": ["LaTeX", "Editor", "AI"]},
    {"name": "Hunyuan Video", "url": "https://www.hunyuanvideo.org/", "desc": "Free Online AI Video Generation Tool.", "cat": "Tools", "tags": ["AI", "Video", "Generation"]},
    {"name": "Z-Image AI", "url": "https://z-image.app/", "desc": "Free, Fast, Photorealistic AI Image Generator.", "cat": "Tools", "tags": ["AI", "Images", "Generation"]},
    {"name": "AI Tool Index", "url": "https://www.theaireport.ai/tools", "desc": "Directory to find the right AI tool by The AI Report.", "cat": "Resources", "tags": ["AI", "Directory", "Tools"]},
    {"name": "HubSpot Full-Stack AI Marketing Toolkit", "url": "https://docs.google.com/spreadsheets/d/1e25QKZ79GO7b5obA2DwB5W3I0Gflw3-unziCK2lWixA/edit", "desc": "Comprehensive marketing toolkit template on Google Sheets.", "cat": "Templates", "tags": ["Marketing", "AI", "Toolkit"]},
    {"name": "Marketing Against the Grain Newsletter Template", "url": "https://docs.google.com/spreadsheets/d/12cw8R1Ef45SkHLKp4ypKZLk5a3vi9hTtn1PqRdPztgw/edit", "desc": "Email newsletter setup template on Google Sheets.", "cat": "Templates", "tags": ["Newsletter", "Email", "Template"]},
    {"name": "Starter Story Data", "url": "https://www.starterstory.com/data", "desc": "Explore successful businesses, revenue metrics, and growth strategies.", "cat": "Resources", "tags": ["Business", "Startups", "Growth"]},
    {"name": "How to Create a Cold Email Generator Using AI", "url": "https://offers.hubspot.com/cold-email-using-ai", "desc": "Guide on creating personalized cold emails using AI.", "cat": "Guides", "tags": ["Email", "AI", "Sales"]},
    {"name": "Obsidian Is My AI's Second Brain", "url": "https://pear-diadem-016.notion.site/Obsidian-Is-My-AI-s-Second-Brain-Here-s-My-Full-Setup-33a4eefac3948167b640fcd0d83427c6", "desc": "Detailed guide on setting up Obsidian as an AI knowledge base.", "cat": "Guides", "tags": ["Obsidian", "Knowledge Base", "AI"]},
    {"name": "39 Claude Skills Examples", "url": "https://aiblewmymind.substack.com/p/claude-skills-36-examples", "desc": "Examples of Claude skills to transform workflows.", "cat": "Guides", "tags": ["Claude", "Skills", "Workflows"]},
    {"name": "How to Spot $100M+ Product Ideas", "url": "https://offers.hubspot.com/spot-100m-product-ideas", "desc": "The Eric Ryan Playbook on spotting massive product opportunities.", "cat": "Guides", "tags": ["Product", "Business", "Ideas"]},
    {"name": "$1M Attention", "url": "https://docs.google.com/document/d/1jZ3W0-JVXpHOG_SbjTuqD2kYPo5PRozCXFkUUqgxQlI/edit", "desc": "Guide on getting attention and building audience.", "cat": "Guides", "tags": ["Marketing", "Audience", "Growth"]},
    {"name": "The $1M Solopreneur MVP", "url": "https://docs.google.com/document/d/1zI2ya7sDv8ycXmOzPO_aOS8-dNEwDoow14q_rrs_aU4/edit", "desc": "Guide on building a minimal viable product for solopreneurs.", "cat": "Guides", "tags": ["MVP", "Solopreneur", "Business"]},
    {"name": "Build a Self-Updating LLM Knowledge Base", "url": "https://bholmes.dev/blog/llm-knowledge-bases/", "desc": "Tutorial on building an automated knowledge base.", "cat": "Guides", "tags": ["LLM", "Knowledge Base", "Tutorial"]},
    {"name": "Let AI Build Your First AI App", "url": "https://www.youtube.com/playlist?list=PLJrzt4ameiaOKxniCEH5RH-skejpcMXRq", "desc": "YouTube playlist guide for beginners on building AI apps.", "cat": "Guides", "tags": ["AI", "App", "YouTube", "Beginner"]},
    {"name": "How To Use Cursor AI To Build Software", "url": "https://www.youtube.com/playlist?list=PLJrzt4ameiaMxmOwTlxOy3eW37oZgAMIw", "desc": "Full YouTube guide on using Cursor AI.", "cat": "Guides", "tags": ["Cursor", "AI", "Software", "YouTube"]},
    {"name": "Mobile App Growth Cheat Sheet", "url": "https://offers.hubspot.com/view/mobile-app-growth", "desc": "Cheat sheet for mobile app marketing and growth.", "cat": "Cheat Sheets", "tags": ["Mobile", "App", "Growth", "Marketing"]}
]

os.makedirs('organized-data/Templates', exist_ok=True)
os.makedirs('organized-data/Cheat Sheets', exist_ok=True)

with open('organized-data/Templates/README.md', 'w') as f:
    f.write("# Templates\n\nThis folder contains structural templates, spreadsheets, and foundational documents meant to be duplicated and modified for personal use.\n")

with open('organized-data/Cheat Sheets/README.md', 'w') as f:
    f.write("# Cheat Sheets\n\nThis folder contains dense, quick-reference materials intended for rapid lookups rather than deep learning.\n")

def filename(name):
    return name.lower().replace(' ', '-').replace('/', '-').replace('$', '').replace('+', '').replace('+', '').replace('+', '').replace("'", '').replace('(', '').replace(')', '').replace('+', '').replace(',', '').replace('.', '').replace('&', '').replace(':', '') + '.md'

for b in bookmarks:
    content = f"### Name\n{b['name']}\n\n### Description\n{b['desc']}\n\n### URL\n{b['url']}\n\n### Category\n{b['cat']}\n\n### Tags\n"
    for tag in b['tags']:
        content += f"- {tag}\n"
    
    cat_folder = b['cat']
    filepath = f"organized-data/{cat_folder}/{filename(b['name'])}"
    
    with open(filepath, 'w') as f:
        f.write(content)

print("Bookmarks written.")
