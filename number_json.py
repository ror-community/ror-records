import os
from pathlib import Path

def count_json_files_per_release(repo_path="ror-records"):
    releases_data = {}
    
    for folder in Path(repo_path).iterdir():
        if folder.is_dir() and folder.name.startswith("v1."):
            json_count = 0
            for root, _, files in os.walk(folder):
                json_count += sum(1 for file in files if file.endswith(".json"))
            releases_data[folder.name] = json_count
    
    return releases_data

if __name__ == "__main__":
    results = count_json_files_per_release(Path(__file__).parent.parent / 'store_ror.org/releases')
    sum = 0

    for version, count in sorted(results.items()):
        sum = sum + count
        print(f"{version}: {count:,}")
        
    print(f"Sum : {sum}")