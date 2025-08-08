import requests
import random
import time
import json
import os

# ---------- Configuration ----------
TOTAL_NEW_BOOKS = 1000
BOOKS_FILE = "books.json"
MAX_PAGES = 40
QUERY_LIST = ["the", "book", "story", "life", "world", "man", "woman", "dream", "journey", "time"]
SLEEP_TIME = 0.2
MAX_RETRIES = 3

# ---------- Load Existing Books ----------
if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        books = json.load(f)
        seen_ids = set(book["id"] for book in books)
    print(f"[INFO] Loaded {len(books)} existing books from {BOOKS_FILE}")
else:
    books = []
    seen_ids = set()
    print(f"[INFO] Starting fresh, no {BOOKS_FILE} found.")

# ---------- Helpers ----------
def safe_request(url):
    for _ in range(MAX_RETRIES):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                return res
            elif res.status_code >= 500:
                print(f"[WARN] Server error {res.status_code}, retrying...")
                time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Request failed: {e}")
        time.sleep(0.3)
    print(f"[ERROR] Failed after {MAX_RETRIES} retries: {url}")
    return None

def fetch_description(work_key):
    url = f"https://openlibrary.org{work_key}.json"
    res = safe_request(url)
    if not res:
        return None
    try:
        data = res.json()
        desc = data.get("description")
        if isinstance(desc, dict):
            return desc.get("value")
        elif isinstance(desc, str):
            return desc
    except Exception:
        return None
    return None

# ---------- Main Logic ----------
def fetch_random_books():
    added = 0
    while added < TOTAL_NEW_BOOKS:
        query = random.choice(QUERY_LIST)
        page = random.randint(1, MAX_PAGES)
        url = f"https://openlibrary.org/search.json?q={query}&page={page}"
        print(f"[INFO] Fetching query '{query}' from page {page}...")

        res = safe_request(url)
        if not res:
            continue

        try:
            data = res.json()
            docs = data.get("docs", [])
        except Exception:
            continue

        for doc in docs:
            work_key = doc.get("key")  # e.g., "/works/OL82563W"
            title = doc.get("title")

            if not work_key or not title:
                continue

            book_id = work_key.replace("/works/", "")
            if book_id in seen_ids:
                continue

            description = fetch_description(work_key)
            if description:
                books.append({
                    "id": book_id,
                    "title": title,
                    "description": description
                })
                seen_ids.add(book_id)
                added += 1
                print(f"[+] {len(books)} total ({added} new): {title}")

            if added >= TOTAL_NEW_BOOKS:
                break

        time.sleep(SLEEP_TIME)

# ---------- Run ----------
fetch_random_books()

# ---------- Save ----------
with open(BOOKS_FILE, "w", encoding="utf-8") as f:
    json.dump(books, f, indent=2, ensure_ascii=False)

print(f"\nSaved updated book list: {len(books)} total books in {BOOKS_FILE}")
