from pathlib import Path

import pymupdf


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "data" / "pdf" / "2024-06-26 (16)_20240626125419.pdf"

with pymupdf.open(PDF_PATH) as document:
     print(f"File: {PDF_PATH.name}")
     print(f"Pages: {document.page_count}")

     for i in range(document.page_count):
        page = document[i]
        image = page.get_pixmap(dpi=300)

        output_path = PROJECT_ROOT / "data" / "images" / f"{PDF_PATH.stem}_page_{i+1:03d}.png"
        image.save(output_path)

        print(f"Image saved: {output_path}")
        print(f"Image size: {image.width} x {image.height} pixels")