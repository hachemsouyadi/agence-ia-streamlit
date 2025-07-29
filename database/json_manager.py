import json

class JSONManager:
    def __init__(self, filename="data.json"):
        self.filename = filename

    def enregistrer(self, data):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("Erreur d'enregistrement :", e)

    def charger(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            print("Erreur de chargement :", e)
            return []
