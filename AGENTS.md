# Rewards Directory Instructions

- **Architecture**: `data` folder contains raw data. `organized-data` folder contains that but organized for easy website building. `site` contains all website.

- **Tech Stack**: Website must be built using plain HTML/CSS/JS with modern dynamic aesthetics.

- **skool-guide-to-md skill**: `C:\Users\bafna\Desktop\Projects\OWGT-Newsletter-Automation\rewards\.agents\skool-guide-to-md\SKILL.md` - use when pastes text (usually a long guide for something) and roughly names the skill.

- **Scripts Policy**: Prefer manual work > scripts where scripts might not work. If scripts almost guarenteed to work, create script (in scripts folder) carefully AFTER READING files the script will work on. Never rely solely on automated transformation scripts (they almost NEVER work). ALWAYS inspect changed/outputted files using `view_file` after script execution to make sure the right thing happened. If wrong occured, solve manually after script fails. ANYTIME YOU CREATE ONE-TIME SCRIPT, DELETE AFTER USE.

- **Running Locally**: When asked to run or preview the site locally, ALWAYS run `python scripts/serve.py` from the `rewards/` directory (NOT `python -m http.server`). Vercel uses clean URLs (`/rewards`, `/items/bundles/...` without `.html`), and `scripts/serve.py` automatically handles these clean URLs so pages and links do not 404.