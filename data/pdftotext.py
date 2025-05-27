import os
import fitz  # PyMuPDF

def pdftotxt(pdf_file, output_dir="extracted_texts", save_to_txt=False):
    
    if not pdf_file.lower().endswith(".pdf"):
        raise ValueError("Le fichier fourni n'est pas un PDF.")

    try:
        doc = fitz.open(pdf_file)
        full_text = ""
        for page in doc:
            full_text += page.get_text()

        if save_to_txt:
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.basename(pdf_file).replace(".pdf", ".txt")
            output_path = os.path.join(output_dir, base_name)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"Texte extrait et sauvegardé dans : {output_path}")

        return full_text

    except Exception as e:
        print(f"Erreur lors de la lecture de {pdf_file} : {e}")
        return ""