import json
from pathlib import Path
from jsonschema import validate, ValidationError

def load_schema(version):
    """Charge le schéma JSON correspondant à la version"""
    schema_path = Path(__file__).parent.parent / "json_struct" / f"ror_schema_v{version}.json"
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def detect_ror_version(json_file_path):
    """Détecte la version ROR d'un fichier JSON"""
    try:
        # Charger les schémas
        schema_v1 = load_schema("1")
        schema_v2_0 = load_schema("2_0")
        schema_v2_1 = load_schema("2_1")
        
        # Charger le fichier à analyser avec encodage UTF-8
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Tester d'abord la version la plus récente (2.1)
        try:
            validate(data, schema_v2_1)
            return "2.1"
        except ValidationError:
            try:
                validate(data, schema_v2_0)
                return "2.0"
            except ValidationError:
                validate(data, schema_v1)  # Si échec, lève une exception
                return "1.0"
                
    except FileNotFoundError as e:
        print(f"Erreur: Fichier non trouvé - {e.filename}")
        return None
    except json.JSONDecodeError:
        print("Erreur: Fichier JSON invalide")
        return None
    except ValidationError:
        print("Erreur: Le fichier ne correspond à aucune version connue")
        return None
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")
        return None

if __name__ == "__main__":
    # Chemin vers le fichier à analyser
    test_file = Path("../releases/v1.66/00b3mhg89.json")
    
    # Vérification que le fichier existe
    if not test_file.exists():
        print(f"Erreur: Le fichier {test_file} n'existe pas")
    else:
        version = detect_ror_version(test_file)
        if version:
            print(f"Version détectée : {version}")