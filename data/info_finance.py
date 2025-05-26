import requests
import json

# URL de l'API
url = "https://www.info-financiere.gouv.fr/api/explore/v2.1/catalog/datasets/flux-amf-new-prod/records?select=*&limit=100"

try:
    # Faire une requête GET
    response = requests.get(url)
    response.raise_for_status()  # Lève une erreur si le code HTTP est 4xx ou 5xx

    # Convertir la réponse en JSON
    data = response.json()

    # Sauvegarder dans un fichier JSON local
    with open("data/amf_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Données sauvegardées dans 'amf_data.json' avec succès.")

except requests.exceptions.RequestException as e:
    print("Une erreur s'est produite lors de la requête API :", e)
