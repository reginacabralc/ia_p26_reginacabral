#!/usr/bin/env python3
"""
Laboratorio: Teoría de la Información (imágenes + experimentos)

Uso:
    cd clase/06_teoria_de_la_informacion
    python lab_informacion.py

Genera imágenes en:
    clase/06_teoria_de_la_informacion/images/

Este laboratorio está diseñado para enseñar en clase:
- bits como preguntas
- auto-información y entropía
- cross-entropy y KL
- ganancia esperada de información en Wordle (a escala pequeña)
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from it_code.info_math import entropy_bits, cross_entropy_bits, kl_divergence_bits
from it_code.lexicons import load_generated_spanish_5letter, load_mini_spanish_5letter
from it_code.wordle import feedback_pattern


# -----------------------------------------------------------------------------
# Styling (similar vibe to lab_probabilidad.py)
# -----------------------------------------------------------------------------

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 11
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.labelsize"] = 11

COLORS = {
    "blue": "#2E86AB",
    "red": "#E94F37",
    "green": "#27AE60",
    "gray": "#7F8C8D",
}


ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

np.random.seed(42)


def _save(fig, name: str) -> None:
    out = IMAGES_DIR / name
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Generada: {out.name}")


# -----------------------------------------------------------------------------
# 1) Entropy vs concentration (simple UX)
# -----------------------------------------------------------------------------


def plot_entropy_two_outcomes():
    ps = np.linspace(1e-6, 1 - 1e-6, 800)
    hs = [entropy_bits([p, 1 - p]) for p in ps]

    fig, ax = plt.subplots()
    ax.plot(ps, hs, color=COLORS["blue"], linewidth=2)
    ax.set_title("Entropía de Bernoulli: H(p) (bits)")
    ax.set_xlabel("p")
    ax.set_ylabel("H(p)")
    ax.axvline(0.5, color=COLORS["gray"], linestyle="--", linewidth=1)
    ax.annotate("Máximo en p=0.5", xy=(0.5, 1.0), xytext=(0.62, 0.85),
                arrowprops=dict(arrowstyle="->"))

    # Escenarios típicos para fijar intuición (no solo la forma de la curva)
    for p in [0.5, 0.9, 0.99, 0.1, 0.01]:
        h = entropy_bits([p, 1 - p])
        ax.scatter([p], [h], color=COLORS["red"], s=28, zorder=3)
        ax.annotate(
            f"p={p}\nH={h:.3f}",
            xy=(p, h),
            xytext=(10, -18),
            textcoords="offset points",
            fontsize=9,
            arrowprops=dict(arrowstyle="->", lw=0.8, alpha=0.8),
        )

    ax.set_ylim(0, 1.05)
    _save(fig, "entropia_bernoulli.png")


def plot_log2_questions():
    """
    Visual: log2(N) as \"# de preguntas sí/no\" para N opciones equiprobables.
    """
    # (A) Eje x lineal: se ve la curva logarítmica “real” en N
    Ns_lin = np.arange(1, 4097)
    ys_lin = np.log2(Ns_lin)

    fig, ax = plt.subplots()
    ax.plot(Ns_lin, ys_lin, color=COLORS["blue"], linewidth=2)
    ax.set_title("Bits como preguntas: log2(N) vs N (eje x lineal)")
    ax.set_xlabel("N (número de opciones equiprobables)")
    ax.set_ylabel("log2(N)  (preguntas sí/no en el mejor caso)")
    for N in [1, 2, 4, 8, 1024, 4096]:
        ax.scatter([N], [math.log(N, 2)], color=COLORS["red"], s=25, zorder=3)
        ax.annotate(f"N={N} → {math.log(N,2):.0f} bits", xy=(N, math.log(N, 2)),
                    xytext=(8, 8), textcoords="offset points", fontsize=9)
    _save(fig, "log2_n_preguntas_linearx.png")

    # (B) Eje x log: la curva se ve casi recta (porque log2(N) es lineal en log(N))
    Ns = np.unique(np.round(np.logspace(0, 6, 250)).astype(int))
    ys = np.log2(Ns)
    fig, ax = plt.subplots()
    ax.plot(Ns, ys, color=COLORS["blue"], linewidth=2)
    ax.set_xscale("log")
    ax.set_title("Bits como preguntas: log2(N) vs N (eje x log)")
    ax.set_xlabel("N (escala log)")
    ax.set_ylabel("log2(N) (bits)")
    for N in [1, 2, 4, 8, 1024, 4096, 1_000_000]:
        ax.scatter([N], [math.log(N, 2)], color=COLORS["red"], s=25, zorder=3)
        ax.annotate(f"N={N}\n{math.log(N,2):.1f} bits", xy=(N, math.log(N, 2)),
                    xytext=(8, 8), textcoords="offset points", fontsize=9)
    ax.annotate(
        "En eje x log, log2(N) se ve lineal",
        xy=(2000, math.log(2000, 2)),
        xytext=(30, -25),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", lw=0.8),
        fontsize=9,
    )
    _save(fig, "log2_n_preguntas_logx.png")


def plot_surprisal_vs_p_bits():
    """
    Visual: I(p) = -log2(p) vs p.
    """
    ps = np.linspace(1e-6, 1 - 1e-6, 1200)
    I = -np.log2(ps)

    fig, ax = plt.subplots()
    ax.plot(ps, I, color=COLORS["red"], linewidth=2)
    ax.set_title("Sorpresa (surprisal): I(p) = -log2(p)")
    ax.set_xlabel("p")
    ax.set_ylabel("I(p) (bits)")
    ax.set_ylim(0, 20)

    for p in [0.5, 0.1, 0.01]:
        ax.scatter([p], [-math.log(p, 2)], color=COLORS["blue"], s=30, zorder=3)
        ax.annotate(f"p={p}\nI={-math.log(p,2):.2f} bits", xy=(p, -math.log(p, 2)),
                    xytext=(10, 10), textcoords="offset points", fontsize=9,
                    arrowprops=dict(arrowstyle="->", lw=0.8))

    _save(fig, "surprisal_vs_p_bits.png")


def plot_surprisal_bases_comparison():
    """
    Visual: same surprisal curve in different bases (bits vs nats vs hartleys).
    Shows: changing base is just rescaling.
    """
    ps = np.linspace(1e-6, 1 - 1e-6, 1200)
    I_bits = -np.log2(ps)
    I_nats = -np.log(ps)  # natural log
    I_hart = -np.log10(ps)

    fig, ax = plt.subplots()
    ax.plot(ps, I_bits, label="bits (base 2)", color=COLORS["blue"], linewidth=2)
    ax.plot(ps, I_nats, label="nats (base e)", color=COLORS["red"], linewidth=2, alpha=0.85)
    ax.plot(ps, I_hart, label="hartleys (base 10)", color=COLORS["green"], linewidth=2, alpha=0.85)
    ax.set_title("La base del log solo cambia la unidad (reescala)")
    ax.set_xlabel("p")
    ax.set_ylabel("I(p) en distintas unidades")
    ax.set_ylim(0, 20)
    ax.legend()
    _save(fig, "surprisal_bases_comparison.png")


def plot_unit_conversions():
    """
    Visual: unit conversions expressed in bits.
    """
    vals = {
        "1 nat": math.log(math.e, 2),
        "1 trit": math.log(3, 2),
        "1 hartley": math.log(10, 2),
    }

    fig, ax = plt.subplots(figsize=(10, 5))
    labels = list(vals.keys())
    bits = list(vals.values())
    ax.bar(labels, bits, color=COLORS["gray"], alpha=0.9)
    ax.set_title("Conversión de unidades a bits")
    ax.set_ylabel("bits")
    for i, b in enumerate(bits):
        ax.text(i, b + 0.05, f"{b:.3f}", ha="center", va="bottom", fontsize=10)
    _save(fig, "conversion_unidades.png")


def plot_ideal_length_vs_prob():
    """
    Visual: ideal code length -log2 p vs integer lengths (ceil) for a toy prior.
    """
    # Toy prior (non-uniform)
    p = np.array([0.34, 0.22, 0.16, 0.10, 0.08, 0.05, 0.03, 0.02])
    p = p / p.sum()
    symbols = [f"s{i+1}" for i in range(len(p))]
    ideal = -np.log2(p)
    shannon = np.ceil(ideal)  # a common constructive upper bound

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(p))
    ax.bar(x - 0.18, ideal, width=0.36, label="-log2 p(x) (ideal)", color=COLORS["blue"])
    ax.bar(x + 0.18, shannon, width=0.36, label="ceil(-log2 p) (longitud entera)", color=COLORS["red"], alpha=0.85)
    ax.set_xticks(x, symbols)
    ax.set_title("Longitudes de código: ideal vs enteras (toy prior)")
    ax.set_xlabel("símbolo")
    ax.set_ylabel("bits")
    ax.legend()
    _save(fig, "ideal_length_vs_prob.png")


def plot_zipf_password_prior():
    """
    Visual: Zipf-like prior over rank: p(r) ~ 1/r^alpha (log-log).
    """
    r = np.arange(1, 100_001)
    fig, ax = plt.subplots()
    for alpha, color in [(0.9, COLORS["blue"]), (1.07, COLORS["red"]), (1.3, COLORS["green"])]:
        w = 1.0 / (r ** alpha)
        p = w / w.sum()
        ax.loglog(r, p, label=f"alpha={alpha}", linewidth=2, color=color)
    # Avoid special glyphs (font portability in CI/servers)
    ax.set_title("Prior Zipf (passwords): p(rank) ~ 1/r^alpha")
    ax.set_xlabel("rank (1=más común)")
    ax.set_ylabel("probabilidad (escala log-log)")
    ax.legend()
    _save(fig, "zipf_password_prior.png")


def plot_landauer_kTln2():
    """
    Visual: Landauer limit kT ln 2 as a function of temperature.
    (Light version: 1 equation + intuition.)
    """
    k = 1.380649e-23  # J/K
    T = np.linspace(100, 400, 400)
    E = k * T * math.log(2)

    fig, ax = plt.subplots()
    ax.plot(T, E, color=COLORS["green"], linewidth=2)
    ax.set_title("Límite de Landauer: E_min ≈ kT ln 2 (energía por borrar 1 bit)")
    ax.set_xlabel("Temperatura T (K)")
    ax.set_ylabel("E_min (joules)")

    T0 = 300
    E0 = k * T0 * math.log(2)
    ax.scatter([T0], [E0], color=COLORS["red"], s=35, zorder=3)
    ax.annotate(f"T=300K\nE≈{E0:.2e} J", xy=(T0, E0),
                xytext=(10, 10), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", lw=0.8), fontsize=9)

    _save(fig, "landauer_kTln2.png")


def plot_wordle_pattern_mass(max_words: int = 200):
    """
    Visual: for a chosen guess, show distribution over feedback patterns.
    Helps explain why some guesses \"parten\" mejor.
    """
    lex = load_generated_spanish_5letter(ROOT) or load_mini_spanish_5letter(ROOT)
    words = sorted(lex.words, key=lambda w: lex.weights.get(w, 0.0), reverse=True)[:max_words]
    weights = {w: max(lex.weights.get(w, 1.0), 1e-12) for w in words}

    # Pick a guess from the top information gain list (reusing existing logic)
    base_h = _entropy_of_word_posterior(weights, words)
    guesses = words[: min(80, len(words))]
    igs = []
    for g in guesses:
        exp_h = expected_entropy_after_guess(words, weights, g)
        igs.append((g, base_h - exp_h))
    igs.sort(key=lambda t: t[1], reverse=True)
    guess = igs[0][0]

    total = sum(weights[w] for w in words)
    pattern_mass: Dict[Tuple[int, int, int, int, int], float] = {}
    for secret in words:
        pat = feedback_pattern(secret, guess)
        pattern_mass[pat] = pattern_mass.get(pat, 0.0) + weights[secret] / total

    items = sorted(pattern_mass.items(), key=lambda kv: kv[1], reverse=True)[:25]
    labels = ["".join(str(x) for x in pat) for pat, _ in items][::-1]
    vals = [mass for _, mass in items][::-1]

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.barh(labels, vals, color=COLORS["gray"], alpha=0.9)
    ax.set_title(f"Wordle: distribución de patrones para guess='{guess}' (top 25)")
    ax.set_xlabel("P(pattern | guess, prior)")
    ax.set_ylabel("patrón (0=gris,1=amarillo,2=verde)")
    _save(fig, "wordle_pattern_mass.png")


def plot_entropy_dirichlet_like():
    """
    Show entropy as distribution becomes more concentrated.
    We build a family of distributions over N symbols by interpolating
    between uniform and a 'peaked' distribution.
    """
    # Family A: mix between uniform and one-hot (peaked on a single symbol)
    #   p_i(a) = (1-a)/N + a * 1{i=1}
    # This is a clean, controlled path from maximum-entropy (uniform) to minimum (deterministic).

    alphas = np.linspace(0, 1, 201)

    # (1) Multi-scenario plot: different N
    fig, ax = plt.subplots()
    for N, color in [(4, COLORS["blue"]), (12, COLORS["red"]), (50, COLORS["green"])]:
        uniform = np.ones(N) / N
        peaked = np.zeros(N)
        peaked[0] = 1.0
        hs = []
        for a in alphas:
            p = (1 - a) * uniform + a * peaked
            hs.append(entropy_bits(p))
        ax.plot(alphas, hs, linewidth=2, color=color, label=f"N={N}")

    ax.set_title("Entropía vs concentración (familia p(a) = (1-a)u + a·onehot)")
    ax.set_xlabel("a (0=uniforme, 1=determinista)")
    ax.set_ylabel("H (bits)")
    ax.legend(title="Tamaño del soporte")
    ax.annotate("Máximo en uniforme", xy=(0.0, math.log(12, 2)), xytext=(0.05, math.log(12, 2) - 0.6))
    ax.annotate("0 bits cuando a→1", xy=(1.0, 0.0), xytext=(0.62, 0.35))
    _save(fig, "entropia_concentracion_familias.png")

    # (2) Single-scenario plot (N=12) kept for continuity, but now explicit in the title/caption.
    N = 12
    uniform = np.ones(N) / N
    peaked = np.zeros(N)
    peaked[0] = 1.0
    hs = [entropy_bits((1 - a) * uniform + a * peaked) for a in alphas]
    fig, ax = plt.subplots()
    ax.plot(alphas, hs, color=COLORS["red"], linewidth=2)
    ax.set_title("Entropía disminuye cuando el prior se concentra (N=12, mezcla uniforme→onehot)")
    ax.set_xlabel("a (0=uniforme, 1=determinista)")
    ax.set_ylabel("H (bits)")
    ax.annotate("Uniforme: p_i=1/12", xy=(0, hs[0]), xytext=(0.06, hs[0] - 0.45))
    ax.annotate("Determinista: p_1≈1", xy=(1, hs[-1]), xytext=(0.62, 0.35))
    _save(fig, "entropia_concentracion.png")

    # (3) What do these distributions look like? Show bar charts for selected a.
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    for ax_i, a in zip(axes, [0.0, 0.6, 0.9]):
        p = (1 - a) * uniform + a * peaked
        ax_i.bar(np.arange(1, N + 1), p, color=COLORS["gray"], alpha=0.9)
        ax_i.set_title(f"N=12, a={a:.1f}")
        ax_i.set_xlabel("símbolo i")
        if ax_i is axes[0]:
            ax_i.set_ylabel("p_i")
        ax_i.set_ylim(0, 1.0)
    fig.suptitle("Cómo se ve la concentración: distribuciones p(a) para N=12", y=1.05)
    plt.tight_layout()
    _save(fig, "entropia_concentracion_distribuciones.png")


# -----------------------------------------------------------------------------
# 2) Cross-entropy & KL demo
# -----------------------------------------------------------------------------


def plot_cross_entropy_vs_model_mismatch():
    """
    Fix true p over 3 classes and vary q along a path to show:
    H(p,q) and D_KL(p||q) track mismatch.
    """
    p = np.array([0.7, 0.2, 0.1])
    q_good = np.array([0.6, 0.25, 0.15])
    q_bad = np.array([0.4, 0.3, 0.3])

    ts = np.linspace(0, 1, 201)
    h_p = entropy_bits(p)
    hs = []
    kls = []
    for t in ts:
        q = (1 - t) * q_good + t * q_bad
        q = q / q.sum()
        hs.append(cross_entropy_bits(p, q))
        kls.append(kl_divergence_bits(p, q))

    fig, ax = plt.subplots()
    ax.plot(ts, hs, label="H(p,q) (cross-entropy)", color=COLORS["blue"], linewidth=2)
    ax.plot(ts, [h_p] * len(ts), label="H(p) (entropía verdadera)", color=COLORS["gray"], linestyle="--")
    ax.plot(ts, [h_p + d for d in kls], label="H(p)+D_KL(p||q)", color=COLORS["red"], alpha=0.8)
    ax.set_title("Cross-entropy = entropía + KL (bits)")
    ax.set_xlabel("t (0=q_good → 1=q_bad)")
    ax.set_ylabel("bits")
    ax.legend()
    _save(fig, "cross_entropy_kl_identidad.png")


# -----------------------------------------------------------------------------
# 3) Wordle expected information gain (small scale)
# -----------------------------------------------------------------------------


def _entropy_of_word_posterior(weights: Dict[str, float], words: List[str]) -> float:
    ws = np.array([weights[w] for w in words], dtype=float)
    ws = ws / ws.sum()
    return entropy_bits(ws)


def expected_entropy_after_guess(
    words: List[str],
    weights: Dict[str, float],
    guess: str,
) -> float:
    """
    Computes E_F[ H(X | F, I) ] for a given guess.

    Complexity: O(N^2) in worst case (fine for demo N<=500).
    """
    # Probability of each pattern under current prior
    pattern_mass: Dict[Tuple[int, int, int, int, int], float] = {}
    # Group secrets by pattern to compute posterior entropies efficiently
    pattern_words: Dict[Tuple[int, int, int, int, int], List[str]] = {}

    total = sum(weights[w] for w in words)
    for secret in words:
        pat = feedback_pattern(secret, guess)
        m = weights[secret] / total
        pattern_mass[pat] = pattern_mass.get(pat, 0.0) + m
        pattern_words.setdefault(pat, []).append(secret)

    exp_h = 0.0
    for pat, mass in pattern_mass.items():
        post_words = pattern_words[pat]
        # Posterior over remaining candidates is proportional to prior restricted to this set
        exp_h += mass * _entropy_of_word_posterior(weights, post_words)
    return exp_h


def plot_wordle_expected_information_gain(max_words: int = 200):
    lex = load_generated_spanish_5letter(ROOT) or load_mini_spanish_5letter(ROOT)

    # For speed/UX, restrict to top-N by weight
    words = sorted(lex.words, key=lambda w: lex.weights.get(w, 0.0), reverse=True)[:max_words]
    weights = {w: max(lex.weights.get(w, 1.0), 1e-12) for w in words}

    base_h = _entropy_of_word_posterior(weights, words)

    # Candidate guesses: use same set (good enough for teaching)
    guesses = words[: min(80, len(words))]
    igs = []
    for g in guesses:
        exp_h = expected_entropy_after_guess(words, weights, g)
        igs.append((g, base_h - exp_h))

    igs.sort(key=lambda t: t[1], reverse=True)
    top = igs[:20]

    fig, ax = plt.subplots(figsize=(12, 7))
    labels = [w for (w, _) in top][::-1]
    vals = [v for (_, v) in top][::-1]
    ax.barh(labels, vals, color=COLORS["green"], alpha=0.9)
    ax.set_title(f"Top guesses por ganancia esperada de información (N={len(words)})")
    ax.set_xlabel("IG(g) = H - E[H | feedback]  (bits)")
    ax.set_ylabel("guess")
    _save(fig, "wordle_top_info_gain.png")


def main() -> int:
    print("Generando imágenes (Teoría de la Información)...")
    plot_log2_questions()
    plot_entropy_two_outcomes()
    plot_entropy_dirichlet_like()
    plot_surprisal_vs_p_bits()
    plot_surprisal_bases_comparison()
    plot_unit_conversions()
    plot_cross_entropy_vs_model_mismatch()
    plot_ideal_length_vs_prob()
    plot_zipf_password_prior()
    plot_landauer_kTln2()
    plot_wordle_expected_information_gain()
    plot_wordle_pattern_mass()
    print("Listo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

