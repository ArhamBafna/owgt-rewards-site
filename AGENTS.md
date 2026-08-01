# Rewards Directory Instructions

## Rules & Memory

- **Plan Updates**: All future plan updates and refinement changes MUST be made directly to `rewards/implementation_plan.md`. Do not create or update `spec.md`.

- **Location Isolation**: All work, scripts, database (`rewards/data/`), and website files (`rewards/site/` or `rewards/landing-options/`) must stay strictly inside the `rewards/` folder.

- **Tech Stack**: Website must be built using plain HTML/CSS/JS with modern dynamic aesthetics.

- **skool-guide-to-md skill**: `C:\Users\bafna\Desktop\Projects\OWGT-Newsletter-Automation\rewards\.agents\skool-guide-to-md\SKILL.md` - use when pastes text (usually a long guide for something) / roughly names the skill.

- **Phase Commits**: ALWAYS `git add`, `git commit -m "Phase X: ..."` and `git push` immediately upon completing each phase of `implementation_plan.md`.

- **Scripts Policy**: Prefer manual work over scripts where scripts might not work. If scripts almost guarenteed to work, create script (in scripts folder) carefully AFTER READING files the script will work on. Never rely solely on automated transformation scripts (they almost NEVER work). ALWAYS inspect changed/outputter files using `view_file` after script execution to that the right thing happened. If wrong occured, solve manually after script fails.
