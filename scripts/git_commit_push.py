import subprocess
import os

def git_commit_and_push(repo_dir, version_name):
    """Effectue un commit et push Git, retourne True si réussi"""
    try:
        # Se placer dans le répertoire Git
        os.chdir(repo_dir)
        
        # Ajouter tous les fichiers
        subprocess.run(["git", "add", "."], check=True)
        
        # Faire le commit
        commit_message = f"Ajout des données RDF pour la version {version_name}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Pousser vers le dépôt distant
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print(f"Push Git réussi pour {version_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur Git pour {version_name}: {e}")
        return False