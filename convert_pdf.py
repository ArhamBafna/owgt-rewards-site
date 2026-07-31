import re
from pathlib import Path

def sanitize_filename(name):
    clean = re.sub(r'[\\/*?:"<>|]', "", name)
    clean = clean.strip()
    return clean

def clean_text_formatting(text):
    # Fix single-character spacing artifact (e.g. 'c o v e r i n g' -> 'covering')
    lines = []
    for line in text.splitlines():
        cleaned = re.sub(r'(?<=\b[A-Za-z0-9])\s+(?=[A-Za-z0-9]\b)', '', line)
        lines.append(cleaned)
    return "\n".join(lines)

def extract_pdf_text(pdf_path):
    # Pure PyMuPDF text extraction (lightweight & fast, no OCR)
    try:
        import fitz
        doc = fitz.open(pdf_path)
        text_content = []
        for page in doc:
            t = page.get_text()
            if t and t.strip():
                text_content.append(t)
        
        raw_text = "\n\n".join(text_content).strip()
        if raw_text:
            return clean_text_formatting(raw_text)

    except Exception as e:
        print(f"Error reading {pdf_path.name}: {e}")

    return ""

def main():
    rewards_dir = Path(__file__).parent
    raw_pdfs_dir = rewards_dir / "raw-pdfs"

    pdf_files = list(raw_pdfs_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in raw-pdfs.")
        return

    output_dir = rewards_dir / "data" / "pdfs-to-text"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Found {len(pdf_files)} PDFs to process in {raw_pdfs_dir.name}...")

    for pdf_path in pdf_files:
        safe_stem = sanitize_filename(pdf_path.stem)
        output_file = output_dir / f"{safe_stem}-text.txt"

        print(f"Processing: {pdf_path.name}")
        full_text = extract_pdf_text(pdf_path)

        if full_text:
            output_file.write_text(full_text, encoding="utf-8")
            print(f"  -> Successfully saved: {output_file.name} ({len(full_text.split())} words)")
        else:
            print(f"  -> WARNING: No direct text extracted from {pdf_path.name}")

    print("\nAll PDFs processed successfully!")

if __name__ == "__main__":
    main()
