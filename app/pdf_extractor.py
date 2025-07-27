# app/pdf_extractor.py

import fitz  # PyMuPDF
import os
import json

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    font_stats = {}

    # Collect all text blocks with font sizes
    text_blocks = []
    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = round(span["size"], 1)
                    text = span["text"].strip()
                    if not text:
                        continue
                    key = (size, span["font"])
                    font_stats[key] = font_stats.get(key, 0) + 1
                    text_blocks.append({
                        "text": text,
                        "size": size,
                        "font": span["font"],
                        "page": page_number
                    })

    # Determine likely heading font sizes
    common_fonts = sorted(font_stats.items(), key=lambda x: -x[1])
    font_sizes = sorted(set(size for (size, _), _ in common_fonts), reverse=True)

    if len(font_sizes) < 3:
        font_sizes += [0] * (3 - len(font_sizes))  # padding

    h1_size, h2_size, h3_size = font_sizes[:3]

    # Extract title: largest text on page 1
    title = "Untitled Document"
    for block in text_blocks:
        if block["page"] == 1 and block["size"] == h1_size:
            title = block["text"]
            break

    # Extract outline
    outline = []
    for block in text_blocks:
        level = None
        if block["size"] == h1_size:
            level = "H1"
        elif block["size"] == h2_size:
            level = "H2"
        elif block["size"] == h3_size:
            level = "H3"
        if level:
            outline.append({
                "level": level,
                "text": block["text"],
                "page": block["page"]
            })

    return {"title": title, "outline": outline}

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            result = extract_outline_from_pdf(pdf_path)
            output_path = os.path.join(output_dir, file.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()
