import os
import json
import shutil
from bs4 import BeautifulSoup

HTML_FILE = "Atividades _ Diêgo Oliveira _ LinkedIn.html"
FILES_DIR = "Atividades _ Diêgo Oliveira _ LinkedIn_files"
IMAGES_DIR = "linkedin_images"
OUTPUT_JSON = "linkedin_posts.json"

os.makedirs(IMAGES_DIR, exist_ok=True)

with open(HTML_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")

def copy_local_image(src_path, index):
    try:
        ext = ".jpg"
        filename = f"post_image_{index}{ext}"
        src_full = os.path.join(FILES_DIR, src_path)
        dest_path = os.path.join(IMAGES_DIR, filename)
        shutil.copy(src_full, dest_path)
        return dest_path.replace("\\", "/")
    except Exception as e:
        print(f"Erro ao copiar imagem {src_path}: {e}")
        return None


spans = soup.find_all("span", attrs={"dir": "ltr"})
posts_data = []
pending_author = None
post_index = 0

for span in spans:
    text = span.get_text(separator="\n", strip=True)

    if len(text.split()) <= 4 and all(c.isalpha() or c.isspace() for c in text):
        author = text.split("\n")[0].strip()
        pending_author = author
        continue

    if pending_author and len(text.strip()) > 30:
        img_tag = span.find_parent().find_next("img")
        img_src = img_tag["src"] if img_tag and "src" in img_tag.attrs else None
        image_path = None

        if img_src and not img_src.startswith("http"):
            local_filename = os.path.basename(img_src)
            image_path = copy_local_image(local_filename, post_index)

        posts_data.append({
            "author": pending_author,
            "description": text,
            "image_path": image_path
        })
        pending_author = None
        post_index += 1

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=2)

print(f"{len(posts_data)} posts exportados com sucesso para '{OUTPUT_JSON}'")
