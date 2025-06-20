import os
from pathlib import Path
from detect_version_json import detect_ror_version
from create_rdf_file import json_to_individual_rdf

def process_ror_file(json_path, output_dir):
    version = detect_ror_version(json_path)
    
    templates_to_try = []
    
    if version is None:
        templates_to_try = [
            "template_1_0.ttl",
            "template_2_0.ttl",
            "template_2_1.ttl"
        ]
    else:
        templates_to_try = [f"template_{version}.ttl"]
    
    for template_name in templates_to_try:
        path_used_template = Path(__file__).parent.parent / f"template/{template_name}"
        
        try:
            json_to_individual_rdf(
                json_path=json_path,
                template_path=path_used_template,
                output_dir=output_dir
            )
            # print(f"Succès avec le template: {template_name}")
            return
            
        except Exception as e:
            print(f"Échec avec le template {template_name}: {str(e)}")
            continue
    
    raise ValueError(f"Aucun template valide trouvé pour le fichier: {json_path}")

# Exemple avec un json qui ne correspond a aucune version
# process_ror_file(Path(__file__).parent.parent / "releases/v1.6/023rffy11.json", Path(__file__).parent.parent / "test")
