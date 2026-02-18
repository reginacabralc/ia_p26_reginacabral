#!/usr/bin/env python3
"""
Download datasets used in the module (OpenSLR SLR21 + SecLists).

Usage (from clase/06_teoria_de_la_informacion/):
    python -m datasets.download_datasets

This script downloads to datasets/cache/ by default.
"""

from __future__ import annotations

import hashlib
import os
import sys
import tarfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / "cache"
CACHE_DIR.mkdir(exist_ok=True)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    print(f"↓ Downloading {url}")
    with urllib.request.urlopen(url) as r, dest.open("wb") as f:
        f.write(r.read())
    print(f"✓ Saved {dest}")


def download_openslr_es_wordlist() -> Path:
    """
    OpenSLR SLR21 provides es_wordlist.json.tgz
    Mirrors can change; we use the canonical page host.
    """
    url = "https://www.openslr.org/resources/21/es_wordlist.json.tgz"
    tgz_path = CACHE_DIR / "openslr_slr21_es_wordlist.json.tgz"
    _download(url, tgz_path)
    return tgz_path


def extract_openslr_wordlist(tgz_path: Path) -> Path:
    out_path = CACHE_DIR / "openslr_slr21_es_wordlist.json"
    if out_path.exists():
        return out_path

    print("↳ Extracting OpenSLR wordlist JSON")
    with tarfile.open(tgz_path, "r:gz") as tf:
        # The tarball typically contains a single file named es_wordlist.json
        members = tf.getmembers()
        json_members = [m for m in members if m.name.endswith(".json")]
        if not json_members:
            raise RuntimeError("No .json found inside OpenSLR tarball")
        m = json_members[0]
        extracted = tf.extractfile(m)
        if extracted is None:
            raise RuntimeError("Failed to extract JSON member")
        out_path.write_bytes(extracted.read())

    print(f"✓ Extracted {out_path}")
    return out_path


def download_seclists_passwords() -> Path:
    """
    Download a common-passwords list from SecLists (MIT).

    We avoid heavy / clearly-leaked raw corpora when possible. This is a curated top list.
    """
    url = (
        "https://raw.githubusercontent.com/danielmiessler/SecLists/"
        "master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt"
    )
    out_path = CACHE_DIR / "seclists_top_100000_passwords.txt"
    _download(url, out_path)
    return out_path


def main() -> int:
    print(f"Cache dir: {CACHE_DIR}")

    try:
        tgz = download_openslr_es_wordlist()
        json_path = extract_openslr_wordlist(tgz)
        pw_path = download_seclists_passwords()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print("\nResumen:")
    print(f"- OpenSLR tgz: {tgz} (sha256={_sha256(tgz)[:12]}...)")
    print(f"- OpenSLR json: {json_path} (sha256={_sha256(json_path)[:12]}...)")
    print(f"- SecLists pw: {pw_path} (sha256={_sha256(pw_path)[:12]}...)")
    print("\nSiguiente paso:")
    print("  python -m datasets.prepare_lexicons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

