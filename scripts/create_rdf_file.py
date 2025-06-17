import os
import json
import tempfile
from pathlib import Path

from sema.subyt import (
    Generator,
    GeneratorSettings,
    Sink,
    Source,
    SinkFactory,
    SourceFactory,
    JinjaBasedGenerator,
)

def json_to_rdf(path_json_file, template_name, template_directory, output_directory):
    """Convertit un JSON en multiples fichiers TTL (un par objet)"""
    # Création du dossier de sortie
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    
    # Configuration des chemins
    template_path = os.path.join(os.path.dirname(__file__), template_directory)
    generator = JinjaBasedGenerator(template_path)
    
    # Chargement des données JSON
    with open(path_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)  # Doit être une liste d'objets
    
    # Traitement par objet
    for obj in enumerate(data, start=1):
        # Création d'un fichier temporaire pour l'objet courant
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump(obj, tmp)
            tmp_path = tmp.name
        
        try:
            # Fichier de sortie pour cet objet
            ror_id = obj["id"].split("/")[-1]
            output_file = os.path.join(output_directory, f"{ror_id}.ttl")
            
            # Configuration avec le fichier temporaire comme source
            sink = SinkFactory.make_sink(output_file, False)
            inputs = {"qres": SourceFactory.make_source(tmp_path)}  # Utilise le chemin du fichier
            
            # Génération
            generator.process(f"{template_name}.ttl", inputs, GeneratorSettings(), sink, {})
            
            print(f"Généré : {output_file}")
        finally:
            # Nettoyage du fichier temporaire
            os.unlink(tmp_path)

    print(f"Terminé ! {len(data)} fichiers créés dans {output_directory}")