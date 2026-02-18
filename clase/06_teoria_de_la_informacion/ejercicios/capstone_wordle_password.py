#!/usr/bin/env python3
"""
Capstone: Wordle/Password con entropía y priors (en español).

Uso:
    cd clase/06_teoria_de_la_informacion
    python ejercicios/capstone_wordle_password.py --mode wordle --random
    python ejercicios/capstone_wordle_password.py --mode wordle --secret canto
    python ejercicios/capstone_wordle_password.py --mode password
"""

from __future__ import annotations

import argparse
import math
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

MODULE_ROOT = Path(__file__).resolve().parents[1]  # .../06_teoria_de_la_informacion
# Ensure module root is importable even when executed as a script from subdir.
sys.path.insert(0, str(MODULE_ROOT))

from it_code.info_math import entropy_bits, normalize_weights
from it_code.lexicons import (
    load_generated_spanish_5letter,
    load_mini_spanish_5letter,
    load_passwords_generated,
    load_passwords_mini,
)
from it_code.wordle import feedback_pattern, filter_candidates, pattern_to_emoji


ROOT = MODULE_ROOT


Pattern = Tuple[int, int, int, int, int]


def posterior_probs(words: List[str], weights: Dict[str, float]) -> List[float]:
    ws = [max(weights.get(w, 0.0), 0.0) for w in words]
    s = sum(ws)
    if s <= 0:
        # fallback uniform
        return [1.0 / len(words)] * len(words)
    return [w / s for w in ws]


def entropy_candidates(words: List[str], weights: Dict[str, float]) -> float:
    return entropy_bits(posterior_probs(words, weights))


def expected_entropy_after_guess(
    candidates: List[str],
    weights: Dict[str, float],
    guess: str,
) -> float:
    """
    Compute E_F[ H(X | F, I) ] for a fixed guess.

    Implementation groups secrets by feedback pattern. Complexity is O(N*L),
    where N=len(candidates), L=word length (5).
    """
    total = sum(weights[w] for w in candidates)
    if total <= 0:
        total = float(len(candidates))

    pattern_mass: Dict[Pattern, float] = defaultdict(float)
    pattern_bucket: Dict[Pattern, List[str]] = defaultdict(list)

    for secret in candidates:
        pat = feedback_pattern(secret, guess)
        pattern_bucket[pat].append(secret)
        pattern_mass[pat] += weights.get(secret, 1.0) / total

    exp_h = 0.0
    for pat, mass in pattern_mass.items():
        bucket = pattern_bucket[pat]
        exp_h += mass * entropy_candidates(bucket, weights)
    return exp_h


def best_guesses_by_info_gain(
    candidates: List[str],
    weights: Dict[str, float],
    guess_pool: List[str],
    top_k: int = 10,
) -> List[Tuple[str, float]]:
    base_h = entropy_candidates(candidates, weights)
    scored: List[Tuple[str, float]] = []
    for g in guess_pool:
        exp_h = expected_entropy_after_guess(candidates, weights, g)
        scored.append((g, base_h - exp_h))
    scored.sort(key=lambda t: t[1], reverse=True)
    return scored[:top_k]


def sample_secret(candidates: List[str], weights: Dict[str, float]) -> str:
    probs = posterior_probs(candidates, weights)
    return random.choices(candidates, weights=probs, k=1)[0]


def run_wordle(secret: str | None, max_candidates: int, guess_pool_size: int, max_steps: int) -> None:
    lex = load_generated_spanish_5letter(ROOT) or load_mini_spanish_5letter(ROOT)

    # Restrict for runtime (teaching-friendly)
    candidates = sorted(lex.words, key=lambda w: lex.weights.get(w, 0.0), reverse=True)[:max_candidates]
    weights = {w: max(lex.weights.get(w, 1.0), 1e-12) for w in candidates}

    if secret is None:
        secret = sample_secret(candidates, weights)
    if secret not in set(candidates):
        raise SystemExit(
            f"Secret '{secret}' no está en el lexicón actual (N={len(candidates)}). "
            "Prueba con --random o aumenta --max-candidates."
        )

    # Choose guesses from top weights as well (good enough for class)
    guess_pool = candidates[: min(guess_pool_size, len(candidates))]

    print("\n=== Wordle (con feedback) ===")
    print(f"Lexicón: N={len(candidates)} (prior proxy)")
    print(f"Entropía inicial H(X|I) = {entropy_candidates(candidates, weights):.2f} bits")
    print("Nota: el solver elige guess maximizando IG(g) = H - E[H | feedback].\n")

    remaining = candidates
    for step in range(1, max_steps + 1):
        base_h = entropy_candidates(remaining, weights)
        top = best_guesses_by_info_gain(
            candidates=remaining,
            weights=weights,
            guess_pool=guess_pool,
            top_k=5,
        )
        guess = top[0][0]

        pat = feedback_pattern(secret, guess)
        remaining2 = filter_candidates(remaining, guess, pat)
        h2 = entropy_candidates(remaining2, weights) if remaining2 else 0.0

        print(f"Paso {step}: guess='{guess}'  feedback={pattern_to_emoji(pat)}")
        print(f"  H antes: {base_h:.2f} bits")
        print("  Top-5 IG: " + ", ".join([f"{g}:{ig:.2f}" for g, ig in top]))
        print(f"  Candidatas: {len(remaining)} → {len(remaining2)}")
        print(f"  H después: {h2:.2f} bits\n")

        remaining = remaining2
        if guess == secret:
            print(f"✓ ¡Encontrada! secret='{secret}' en {step} pasos.\n")
            return
        if len(remaining) <= 1:
            if remaining:
                print(f"✓ Quedó una sola candidata: '{remaining[0]}'\n")
            else:
                print("⚠️ No quedaron candidatas (inconsistencia). Revisa lexicón/feedback.\n")
            return

    print(f"Fin: no se encontró en {max_steps} pasos. Secret era '{secret}'.\n")


def password_expected_guesses_zipf(passwords: List[str], alpha: float = 1.07, top_n: int = 50000) -> float:
    """
    We usually don't have real probabilities for passwords; we use a Zipf-like prior
    over rank as a defensible proxy: p(rank=r) ∝ 1/r^alpha.
    """
    m = min(top_n, len(passwords))
    weights = [1.0 / (r ** alpha) for r in range(1, m + 1)]
    s = sum(weights)
    probs = [w / s for w in weights]
    # Expected number of guesses if we try in rank order:
    return sum((r + 1) * p for r, p in enumerate(probs))


def run_password(top_n: int) -> None:
    pw = load_passwords_generated(ROOT, top_n=top_n) or load_passwords_mini(ROOT)
    m = min(top_n, len(pw))
    pw = pw[:m]

    print("\n=== Password guessing (sin feedback) ===")
    print(f"Lista de passwords: N={len(pw)} (orden ≈ 'más comunes primero')")
    print("Modelo de prior: Zipf sobre rank (proxy realista cuando no hay frecuencias).")

    for alpha in [0.9, 1.07, 1.3]:
        eg = password_expected_guesses_zipf(pw, alpha=alpha, top_n=m)
        print(f"- alpha={alpha:.2f}: E[#intentos] ≈ {eg:.0f}")

    print("\nLectura:")
    print("- Con feedback (Wordle), puedes maximizar ganancia de información por intento.")
    print("- Sin feedback (password), tu estrategia es ordenar intentos por prior;")
    print("  el costo esperado depende brutalmente de qué tan sesgada es la distribución.\n")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["wordle", "password"], required=True)
    ap.add_argument("--secret", type=str, default=None, help="Palabra secreta (5 letras) para Wordle")
    ap.add_argument("--random", action="store_true", help="Elegir secret aleatorio según prior")
    ap.add_argument("--max-candidates", type=int, default=800, help="N máximo de candidatas (runtime)")
    ap.add_argument("--guess-pool", type=int, default=250, help="Tamaño del pool de guesses (runtime)")
    ap.add_argument("--max-steps", type=int, default=6)
    ap.add_argument("--password-top-n", type=int, default=50000)
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    random.seed(42)

    if args.mode == "wordle":
        if args.random:
            secret = None
        else:
            secret = args.secret
        run_wordle(
            secret=secret,
            max_candidates=args.max_candidates,
            guess_pool_size=args.guess_pool,
            max_steps=args.max_steps,
        )
        return 0

    if args.mode == "password":
        run_password(top_n=args.password_top_n)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

