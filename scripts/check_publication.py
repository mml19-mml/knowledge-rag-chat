"""Inspect Git index (or source tree outside Git); never print credential values."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DENIED_DIRS = {'.git', 'uploads', 'node_modules', 'model-cache', '.venv', 'venv', '__pycache__', '.pytest_cache', 'logs', 'reports'}
DENIED_EXT = {'.zip', '.7z', '.rar', '.tar', '.gz', '.pdf', '.docx', '.xlsx', '.db', '.sqlite', '.sqlite3', '.dump', '.pem', '.key', '.p12', '.pfx', '.log', '.safetensors', '.pt', '.pth'}
PATTERNS = [rb'sk-[A-Za-z0-9_-]{20,}', rb'gh[pousr]_[A-Za-z0-9]{30,}',
            rb'github_pat_[A-Za-z0-9_]{30,}', rb'AKIA[0-9A-Z]{16}',
            rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
            rb'xox[baprs]-[A-Za-z0-9-]{20,}']

def git(*args):
    return subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True)

def main():
    try:
        probe = git('rev-parse', '--show-toplevel')
        indexed = probe.returncode == 0 and Path(probe.stdout.decode().strip()).resolve() == ROOT
    except FileNotFoundError:
        indexed = False
    if indexed:
        listing = git('ls-files', '--stage', '-z')
        if listing.returncode: raise SystemExit('Cannot read Git index')
        entries=[]
        for entry in listing.stdout.split(b'\0'):
            if not entry: continue
            meta, path = entry.split(b'\t', 1)
            mode, oid, stage = meta.split()
            name = path.decode('utf-8')
            if mode not in {b'100644', b'100755'} or stage != b'0':
                raise SystemExit('Unsupported index entry: '+name)
            blob=git('cat-file', 'blob', oid.decode())
            if blob.returncode: raise SystemExit('Cannot read staged file: '+name)
            entries.append((name,blob.stdout))
    else:
        entries=[]
        for path in ROOT.rglob('*'):
            rel=path.relative_to(ROOT)
            if '.git' in rel.parts: continue
            if path.is_symlink(): raise SystemExit('Symlink must be reviewed: '+str(rel))
            if path.is_file(): entries.append((rel.as_posix(),path.read_bytes()))
    failures=[]
    for name,data in entries:
        p=Path(name)
        if (set(p.parts)&DENIED_DIRS or p.suffix.lower() in DENIED_EXT or
            (p.name.startswith('.env') and p.name!='.env.example') or p.name in {'id_rsa','id_ed25519'}):
            failures.append((name,'private/data/generated file'))
        if any(re.search(pattern,data) for pattern in PATTERNS):
            failures.append((name,'credential-like content'))
        if p.name=='.env.example':
            for line in data.decode('utf-8-sig').splitlines():
                if line.lstrip().startswith('#') or '=' not in line: continue
                key,value=line.split('=',1)
                if re.search(r'API_KEY|SECRET|TOKEN|PASSWORD',key) and value.strip():
                    failures.append((name,'nonempty credential template'))
    for name,reason in failures: print(f'BLOCKED: {name}: {reason}')
    print(f'Checked {len(entries)} files from '+('Git index' if indexed else 'source tree'))
    return 1 if failures else 0

if __name__=='__main__': sys.exit(main())
