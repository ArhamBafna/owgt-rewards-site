# Rewards Website Plan (Refined)

> [!NOTE]
> All work, scripts, database, and website files will be located inside the `rewards/` directory.

## Goal
Build a plain HTML/CSS/JS website full of AI tools, prompts, guides, and links that looks premium and high-quality. Give this website as a "reward" to people who sign up for your newsletter. More rewards = more signups. 

## Where Me Get Data (Raw Material)
1. **Local Files & Local Code**: PDFs and text files in `rewards/` folder, local downloads folder, and system prompts/config files from local projects.
2. **Personal Accounts (Notion, YouTube, Browser, GitHub)**: Use Composio MCP to connect. 
   - **YouTube**: Saved AI videos from "AI/Tech" playlist + transcripts.
   - **Notion**: Page "system AI stack" (IDEs, CLIs, tools) + saved bookmarks.
   - **Browser Bookmarks**: Exported Chrome/Brave/Arc bookmark HTML files.
   - **GitHub Stars**: Starred repos related to AI tools, LLM frameworks, and awesome lists.
   - **AI Chat Histories / System Prompts**: Exported custom instructions or past prompts from ChatGPT/Claude/Cursor.
3. **Public Web & AI Aggregators**: Use Exa and Firecrawl to find tools on Futurepedia, Product Hunt, GitHub, and Hugging Face.
4. **Other Newsletters/Skool Communities**: Me search web for newsletters/Skool communities offering free resources. Me list them and ask you to sign up. Once you get resource, you give to me and me add to database.
5. **Autonomous AI Discovery Source**: Me pick one other separate source on my own and search there, or ask you if I cannot do it and source required human to find material.

## How Me Build Website (The Process & Suggested Models)

### Step 1: Data Hoarding & Resource Discovery (COMPLETED)
- **Local Files**: Converted 6 raw PDFs in `rewards/raw-pdfs` and moved them to `rewards/data/pdfs-to-text`.
- **YouTube Transcripts**: Fetched 21 items from "AI/Tech" playlist via Composio YouTube integration. Extracted full transcripts via `youtube-transcript-api` and saved individual `.txt` files in `rewards/data/youtube/`.
- **Notion AI Stack**: Extracted "System AI Stack" markdown page via Composio Notion integration and saved to `rewards/data/notion/`. (Note: Skipped sub-pages to maintain focus on the top-level list).
- **GitHub Repositories**: Searched web and curated top AI agent frameworks (CrewAI, AutoGen, LangChain, OpenManus, OpenClaw), production starter kits (awesome-llm-apps, llm-zoomcamp, composio), UI libraries (shadcn/ui), and awesome lists into `rewards/data/github.txt`.
- **Bookmarks**: Moved `bookmarks_7_31_26.html` to `rewards/data/bookmarks.html` and parsed 139 developer bookmarks (excluding personal projects) into `rewards/data/bookmarks/bookmarks_summary.txt`.
- **Newsletter & Skool Discovery**: Discovered top AI communities/newsletters (AI Launchpad, AI Builders Club, The AI Edge, AI Essentials, Ainsider) via Exa web search. Saved details to `rewards/data/communities/`. (Note: Skipped deep scraping because these require manual human signup/login).
- **Database Output**: Replaced single JSON file with a deep, human-readable subfolder structure in `rewards/data/`.


### Step 2: The UI Bake-Off (3 Landing Pages) (COMPLETED)
- You have 3 UI design skills.
- **STOP POINT**: Me ask you which 3 skills to use. Me NO PROCEED BEFORE ASKING.
- Once you tell me the 3 skills, me build **3 different landing pages** inside `rewards/skill-test-landing-page/` (using plain HTML/CSS/JS).
- You look. You pick the best one.
- **Suggested Model**: **Claude 3.5 Sonnet** or **Gemini 3.1 Pro** (best for high-aesthetic UI/UX and web layout design).

### Step 3: Build Full Website & Deploy
- Using the winning UI skill, me build the whole website inside `rewards/site/` (Plain HTML/CSS/JS with modern dynamic design).
- Add categories, search bar, tags, filter by source, and dynamic rendering of `rewards_db.json`.
- Me deploy it to Vercel so it is live on the internet.
- **Suggested Model**: **Claude 3.5 Sonnet** (for clean, bug-free frontend code) and **Gemini 3.6 Flash** (for rapid execution/deployment).
