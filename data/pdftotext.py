import os
import fitz  # PyMuPDF

# Répertoire contenant les fichiers PDF
pdf_dir = "pdfs"  # ou adapte selon ton projet
output_dir = "extracted_texts"
os.makedirs(output_dir, exist_ok=True)

for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, pdf_file)
        output_path = os.path.join(output_dir, pdf_file.replace(".pdf", ".txt"))

        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text()

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            
            print(f"Texte extrait : {pdf_file}")
        except Exception as e:
            print(f"Erreur avec {pdf_file} : {e}")
