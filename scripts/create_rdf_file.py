import json
from pathlib import Path
import tempfile
from sema.subyt import Subyt
import logging

logging.getLogger("sema.subyt").setLevel(logging.ERROR) #montre uniquement les erreurs

def json_to_individual_rdf(json_path, template_path, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
        organizations = [data] if isinstance(data, dict) else data
        
        for org in organizations:
            ror_id = org['id'].split('/')[-1]
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp:
                json.dump({"sets": {"qres": [org]}}, tmp, ensure_ascii=False, indent=2)
                tmp_path = tmp.name
            
            try:
                Subyt(
                    template_name=Path(template_path).name,
                    template_folder=str(Path(template_path).parent),
                    extra_sources={"qres": str(Path(tmp_path).resolve())},
                    sink=str(output_dir / f"{ror_id}.ttl"),
                    overwrite_sink=True,
                    conditional=False
                ).process()
            finally:
                Path(tmp_path).unlink()

# Exemple d'utilisation pour 2.1
# json_to_individual_rdf( 
#     json_path= Path(__file__).parent.parent / "releases/v1.6/023rffy11.json",
#     template_path= Path(__file__).parent.parent / "template/template_2_1.ttl",
#     output_dir= Path(__file__).parent.parent / "to_push"
# )

# Exemple d'utilisation pour 1.0
# json_to_individual_rdf( 
#     json_path= Path(__file__).parent.parent / "releases/v1.6/023rffy11.json",
#     template_path= Path(__file__).parent.parent / "template/template_1_0.ttl",
#     output_dir= Path(__file__).parent.parent / "to_push"
# )