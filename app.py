import json
import streamlit as st
import os
from PIL import Image, UnidentifiedImageError
import re

JSON_FILE = "linkedin_posts.json"


@st.cache_data
def load_posts():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

posts = load_posts()

st.title("🔍 Buscador de Posts do LinkedIn")
query = st.text_input("Digite uma palavra-chave para buscar na descrição:")


if query:
    results = [p for p in posts if query.lower() in p["description"].lower()]
    st.write(f"🔎 {len(results)} posts encontrados:")
    
    for post in results:
        hashtags = re.findall(r'hashtag\s*#\s*([^\n#]+)', post["description"], re.IGNORECASE)


        
        descricao_limpa = re.sub(r'hashtag\s*#\s*[^\n#]+', '', post["description"], flags=re.IGNORECASE)
        descricao_limpa = re.sub(r'\n+', '\n', descricao_limpa).strip()
        descricao_html = descricao_limpa.replace("\n", "<br>")
        st.markdown(f"**Autor:** {post['author']}")
        st.markdown(f"**Descrição:**<br>{descricao_html}", unsafe_allow_html=True)
        if hashtags:
            hashtag_str = " ".join([f"#{tag.strip()}" for tag in hashtags])
            st.markdown(f"**Hashtags:** {hashtag_str}")
        if post["image_path"] and os.path.exists(post["image_path"]):
            try:
                img = Image.open(post["image_path"])
                st.image(img, use_container_width=True)
            except UnidentifiedImageError:
                st.markdown("Imagem não carregada")
        st.markdown("---")

else:
    st.info("Digite uma palavra para iniciar a busca.")
