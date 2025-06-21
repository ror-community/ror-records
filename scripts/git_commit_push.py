import shutil
import subprocess
import os
from pathlib import Path

def git_push_existing_ttl(repo_dir, target_dir, version_name, tag_version=None):
    try:
        repo_dir = Path(repo_dir).absolute()
        target_path = repo_dir / target_dir
        original_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=repo_dir).decode().strip()
        status_output = subprocess.check_output(['git', 'status', '--porcelain'], cwd=repo_dir).decode()

        print(f"\n=== Traitement de la release {version_name} ===")

        if status_output:
            print("\n⚠️ Attention : Votre dépôt contient des modifications non commitées :")
            print(status_output)
            confirm = input("Voulez-vous continuer ? Ces modifications ne seront pas affectées (y/n): ")
            if confirm.lower() != 'y':
                print("Annulation par l'utilisateur")
                return False

        temp_branch = f"temp/rdf-release-{version_name}"
        subprocess.run(['git', 'checkout', '-b', temp_branch], cwd=repo_dir, check=True)
        print(f"✓ Branche temporaire créée : {temp_branch}")

        try:
            subprocess.run(['git', 'add', f'{target_dir}/*.ttl'], cwd=repo_dir, check=True)
            
            diff_output = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=repo_dir).decode()
            
            if not diff_output:
                print("Aucun changement TTL à commiter - peut-être que les fichiers étaient déjà indexés")
                return True

            commit_msg = f"[RDF-AUTO] Update {version_name}"
            subprocess.run(['git', 'commit', '-m', commit_msg], cwd=repo_dir, check=True)
            print(f"✓ Commit créé : {commit_msg}")

            tag_name = tag_version if tag_version else version_name
            subprocess.run(['git', 'tag', '-a', tag_name, '-m', f"RDF Release {tag_name}"], cwd=repo_dir, check=True)
            print(f"✓ Tag créé : {tag_name}")

            subprocess.run(['git', 'push', 'origin', f'{temp_branch}:main', '--tags'], cwd=repo_dir, check=True)
            print("✓ Push réussi vers main")

            subprocess.run(['git', 'checkout', original_branch], cwd=repo_dir, check=True)
            subprocess.run(['git', 'branch', '-D', temp_branch], cwd=repo_dir, check=True)
            
            if target_path.exists():
                shutil.rmtree(target_path)
                print(f"✓ Dossier {target_dir} nettoyé")
            else:
                print(f"Le dossier {target_dir} était déjà absent")

            return True

        except Exception as e:
            print(f"⚠️ Erreur durant le processus : {str(e)}")
            print("Nettoyage de la branche temporaire...")
            subprocess.run(['git', 'checkout', original_branch], cwd=repo_dir)
            subprocess.run(['git', 'branch', '-D', temp_branch], cwd=repo_dir, stderr=subprocess.DEVNULL)
            return False

    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE : {str(e)}")
        return False