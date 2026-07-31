import os
import re

def fix_filenames():
    # Fix Skool Guides -md.md
    guides_dir = 'c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/organized-data/Guides'
    for f in os.listdir(guides_dir):
        if f.endswith('-md.md'):
            new_f = f.replace('-md.md', '.md')
            os.rename(os.path.join(guides_dir, f), os.path.join(guides_dir, new_f))
            print(f"Renamed {f} to {new_f}")

    # Fix Mangled Skills
    skills_dir = 'c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/organized-data/Learning'
    mangled_map = {
        'aiethics-and.md': 'ai-ethics-and-governance-awareness.md',
        'aipresentation.md': 'ai-presentation-and-document-production.md',
        'aivideo-and-visual-content.md': 'ai-video-and-visual-content.md',
        'ai-powered-processdocumentation.md': 'ai-powered-process-documentation.md'
    }
    
    title_map = {
        'ai-ethics-and-governance-awareness.md': 'AI Ethics and Governance Awareness',
        'ai-presentation-and-document-production.md': 'AI Presentation and Document Production',
        'ai-video-and-visual-content.md': 'AI Video and Visual Content',
        'ai-powered-process-documentation.md': 'AI-Powered Process Documentation'
    }

    for f in os.listdir(skills_dir):
        if f in mangled_map:
            new_f = mangled_map[f]
            old_path = os.path.join(skills_dir, f)
            new_path = os.path.join(skills_dir, new_f)
            os.rename(old_path, new_path)
            print(f"Renamed {f} to {new_f}")
            
            # Fix Title inside the file
            with open(new_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            correct_title = title_map[new_f]
            content = re.sub(r'### Name\n.*?\n', f'### Name\n{correct_title}\n', content)
            
            with open(new_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Fixed content for {new_f}")

if __name__ == '__main__':
    fix_filenames()
