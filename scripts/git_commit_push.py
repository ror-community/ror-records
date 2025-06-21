import os
import subprocess
import shutil
import re
from pathlib import Path

def normalize_name(name):
    """Normalise les noms pour Git (branches/tags)"""
    return re.sub(r'[^\w-]', '-', name).lower()[:40]

def git_push_existing_ttl(repo_dir, target_dir, version_name, tag_version=None):
    """Version finale avec gestion robuste des tags"""
    try:
        # Configuration des chemins
        repo_path = Path(repo_dir).absolute()
        target_path = (repo_path / target_dir).absolute()
        
        # Vérifications
        if not target_path.exists():
            raise FileNotFoundError(f"ERREUR : Dossier {target_path} introuvable")
        
        ttl_files = [f for f in target_path.glob('*.ttl') if f.is_file()]
        if not ttl_files:
            raise FileNotFoundError(f"ERREUR : Aucun fichier .ttl dans {target_path}")

        print(f"\n=== Traitement de {len(ttl_files)} fichiers ===")

        # Gestion du tag
        tag_name = tag_version if tag_version else version_name.replace(' ', '-')
        
        # Vérification si le tag existe déjà
        tag_exists = subprocess.run(
            ['git', 'show-ref', '--tags', f'refs/tags/{tag_name}'],
            cwd=str(repo_path),
            capture_output=True
        ).returncode == 0

        if tag_exists:
            # Option 1 : Suppression du tag existant
            subprocess.run(
                ['git', 'tag', '-d', tag_name],
                cwd=str(repo_path),
                check=True
            )
            print(f"✓ Tag existant {tag_name} supprimé")
            
            # Option 2 : Vous pouvez aussi choisir de ne rien faire et utiliser un nom différent
            # tag_name = f"{tag_name}-new"
            # print(f"✓ Utilisation du nouveau tag {tag_name}")

        # Fichier batch temporaire (méthode infaillible sous Windows)
        batch_file = repo_path / "git_operations.bat"
        try:
            with open(batch_file, 'w', encoding='utf-8') as f:
                f.write("@echo off\n")
                for ttl_file in ttl_files:
                    rel_path = ttl_file.relative_to(repo_path)
                    f.write(f'git add "{rel_path}"\n')
                f.write(f'git commit -m "[RDF] {version_name}"\n')
                f.write(f'git tag -a {tag_name} -m "Version {tag_name}"\n')
                f.write('git push origin main --tags\n')

            # Exécution
            subprocess.run(
                ['cmd', '/c', str(batch_file)],
                cwd=str(repo_path),
                shell=True,
                check=True
            )

            print(f"\n✅ Succès : {len(ttl_files)} fichiers poussés avec tag {tag_name}")

            # Nettoyage
            try:
                shutil.rmtree(target_path, ignore_errors=True)
                print(f"✓ Dossier {target_dir} nettoyé")
            except Exception as e:
                print(f"⚠️ Erreur nettoyage : {str(e)}")

            return True

        finally:
            if batch_file.exists():
                os.remove(batch_file)

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur Git (code {e.returncode}): {e.stderr.decode().strip()}")
        return False
    except Exception as e:
        print(f"\n❌ ERREUR : {str(e)}")
        return False