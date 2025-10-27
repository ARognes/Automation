import sys
import os
import subprocess
import shutil
import re
from tqdm import tqdm

# Optional: Clipboard support
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# Save outputs on Desktop instead of ~/.python/chatgpt_text
DEFAULT_OUTPUT_PREFIX = os.path.expanduser("~/Desktop")

def fast_split_text(text, max_chars=16000):
    total_chars = len(text)
    total_chunks = (total_chars + max_chars - 1) // max_chars

    print(f"\n📊 Splitting text into {total_chunks} chunks (~{max_chars} chars each)...")

    return [
        text[i:i + max_chars]
        for i in tqdm(range(0, total_chars, max_chars), total=total_chunks, desc="⏳ Chunking", unit="chunk")
    ]


def save_chunks_to_files(chunks, output_dir, base_filename):
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n💾 Saving {len(chunks)} chunks to folder: {output_dir}")

    for i, chunk in tqdm(enumerate(chunks, 1), total=len(chunks), desc="💾 Writing", unit="file"):
        filename = os.path.join(output_dir, f"{base_filename}_chunk_{i:02d}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(chunk)

    print("✅ All chunks saved!")


def extract_title(text):
    lines = text.strip().splitlines()
    for line in lines[:20]:
        if len(line.strip()) > 5 and line.strip() == line.strip().title():
            return re.sub(r'[^a-zA-Z0-9_-]', '_', line.strip())[:30]
    return "clipboard"


def resolve_output_folder(title, custom_prefix=None):
    if custom_prefix:
        return os.path.abspath(custom_prefix)
    return os.path.join(DEFAULT_OUTPUT_PREFIX, f"{title}_chunks")


def open_folder_in_finder(folder_path):
    try:
        subprocess.run(["open", folder_path], check=True)
        print(f"📂 Opened folder in Finder: {folder_path}")
    except Exception as e:
        print(f"⚠️  Could not open folder in Finder: {e}")


def play_beep(message="Done"):
    try:
        subprocess.run(["say", message], check=True)  # macOS voice feedback
    except:
        print("\a")  # fallback beep


if __name__ == "__main__":
    args = sys.argv[1:]

    no_open = '--no-open' in args
    from_clipboard = '--from-clipboard' in args or len(args) == 0

    # Clean up flags
    args = [arg for arg in args if arg not in ['--no-open', '--from-clipboard']]

    if from_clipboard:
        if not CLIPBOARD_AVAILABLE:
            print("❌ Clipboard support requires 'pyperclip'. Install with: pip install pyperclip")
            sys.exit(1)

        print("📋 Reading text from clipboard...")
        text = pyperclip.paste()
        if not text.strip():
            print("⚠️ Clipboard is empty!")
            sys.exit(1)

        title = extract_title(text)
        chunks = fast_split_text(text)
        output_folder = resolve_output_folder(title)
        save_chunks_to_files(chunks, output_folder, title)
        if not no_open:
            open_folder_in_finder(output_folder)
        play_beep(message=title)
        sys.exit(0)

    if not args:
        print("⚠️  Usage: python splitchunks.py <input_file or -> [output_folder] [--no-open] [--from-clipboard]")
        sys.exit(1)

    input_arg = args[0]
    if input_arg == "-":
        print("📥 Reading from stdin...")
        text = sys.stdin.read()
    else:
        if not os.path.isfile(input_arg):
            print(f"❌ Not a valid file: {input_arg}")
            sys.exit(1)
        with open(input_arg, "r", encoding="utf-8") as f:
            text = f.read()

    title = extract_title(text)
    output_folder = resolve_output_folder(title, args[1] if len(args) > 1 else None)
    chunks = fast_split_text(text)
    save_chunks_to_files(chunks, output_folder, title)

    if not no_open:
        open_folder_in_finder(output_folder)

    play_beep(message=title)
