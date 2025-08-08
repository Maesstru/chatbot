import json
import re

INPUT_FILE = "books.json"
OUTPUT_FILE = "books_cleaned.json"

def is_valid_description(desc):
    if not desc or not isinstance(desc, str):
        return False
    desc = desc.strip().lower()

    # Too short or clearly a metadata string
    if len(desc) < 30:
        return False

    # Common metadata patterns to reject
    patterns = [
        r"\d+ pages", 
        r"cm$", 
        r"isbn", 
        r"edition", 
        r"volume \d+",
        r"includes bibliographical references"
    ]

    for pattern in patterns:
        if re.search(pattern, desc):
            return False

    return True

# Load books
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    books = json.load(f)

# Filter valid books
cleaned_books = [
    book for book in books
    if is_valid_description(book.get("description"))
]

# Save cleaned books
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_books, f, indent=2, ensure_ascii=False)

print(f"✅ Cleaned list saved: {len(cleaned_books)} valid books in {OUTPUT_FILE}")
