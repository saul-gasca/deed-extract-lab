from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ANNOTATION_PATH = PROJECT_ROOT / "data" / "annotated" / "compraventa_4465_draft.json"

annotation = json.loads(ANNOTATION_PATH.read_text(encoding="utf-8"))


pdf_name = Path(annotation["source_file"])
OCR_PATH = PROJECT_ROOT / "data" / "ocr" / f"{pdf_name.stem}_ocr.txt"

ocr_text = OCR_PATH.read_text(encoding="utf-8")

for person in annotation["persons"]:
    name = person["name"]["value"]


    for field_name in ("name","role"):
        field = person[field_name]
        evidence = field["source_text"]

        found = bool(evidence.strip()) and evidence in ocr_text
        status = "FOUND" if found else "NOT FOUND"

        print(f"{name} | {field_name}: {status}")


for field_name, field in annotation["document"].items():
    evidence = field["source_text"]

    found = bool(evidence.strip()) and evidence in ocr_text
    status = "FOUND" if found else "NOT FOUND"

    print(f"Document | {field_name}: {status}")