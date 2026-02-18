#!/usr/bin/env python3
"""
Prepare lexicons and priors for the capstone and the lab.

Usage (from clase/06_teoria_de_la_informacion/):
    python -m datasets.prepare_lexicons
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / "cache"
OUT_DIR = ROOT / "generated"
OUT_DIR.mkdir(exist_ok=True)


_RE_ASCII_WORD = re.compile(r"^[a-z]+$")


def _normalize_token(token: str) -> str:
    """
    Normalize Spanish tokens to a simplified form:
    - lower
    - strip accents/diacritics
    - keep only [a-z]

    This matches our pedagogical choice to avoid accents in the Wordle-style game.
    """
    token = token.strip().lower()
    token = unicodedata.normalize("NFD", token)
    token = "".join(ch for ch in token if unicodedata.category(ch) != "Mn")
    return token


def _is_valid_5letter_word(token: str) -> bool:
    if len(token) != 5:
        return False
    return _RE_ASCII_WORD.match(token) is not None


def prepare_spanish_5letter_from_openslr(limit: int = 20000) -> Path:
    """
    Reads OpenSLR SLR21 wordlist json (word->count), normalizes tokens,
    filters to 5-letter ASCII words, aggregates collisions, and writes a CSV.
    """
    src = CACHE_DIR / "openslr_slr21_es_wordlist.json"
    if not src.exists():
        raise FileNotFoundError(
            f"Missing {src}. Run: python -m datasets.download_datasets"
        )

    data = json.loads(src.read_text(encoding="utf-8"))
    # data is typically a dict: word -> count
    counts: Counter[str] = Counter()
    for raw_word, raw_count in data.items():
        w = _normalize_token(str(raw_word))
        if not _is_valid_5letter_word(w):
            continue
        try:
            c = int(raw_count)
        except Exception:
            continue
        if c <= 0:
            continue
        counts[w] += c

    # Keep top by count (a prior proxy)
    items = counts.most_common(limit)
    out = OUT_DIR / "spanish_5letter_wordfreq.csv"
    lines = ["word,count"]
    lines += [f"{w},{c}" for (w, c) in items]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def prepare_password_list_top_n(n: int = 50000) -> Path:
    """
    Reads SecLists top passwords and writes a trimmed list.
    """
    src = CACHE_DIR / "seclists_top_100000_passwords.txt"
    if not src.exists():
        raise FileNotFoundError(
            f"Missing {src}. Run: python -m datasets.download_datasets"
        )

    out = OUT_DIR / f"passwords_top_{n}.txt"
    out_lines = []
    for line in src.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s:
            continue
        out_lines.append(s)
        if len(out_lines) >= n:
            break
    out.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    return out


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    w = prepare_spanish_5letter_from_openslr()
    p = prepare_password_list_top_n()
    print("✓ Generated:")
    print(f"- {w}")
    print(f"- {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

