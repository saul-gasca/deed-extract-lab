from pathlib import Path
from dotenv import load_dotenv
import os

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

import json
from datetime import datetime, timezone

import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ENV_PATH = PROJECT_ROOT / ".env"

PDF_PATH = PROJECT_ROOT / "data" / "pdf" / "2024-06-26 (16)_20240626125419.pdf"

#PDF_PATH = PROJECT_ROOT / "data" / "pdf" / "2024-06-04 (29)_20240604135514.pdf"

OUTPUT_PATH = PROJECT_ROOT / "data" / "ocr" / f"{PDF_PATH.stem}_ocr.txt"
METADATA_PATH = OUTPUT_PATH.with_suffix(".metadata.json")

if OUTPUT_PATH.is_file():
    existing_text = OUTPUT_PATH.read_text(encoding="utf-8")

    if existing_text.strip():
        print(f"Using existing OCR: {OUTPUT_PATH.name}")
        print(f"Characters extracted: {len(existing_text)}")

        if not METADATA_PATH.is_file():
            print("Metadata file is missing for this previous extraction.")

        sys.exit(0)

if not ENV_PATH.is_file():
    raise FileNotFoundError("Missing .env file in the project root.")


load_dotenv(ENV_PATH)

endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
api_key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

if not endpoint or not endpoint.strip():
    raise ValueError("Missing AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT.")

if not api_key or not api_key.strip():
    raise ValueError("Missing AZURE_DOCUMENT_INTELLIGENCE_KEY.")

endpoint = endpoint.strip()
api_key = api_key.strip()

print("Azure OCR configuration loaded successfully.")

client = DocumentIntelligenceClient(endpoint=endpoint,credential=AzureKeyCredential(api_key))

print("Azure Document Intelligence client created.")

print("Sending PDF to Azure OCR. Analyzing all pages...")

with PDF_PATH.open("rb") as pdf_file:

    poller = client.begin_analyze_document(
        model_id='prebuilt-read',
        body=pdf_file,
        #pages="1"
    )

    result = poller.result()


print(f"Pages analyzed: {len(result.pages)}")
print(f"Characters extracted: {len(result.content)}")
print("\nText preview:")
print(result.content[:500])

#OUTPUT_PATH = PROJECT_ROOT / "data" / "ocr" / f"{PDF_PATH.stem}_page_001_ocr.txt"

#OUTPUT_PATH = PROJECT_ROOT / "data" / "ocr" / f"{PDF_PATH.stem}_ocr.txt"

OUTPUT_PATH.write_text(result.content,encoding="utf-8")

print(f"OCR text saved: {OUTPUT_PATH}")


metadata = {
    "source_file": PDF_PATH.name,
    "ocr_provider": "azure-document-intelligence",
    "model_id": result.model_id,
    "api_version": result.api_version,
    "ocr_version": "azure-read-v1",
    "pages_analyzed": len(result.pages),
    "characters_extracted": len(result.content),
    "processed_at": datetime.now(timezone.utc).isoformat(),
}

#METADATA_PATH = OUTPUT_PATH.with_suffix(".metadata.json")

METADATA_PATH.write_text(
    json.dumps(metadata, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print(f"OCR metadata saved: {METADATA_PATH}")
