from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


_RE_WORD_5 = re.compile(r"^[a-z]{5}$")


@dataclass(frozen=True)
class Lexicon:
    words: List[str]
    weights: Dict[str, float]  # unnormalized positive weights (prior proxy)


def load_mini_spanish_5letter(module_root: Path) -> Lexicon:
    p = module_root / "datasets" / "mini_spanish_5letter.txt"
    raw_words = [w.strip().lower() for w in p.read_text(encoding="utf-8").splitlines() if w.strip()]
    words = [w for w in raw_words if _RE_WORD_5.match(w)]
    # Simple fallback: uniform prior
    weights = {w: 1.0 for w in words}
    return Lexicon(words=words, weights=weights)


def load_generated_spanish_5letter(module_root: Path) -> Lexicon | None:
    p = module_root / "datasets" / "generated" / "spanish_5letter_wordfreq.csv"
    if not p.exists():
        return None
    words: List[str] = []
    weights: Dict[str, float] = {}
    with p.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            w = row["word"].strip().lower()
            c = float(row["count"])
            if not w or _RE_WORD_5.match(w) is None:
                continue
            words.append(w)
            weights[w] = max(c, 0.0)
    return Lexicon(words=words, weights=weights)


def load_passwords_generated(module_root: Path, top_n: int = 50000) -> List[str] | None:
    p = module_root / "datasets" / "generated" / f"passwords_top_{top_n}.txt"
    if not p.exists():
        return None
    return [s.strip() for s in p.read_text(encoding="utf-8", errors="ignore").splitlines() if s.strip()]


def load_passwords_mini(module_root: Path) -> List[str]:
    p = module_root / "datasets" / "mini_passwords.txt"
    return [s.strip() for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]

