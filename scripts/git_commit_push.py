import os
import subprocess
import shutil
import re
from pathlib import Path

def normalize_name(name):
    return re.sub(r'[^\w-]', '-', name).lower()[:40]

def git_push_existing_ttl(repo_dir, target_dir, version_name, tag_version=None):
    try:
        repo_path = Path(repo_dir).absolute()
        target_path = (repo_path / target_dir).absolute()
        
        if not target_path.exists():
            raise FileNotFoundError(f"ERROR: Folder {target_path} not found")
        
        ttl_files = [f for f in target_path.glob('*.ttl') if f.is_file()]
        if not ttl_files:
            raise FileNotFoundError(f"ERROR: No .ttl file in {target_path}")

        print(f"\n=== Processing {len(ttl_files)} files ===")

        tag_name = tag_version if tag_version else version_name.replace(' ', '-')
        
        tag_exists = subprocess.run(
            ['git', 'show-ref', '--tags', f'refs/tags/{tag_name}'],
            cwd=str(repo_path),
            capture_output=True
        ).returncode == 0

        if tag_exists:
            subprocess.run(
                ['git', 'tag', '-d', tag_name],
                cwd=str(repo_path),
                check=True
            )
            print(f"✓ Existing tag {tag_name} deleted")
    
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

            subprocess.run(
                ['cmd', '/c', str(batch_file)],
                cwd=str(repo_path),
                shell=True,
                check=True
            )

            print(f"\n✅ Success: {len(ttl_files)} files pushed with tag {tag_name}")

            try:
                shutil.rmtree(target_path, ignore_errors=True)
                print(f"✓ Cleaned {target_dir} folder")
            except Exception as e:
                print(f"⚠️ Cleaning error: {str(e)}")

            return True

        finally:
            if batch_file.exists():
                os.remove(batch_file)

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Git error (code{e.returncode}): {e.stderr.decode().strip()}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR : {str(e)}")
        return False