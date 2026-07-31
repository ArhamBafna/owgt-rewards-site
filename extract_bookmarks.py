import os

bookmarks = [
    {"name": "freedom.to", "description": "Block Websites, Apps, and the Internet", "url": "https://freedom.to/", "category": "Tools", "tags": "Focus, Productivity, App Blocker"},
    {"name": "Lando Norris", "description": "Formula 1 Driver Website for UI Inspiration", "url": "https://landonorris.com/", "category": "Resources", "tags": "UI Inspiration, Web Design"},
    {"name": "OFF+BRAND", "description": "Global Creative & Technology Studio for UI Inspiration", "url": "https://www.itsoffbrand.com/", "category": "Resources", "tags": "UI Inspiration, Web Design, Studio"},
    {"name": "awesome-design-md", "description": "A collection of DESIGN.md files analysis by popular agents", "url": "https://github.com/voltagent/awesome-design-md", "category": "Resources", "tags": "Design, AI Agents, GitHub"},
    {"name": "AI Quests", "description": "Google AI Quests and Research", "url": "https://research.google/ai-quests/intl/en_us", "category": "Resources", "tags": "AI Research, Quests"},
    {"name": "Every", "description": "Newsletter and publication covering productivity, AI, and business", "url": "https://every.to/", "category": "Resources", "tags": "Newsletter, Business, AI"},
    {"name": "Backgrounds Library", "description": "Figma Super Visuals Backgrounds Library", "url": "https://www.figma.com/design/1RjQY50dy7t9SucZtAIb1p/Super-Visuals--Backgrounds-Library", "category": "Resources", "tags": "Figma, Design, Backgrounds"},
    {"name": "Yupp", "description": "AI-powered creative legacy and tools", "url": "https://yupp.ai/", "category": "Tools", "tags": "AI Tools, Creative"},
    {"name": "Igloo Inc.", "description": "Web3 and NFT community building tools", "url": "https://www.igloo.inc/", "category": "Tools", "tags": "Web3, Community"},
    {"name": "Dropbox Brand Guidelines", "description": "Dropbox official brand guidelines for inspiration", "url": "https://brand.dropbox.com/", "category": "Resources", "tags": "Brand Guidelines, Design, Inspiration"},
    {"name": "Hour of AI Activities", "description": "Activities for the Hour of AI literacy program", "url": "https://csforall.org/en-US/activities/hour-of-ai", "category": "Resources", "tags": "Education, AI Literacy, Activities"},
    {"name": "AI Hackathons", "description": "Directory of upcoming AI hackathons by lablab.ai", "url": "https://lablab.ai/ai-hackathons", "category": "Resources", "tags": "Hackathons, AI, Events"},
    {"name": "Opal Experiment", "description": "Google Opal Experiment landing page", "url": "https://opal.google/landing/", "category": "Tools", "tags": "Google, Experiment, AI Tools"},
    {"name": "Google AI Flow", "description": "Google Labs FX Tools Flow", "url": "https://labs.google/fx/tools/flow", "category": "Tools", "tags": "Google Labs, Workflow, AI Tools"},
    {"name": "Corbin Skool", "description": "AI for Your Business Skool Community", "url": "https://www.skool.com/ai-for-your-business", "category": "Resources", "tags": "Community, Skool, Business AI"},
    {"name": "How to Hire an AI Email Marketer", "description": "Maven course on hiring an AI email marketer", "url": "https://maven.com/p/9763a4/how-to-hire-an-ai-email-marketer", "category": "Learning", "tags": "Email Marketing, Course, Hiring"},
    {"name": "Cold Email: How to Write Like a Human", "description": "Maven course on writing human-like cold emails", "url": "https://maven.com/p/8a65ef/cold-email-how-to-write-like-a-human", "category": "Learning", "tags": "Cold Email, Course, Writing"},
    {"name": "Zapier MCP", "description": "Model Context Protocol servers for Zapier", "url": "https://mcp.zapier.com/mcp/servers/720c0233-782a-415b-ac2c-f2384b689acc/config", "category": "Tools", "tags": "Zapier, MCP, Automation"},
    {"name": "dotagents", "description": "One location for all of your hooks, commands, skills, and agents", "url": "https://github.com/iannuttall/dotagents", "category": "Resources", "tags": "GitHub, Agents, Skills"},
    {"name": "RSS Post to Message", "description": "Relay.app template for posting RSS to a message", "url": "https://run.relay.app/shared/rss-post-to-message-CxdkjGBKGCJF", "category": "Tools", "tags": "Automation, RSS, Relay.app"},
    {"name": "Claude STARTUP Skill", "description": "Claude STARTUP skill on GitHub", "url": "https://github.com/ferdinandobons/startup-skill", "category": "Resources", "tags": "Claude, Skills, GitHub"},
    {"name": "Obsidian Is My AIs Second Brain", "description": "Notion setup guide for using Obsidian as an AI second brain", "url": "https://pear-diadem-016.notion.site/Obsidian-Is-My-AI-s-Second-Brain-Here-s-My-Full-Setup-33a4eefac3948167b640fcd0d83427c6", "category": "Guides", "tags": "Obsidian, Notion, Second Brain, Workflow"},
    {"name": "Zapier SDK Quickstart", "description": "Quickstart documentation for the Zapier SDK", "url": "https://docs.zapier.com/sdk/quickstart", "category": "Guides", "tags": "Zapier, SDK, Developer Docs"},
    {"name": "Reddit Communities to Promote Your App", "description": "Google Docs list of Reddit communities to promote your app for free", "url": "https://docs.google.com/document/d/1_sICGnI98lYlFGUedXFx8PJHldGDLWvjejiiz17vins/edit", "category": "Resources", "tags": "Reddit, Marketing, Promotion"},
    {"name": "GitHub Student Developer Pack", "description": "GitHub Student Developer Pack and offers", "url": "https://education.github.com/pack", "category": "Resources", "tags": "GitHub, Student, Developer Tools"},
    {"name": "Requests for Startups YC", "description": "Y Combinator Requests for Startups", "url": "https://www.ycombinator.com/rfs", "category": "Resources", "tags": "Y Combinator, Startups, Ideas"},
    {"name": "OpenClaw after 50 days", "description": "All prompts for 20 real workflows", "url": "https://gist.github.com/velvet-shark/b4c6724c391f612c4de4e9a07b0a74b6", "category": "Resources", "tags": "Prompts, Workflows, GitHub Gist"},
    {"name": "Claude Skills", "description": "Google Drive folder with Claude Skills", "url": "https://drive.google.com/drive/folders/1lhFm0v6ppm04daPMI3a5vrIcpBMo5uKP", "category": "Resources", "tags": "Claude, Skills, Google Drive"},
    {"name": "AI Tools Directory AIxploria", "description": "List of Best Free AI by Category", "url": "https://www.aixploria.com/en/", "category": "Resources", "tags": "AI Tools, Directory"},
    {"name": "ToolFK Online Tools", "description": "All in one online tools collection", "url": "https://www.toolfk.com/", "category": "Resources", "tags": "Tools, Directory"},
    {"name": "What AI Can Do Today", "description": "Directory of what AI can do today", "url": "https://whataicandotoday.com/", "category": "Resources", "tags": "AI Capabilities, Directory"},
    {"name": "10015 Tools", "description": "All Online Tools in One Box", "url": "https://10015.io/", "category": "Resources", "tags": "Tools, Directory"},
    {"name": "Banana Prompts", "description": "AI Image & Video Prompts directory", "url": "https://www.bananaprompts.xyz/", "category": "Resources", "tags": "Prompts, Image Generation, Video Generation"},
    {"name": "How to Spot 100M Product Ideas", "description": "The Eric Ryan Playbook on spotting 100M+ product ideas", "url": "https://53.fs1.hubspotusercontent-na1.net/hubfs/53/The%20Eric%20Ryan%20Playbook_%20How%20to%20Spot%20$100M+%20Product%20Ideas.pdf", "category": "Guides", "tags": "Product Ideas, Playbook, Business"},
    {"name": "1M Attention", "description": "Google Docs guide on getting attention", "url": "https://docs.google.com/document/d/1jZ3W0-JVXpHOG_SbjTuqD2kYPo5PRozCXFkUUqgxQlI/edit", "category": "Guides", "tags": "Marketing, Attention, Guide"},
    {"name": "Build a Self-Updating LLM Knowledge Base", "description": "Blog post on building a self-updating LLM knowledge base", "url": "https://bholmes.dev/blog/llm-knowledge-bases/", "category": "Guides", "tags": "LLM, Knowledge Base, Tutorial"},
    {"name": "emilkowalski skills", "description": "Skills for Design Engineers", "url": "https://github.com/emilkowalski/skills", "category": "Resources", "tags": "Design Engineering, Skills, GitHub"},
    {"name": "Cuelume", "description": "Interaction sounds for the web", "url": "https://cuelume-site.pages.dev/", "category": "Resources", "tags": "UI Sounds, Web Audio, Interactions"},
    {"name": "The AI Agent Playbook", "description": "Open Residency x AI with Remy playbook", "url": "https://drive.google.com/file/d/1oLaezBP36RA7X0vG9y3T8nuuDHf4qvbE/view", "category": "Guides", "tags": "AI Agents, Playbook"},
    {"name": "39 Claude Skills Examples", "description": "Examples from 23 Creators to Transform How You Work", "url": "https://aiblewmymind.substack.com/p/claude-skills-36-examples", "category": "Resources", "tags": "Claude, Skills, Substack"},
    {"name": "The Claude Skills That Finally Made AI Write Like Me", "description": "How to Build Yours by Substack creator", "url": "https://aiblewmymind.substack.com/p/claude-skills-ai-write-like-you", "category": "Resources", "tags": "Claude, Writing, Skills"},
    {"name": "openai-oauth", "description": "Free AI with your ChatGPT account", "url": "https://github.com/EvanZhouDev/openai-oauth", "category": "Tools", "tags": "OpenAI, OAuth, GitHub"},
    {"name": "frontend-textbooks", "description": "A coding-agent skill for generating designed HTML", "url": "https://github.com/onepixelaway/frontend-textbooks", "category": "Resources", "tags": "Frontend, AI Agents, Skills"},
    {"name": "List of free AI Models", "description": "DEV Community list of free AI models", "url": "https://dev.to/sbalasa/list-of-ai-models-17on", "category": "Resources", "tags": "AI Models, Free, DEV Community"},
    {"name": "How to Access Multiple Free AI Models at Once", "description": "Make Community guide on accessing multiple free AI models", "url": "https://community.make.com/t/how-to-access-multiple-free-ai-models-at-once/40751", "category": "Guides", "tags": "AI Models, Make, Guide"},
    {"name": "Namecheap Education Program", "description": "Free Domains for Students", "url": "https://nc.me/order", "category": "Resources", "tags": "Domains, Education, Students"},
    {"name": "Name.com Free Domain", "description": "Free Domain for Students on Name.com", "url": "https://www.name.com/github-students", "category": "Resources", "tags": "Domains, Education, Students"},
    {"name": "What Is Vibe Coding", "description": "The Term Was Coined Using Superwhisper", "url": "https://superwhisper.com/vibe-coding", "category": "Learning", "tags": "Vibe Coding, Programming"},
    {"name": "kolejain.com resources", "description": "Collection of resources on kolejain.com", "url": "https://www.kolejain.com/resources", "category": "Resources", "tags": "Resources, Collection"},
    {"name": "The 1M Solopreneur MVP", "description": "Google Docs guide for solopreneur MVP", "url": "https://docs.google.com/document/d/1zI2ya7sDv8ycXmOzPO_aOS8-dNEwDoow14q_rrs_aU4/edit", "category": "Guides", "tags": "Solopreneur, MVP, Business"},
    {"name": "Free Trial and Free Tier Services Google Cloud", "description": "Google Cloud free tier services and products", "url": "https://cloud.google.com/free", "category": "Resources", "tags": "Google Cloud, Free Tier, Hosting"},
    {"name": "Cloudflare Drop", "description": "Cloudflare Drop service", "url": "https://www.cloudflare.com/drop/", "category": "Resources", "tags": "Cloudflare, Infrastructure"},
]

def slugify(s):
    import re
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s)
    return s

for bm in bookmarks:
    filename = slugify(bm["name"]) + ".md"
    filepath = os.path.join("organized-data", bm["category"], filename)
    
    tags = "".join([f"- {t.strip()}\n" for t in bm["tags"].split(",")])
    
    content = f"### Name\n{bm['name']}\n\n### Description\n{bm['description']}\n\n### URL\n{bm['url']}\n\n### Category\n{bm['category']}\n\n### Tags\n{tags}"
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Created {len(bookmarks)} bookmark files.")
