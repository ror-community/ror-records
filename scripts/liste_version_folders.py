import os
import json
from pathlib import Path
import subprocess
from sema.subyt import JinjaBasedGenerator

# --- Configuration des chemins relatifs ---
# Le script est supposé être dans un sous-dossier 'scripts' du projet
PROJECT_ROOT = Path(__file__).parent.parent  # Racine du projet (où se trouve .git)
RELEASES_DIR = PROJECT_ROOT / "releases"    # Dossier contenant v1, v2, etc.
RDF_OUTPUT_DIR = PROJECT_ROOT / "rdf" / "organisations"  # Dossier de sortie
TEMPLATE_DIR = PROJECT_ROOT / "templates"   # Dossier des templates

# --- Vos fonctions existantes adaptées ---
def json_to_rdf(path_json_file, template_name, output_directory):
    """Version adaptée avec chemins relatifs"""
    # Création du dossier de sortie
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    
    # Chemin du template relatif au projet
    generator = JinjaBasedGenerator(str(TEMPLATE_DIR))
    
    # Chargement des données JSON
    with open(path_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Traitement par objet (votre logique existante)
    for obj in data:
        # ... (votre code de conversion existant)
        pass

def git_commit_and_push(version_name):
    """Version adaptée pour utiliser PROJECT_ROOT"""
    try:
        os.chdir(PROJECT_ROOT)
        subprocess.run(["git", "add", str(RDF_OUTPUT_DIR)], check=True)
        subprocess.run(["git", "commit", "-m", f"Version {version_name}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur Git: {e}")
        return False

# --- Nouvelle fonction de traitement principal ---
def process_all_versions():
    """Parcourt toutes les versions et gère le workflow complet"""
    # Vérification des dossiers
    if not RELEASES_DIR.exists():
        raise FileNotFoundError(f"Dossier releases introuvable: {RELEASES_DIR}")
    
    # Création dossier de sortie
    RDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Tri des versions (v1, v1.0, v1.1, etc.)
    version_dirs = sorted(
        [d for d in RELEASES_DIR.iterdir() if d.is_dir() and d.name.startswith('v')],
        key=lambda x: float(x.name[1:]) if x.name[1:].replace('.', '', 1).isdigit() else float('inf')
    )
    
    for version_dir in version_dirs:
        version_name = version_dir.name
        print(f"\n=== Traitement version {version_name} ===")
        
        # 1. Conversion des fichiers
        for json_file in version_dir.glob("*.json"):
            print(f"Conversion de {json_file.name}")
            json_to_rdf(
                path_json_file=str(json_file),
                template_name="template",  # Nom de votre template
                output_directory=str(RDF_OUTPUT_DIR)
            )
        
        # 2. Push Git avec vérification
        if not git_commit_and_push(version_name):
            print(f"Échec du push pour {version_name}, arrêt du processus")
            return False
        
        # 3. Nettoyage avant version suivante
        for ttl_file in RDF_OUTPUT_DIR.glob("*.ttl"):
            ttl_file.unlink()
    
    print("\nToutes les versions traitées avec succès!")
    return True

# --- Point d'entrée ---
if __name__ == "__main__":
    # Vérification que c'est bien un dépôt Git
    if not (PROJECT_ROOT / ".git").exists():
        raise NotADirectoryError(f"Dossier Git introuvable dans {PROJECT_ROOT}")
    
    process_all_versions()