import os
import shutil
import re

# ─────────────────────────────────────────────────────────────────────────────
# SUB-TASK A — Move all .jpg files from a folder to a new folder
# ─────────────────────────────────────────────────────────────────────────────

def move_jpg_files():
    print("\n" + "=" * 50)
    print("  📁 MOVE .JPG FILES")
    print("=" * 50)

    source = input("  Enter source folder path: ").strip()
    if not os.path.isdir(source):
        print(f"  ❌ Source folder '{source}' does not exist.")
        return

    destination = input("  Enter destination folder path (will be created if needed): ").strip()
    os.makedirs(destination, exist_ok=True)

    jpg_files = [f for f in os.listdir(source)
                 if f.lower().endswith(".jpg") and os.path.isfile(os.path.join(source, f))]

    if not jpg_files:
        print("  ⚠  No .jpg files found in the source folder.")
        return

    moved = 0
    for filename in jpg_files:
        src_path  = os.path.join(source, filename)
        dest_path = os.path.join(destination, filename)

        # Avoid overwriting — append a counter if the file already exists
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(destination, f"{base}_{counter}{ext}")):
                counter += 1
            dest_path = os.path.join(destination, f"{base}_{counter}{ext}")

        shutil.move(src_path, dest_path)
        print(f"  ✅ Moved: {filename}")
        moved += 1

    print(f"\n  🎉 Done! Moved {moved} .jpg file(s) to '{destination}'")


# ─────────────────────────────────────────────────────────────────────────────
# SUB-TASK B — Extract all email addresses from a .txt file
# ─────────────────────────────────────────────────────────────────────────────

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")


def extract_emails():
    print("\n" + "=" * 50)
    print("  📧 EXTRACT EMAIL ADDRESSES")
    print("=" * 50)

    input_file = input("  Enter path to the input .txt file: ").strip()
    if not os.path.isfile(input_file):
        print(f"  ❌ File '{input_file}' not found.")
        return

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    emails = sorted(set(EMAIL_PATTERN.findall(content)))  # unique + sorted

    if not emails:
        print("  ⚠  No email addresses found in the file.")
        return

    output_file = input("  Enter path for the output file (e.g., emails.txt): ").strip()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Emails extracted from: {input_file}\n")
        f.write(f"Total found: {len(emails)}\n")
        f.write("=" * 40 + "\n")
        for email in emails:
            f.write(email + "\n")

    print(f"\n  🎉 Done! Found {len(emails)} unique email(s). Saved to '{output_file}'")
    print("  Preview (first 5):")
    for email in emails[:5]:
        print(f"    • {email}")


# ─────────────────────────────────────────────────────────────────────────────
# SUB-TASK C — Scrape the title of a fixed webpage and save it
# ─────────────────────────────────────────────────────────────────────────────

def scrape_webpage_title():
    print("\n" + "=" * 50)
    print("  🌐 SCRAPE WEBPAGE TITLE")
    print("=" * 50)

    try:
        import urllib.request
        from html.parser import HTMLParser
    except ImportError:
        print("  ❌ Required modules not available.")
        return

    class TitleParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self._in_title = False
            self.title = ""

        def handle_starttag(self, tag, attrs):
            if tag.lower() == "title":
                self._in_title = True

        def handle_data(self, data):
            if self._in_title:
                self.title += data

        def handle_endtag(self, tag):
            if tag.lower() == "title":
                self._in_title = False

    url = input("  Enter the webpage URL (e.g., https://example.com): ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"  Fetching '{url}' ...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  ❌ Could not fetch page: {e}")
        return

    parser = TitleParser()
    parser.feed(html)
    title = parser.title.strip() or "(No title found)"

    print(f"\n  📄 Page Title: {title}")

    output_file = input("  Save to file? Enter filename (or press Enter to skip): ").strip()
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"URL   : {url}\n")
            f.write(f"Title : {title}\n")
        print(f"  💾 Saved to '{output_file}'")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────────────────────

def main():
    while True:
        print("\n" + "=" * 50)
        print("      🤖 TASK AUTOMATION SCRIPTS")
        print("=" * 50)
        print("  1. Move .jpg files to a new folder")
        print("  2. Extract email addresses from a .txt file")
        print("  3. Scrape webpage title and save it")
        print("  4. Exit")
        print("=" * 50)

        choice = input("  Choose an option (1-4): ").strip()
        if choice == "1":
            move_jpg_files()
        elif choice == "2":
            extract_emails()
        elif choice == "3":
            scrape_webpage_title()
        elif choice == "4":
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("  ⚠  Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
