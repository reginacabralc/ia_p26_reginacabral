from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple


# Feedback encoding:
# 2 = green (correct letter, correct position)
# 1 = yellow (correct letter, wrong position)
# 0 = gray  (letter not present, or present but already consumed by greens/yellows)


def feedback_pattern(secret: str, guess: str) -> Tuple[int, int, int, int, int]:
    if len(secret) != len(guess):
        raise ValueError("secret and guess must have same length")
    if len(secret) != 5:
        raise ValueError("this helper expects 5-letter words")

    secret = secret.lower()
    guess = guess.lower()

    pat = [0] * 5
    remaining = Counter(secret)

    # Greens first
    for i, (s, g) in enumerate(zip(secret, guess)):
        if g == s:
            pat[i] = 2
            remaining[g] -= 1

    # Yellows next (only if remaining count exists)
    for i, (s, g) in enumerate(zip(secret, guess)):
        if pat[i] == 2:
            continue
        if remaining[g] > 0:
            pat[i] = 1
            remaining[g] -= 1

    return tuple(pat)  # type: ignore[return-value]


def is_consistent(secret_candidate: str, guess: str, pattern: Tuple[int, int, int, int, int]) -> bool:
    return feedback_pattern(secret_candidate, guess) == pattern


def filter_candidates(
    candidates: Iterable[str],
    guess: str,
    pattern: Tuple[int, int, int, int, int],
) -> List[str]:
    return [w for w in candidates if is_consistent(w, guess, pattern)]


def pattern_to_emoji(pattern: Tuple[int, int, int, int, int]) -> str:
    # Wordle-like visualization
    mapping = {2: "🟩", 1: "🟨", 0: "⬛"}
    return "".join(mapping[int(x)] for x in pattern)


@dataclass(frozen=True)
class WordleStep:
    guess: str
    pattern: Tuple[int, int, int, int, int]
    remaining: int

