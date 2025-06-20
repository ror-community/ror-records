import os
import time
import re
from pathlib import Path
from create_rdf_file import json_to_individual_rdf
from detect_version_json import detect_ror_version
from template_to_try import process_ror_file

def version_key(version_str):
    version_parts = version_str[1:].split('.')
    return tuple(int(part) if part.isdigit() else 0 for part in version_parts)

def list_json_files_in_releases(releases_root, output_dir):

    release_folders = [d for d in os.listdir(releases_root) 
                      if os.path.isdir(os.path.join(releases_root, d)) and d.startswith('v')]
    
    release_folders.sort(key=version_key)

    for release in release_folders:
        release_path = os.path.join(releases_root, release)

        print(f"\n=== Traitement de la release {release} ===")
        json_files = [f for f in os.listdir(release_path) if f.endswith('.json')]

        if not json_files:
            print(f"Aucun fichier JSON trouvé dans {release}")
        else:
            print("Fichiers JSON trouvés:")
            for json_file in json_files:
                json_path = os.path.join(release_path, json_file)
                print(f"Traitement du fichier: {json_path}")

                # version = detect_ror_version(json_path)
                # used_template = "template_" + version + ".ttl" # si version = None
                # path_used_template = Path(__file__).parent.parent / f"template/{used_template}"

                # json_to_individual_rdf(
                #     # json_path=Path(__file__).parent.parent / "releases/v1.66/00b3mhg89.json",
                #     json_path= json_path,
                #     template_path= path_used_template,
                #     output_dir=output_dir
                # )

                process_ror_file(json_path, output_dir)

        if release != release_folders[-1]:
            print("\nAttente de 15 secondes avant la release suivante...")
            # time.sleep(15)

if __name__ == "__main__":
    root_dir = Path(__file__).parent.parent
    releases_dir = root_dir / "releases"
    output_dir = root_dir / "folder_to_push"
    
    if not releases_dir.exists():
        print(f"Erreur: Le dossier {releases_dir} n'existe pas")
    else:
        list_json_files_in_releases(releases_dir, output_dir)