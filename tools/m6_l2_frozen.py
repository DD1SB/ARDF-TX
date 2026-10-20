"""Validate committed historical evidence without requiring private KiCad UI state.

The original inventories remain immutable. Four accidentally inventoried,
git-ignored UI/lock files were never published and cannot exist in a fresh clone.
Every other inventory entry must be tracked, present and hash-identical.
"""
import hashlib
import json
import subprocess

PERSONAL_STATE = frozenset({
    'hardware/80m/RF80.kicad_prl',
    'hardware/80m/production/RF80_V1.kicad_prl',
    'hardware/2m/RF2M.kicad_prl',
    'hardware/2m/~RF2M.kicad_pro.lck',
})


def committed_frozen(root, manifest):
    entries = json.loads(manifest.read_text())
    tracked = set(subprocess.check_output(
        ['git', 'ls-files', '-z'], cwd=root).decode().split('\0'))
    untracked = set(entries) - tracked
    assert untracked == PERSONAL_STATE, ('unexpected untracked inventory entries', untracked)
    for name in sorted(PERSONAL_STATE):
        assert subprocess.run(
            ['git', 'check-ignore', '-q', '--', name], cwd=root).returncode == 0, name
    committed = {name: digest for name, digest in entries.items() if name in tracked}
    for name, digest in committed.items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
    return committed
