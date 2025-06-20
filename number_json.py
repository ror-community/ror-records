import os
from pathlib import Path

def count_json_files_per_release(repo_path="ror-records"):
    """
    Compte le nombre de fichiers JSON dans chaque dossier de release (v1.X).
    Args:
        repo_path (str): Chemin local vers le dépôt ror-records (par défaut "ror-records").
    Returns:
        dict: Dictionnaire {version: nombre_de_json}
    """
    releases_data = {}
    
    # Parcours des dossiers v1.X
    for folder in Path(repo_path).iterdir():
        if folder.is_dir() and folder.name.startswith("v1."):
            json_count = 0
            # Compte récursivement tous les .json
            for root, _, files in os.walk(folder):
                json_count += sum(1 for file in files if file.endswith(".json"))
            releases_data[folder.name] = json_count
    
    return releases_data

# Exemple d'utilisation
if __name__ == "__main__":
    repo_path = input("Chemin vers le dossier 'ror-records' (laisser vide si dans le même répertoire) : ") or "ror-records"
    results = count_json_files_per_release(Path(__file__).parent.parent / 'store_ror.org/releases')
    somme = 0

    print("\nNombre de fichiers JSON par release :")
    for version, count in sorted(results.items()):
        somme = somme + count
        print(f"{version}: {count:,}")
        
    print(f"Total : {somme}")