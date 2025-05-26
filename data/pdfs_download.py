import os
import json
import requests


with open("data/amf_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)


output_dir = "data/pdfs"
os.makedirs(output_dir, exist_ok=True)

for item in data.get("results", []):
    pdf_url = item.get("url_de_recuperation")
    if pdf_url:
        
        filename = os.path.basename(pdf_url)
        output_path = os.path.join(output_dir, filename)

        if not os.path.exists(output_path):
            try:
                print(f"Téléchargement de {filename} ...")
                response = requests.get(pdf_url)
                response.raise_for_status()
                with open(output_path, "wb") as pdf_file:
                    pdf_file.write(response.content)
                print(f"Enregistré : {output_path}")
            except Exception as e:
                print(f"Erreur pour {filename} : {e}")
        else:
            print(f"Déjà présent : {filename}")
