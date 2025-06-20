import shutil
import subprocess
import os
from pathlib import Path

def git_push_existing_ttl(repo_dir, target_dir, version_name, tag_version=None):
    
    try:
        repo_dir = Path(repo_dir).absolute()
        target_path = repo_dir / target_dir
        
        print(f"\nVérification du dépôt dans : {repo_dir}")

        if not (repo_dir / ".git").exists():
            raise FileNotFoundError("ERREUR : Aucun dossier .git trouvé (ce n'est pas un dépôt Git valide)")

        remote_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_dir,
            stderr=subprocess.PIPE
        ).decode().strip()

        print(f"URL distante détectée : {remote_url}")

        if "kgFixed/store_ror.org" not in remote_url:
            raise ValueError(
                f"ERREUR : Ce dépôt pointe vers '{remote_url}'\n"
                f"Attendu : 'kgFixed/store_ror.org'"
            )

        if not target_path.exists():
            raise FileNotFoundError(f"ERREUR : Dossier introuvable - {target_path}")

        ttl_files = list(target_path.glob("*.ttl"))
        if not ttl_files:
            print(f"ATTENTION : Aucun fichier .ttl trouvé dans {target_dir}")
        else:
            print(f"Fichiers TTL trouvés ({len(ttl_files)}): {', '.join(f.name for f in ttl_files[:3])}...")

        os.chdir(repo_dir)
        
        print("\nExécution des commandes Git...")

        subprocess.run(["git", "stash", "push", "--include-untracked"], check=True)
        print("✓ Working directory nettoyé (stash)")
        
        subprocess.run(["git", "add", f"{target_dir}/*.ttl"], check=True)
        print("✓ Fichiers ajoutés au staging")
        
        commit_msg = f"RDF update {version_name}"
        try:
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        except subprocess.CalledProcessError as e:
            print("⚠️ Aucun changement à commiter (peut-être que les fichiers étaient déjà indexés)")
            print(f"Message Git : {e.output.decode() if e.output else 'Pas de message'}")
            return True  # Ce n'est pas une erreur critique
        
        print(f"✓ Commit créé : '{commit_msg}'")
        
        if tag_version is None:
            tag_version = version_name
            
        subprocess.run(["git", "tag", "-a", tag_version, "-m", f"Version {tag_version}"], check=True)
        print(f"✓ Tag créé : {tag_version}")
        
        subprocess.run(["git", "push", "origin", "main"], check=True)
        subprocess.run(["git", "push", "origin", "--tags"], check=True)
        
        print(f"\nSUCCÈS : Poussé vers {remote_url}")
        print(f"→ Dossier : {target_dir}")
        print(f"→ Tag : {tag_version}")
        
        try:
            shutil.rmtree(target_path)
            print(f"✓ Dossier {target_dir} supprimé avec succès")
        except Exception as e:
            print(f"⚠️ Erreur lors de la suppression : {str(e)}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\nERREUR Git (code {e.returncode}): {e.stderr.decode().strip()}")
        return False
    except Exception as e:
        print(f"\nERREUR : {str(e)}")
        return False

if __name__ == "__main__":
    repo_dir = Path(__file__).parent.parent
    target_dir = "folder_to_push"  
    
    success = git_push_existing_ttl(
        repo_dir=repo_dir,
        target_dir=target_dir,
        version_name="Release v1.0",
        tag_version="v1.0"
    )
    
    if not success:
        print("\n✗ Échec de l'opération. Voir les messages ci-dessus.")
        exit(1)