#!/usr/bin/env python3
"""
Laboratorio: Teoría de la Decisión (imágenes para las notas)

Uso:
    cd clase/09_teoria_decision
    python lab_decision.py

Genera imágenes en:
    clase/09_teoria_decision/images/

Dependencias: numpy, matplotlib, scipy
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.lines import Line2D
from scipy.stats import norm, poisson

# -----------------------------------------------------------------------------
# Styling (same vibe as lab_prediccion.py / lab_optimization.py)
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
    "orange": "#F39C12",
    "purple": "#8E44AD",
}

ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

np.random.seed(42)


def _save(fig, name: str) -> None:
    out = IMAGES_DIR / name
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"  Generada: {out.name}")


# -----------------------------------------------------------------------------
# 1) Decision matrix heatmap
# -----------------------------------------------------------------------------


def plot_decision_matrix():
    """Heatmap payoff matrix: umbrella (llevar/no) x weather (lluvia/sol)."""
    # Payoff matrix: rows=actions, cols=states
    actions = ["Llevar paraguas", "No llevar paraguas"]
    states = ["Lluvia", "Sol"]
    # Payoffs: (action, state) -> utility
    payoffs = np.array([
        [8, 5],   # llevar paraguas: lluvia=dry but carrying, sol=carrying for nothing
        [1, 10],  # no llevar: lluvia=soaked, sol=free hands
    ])

    fig, ax = plt.subplots(figsize=(8, 5))

    im = ax.imshow(payoffs, cmap="YlGnBu", aspect="auto", vmin=0, vmax=12)
    fig.colorbar(im, ax=ax, label="Utilidad")

    # Labels
    ax.set_xticks(range(len(states)))
    ax.set_xticklabels(states, fontsize=12, fontweight="bold")
    ax.set_yticks(range(len(actions)))
    ax.set_yticklabels(actions, fontsize=12, fontweight="bold")
    ax.set_xlabel("Estado de la naturaleza (S)", fontsize=12)
    ax.set_ylabel("Acción (A)", fontsize=12)

    # Annotate values
    for i in range(len(actions)):
        for j in range(len(states)):
            text_color = "white" if payoffs[i, j] > 6 else "black"
            ax.text(j, i, f"U = {payoffs[i, j]}", ha="center", va="center",
                    fontsize=16, fontweight="bold", color=text_color)

    # Add annotations
    ax.set_title("Matriz de decisión: el problema del paraguas", fontsize=14)

    # Side annotation
    fig.text(0.02, 0.15,
             "Ingredientes:\n"
             "  S = {Lluvia, Sol}\n"
             "  A = {Llevar, No llevar}\n"
             "  U: A x S -> R",
             fontsize=9, fontfamily="monospace",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF3CD", alpha=0.9))

    fig.tight_layout()
    _save(fig, "01_decision_matrix.png")


# -----------------------------------------------------------------------------
# 2) Three regimes: certainty, risk, ignorance
# -----------------------------------------------------------------------------


def plot_three_regimes():
    """3 panels: certainty (single bar), risk (bars+probs), ignorance (bars+'?')."""
    actions = ["Llevar", "No llevar"]
    states = ["Lluvia", "Sol"]
    payoffs = np.array([
        [8, 5],
        [1, 10],
    ])

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # --- Panel 1: Certainty ---
    ax = axes[0]
    # We know it will rain -> state index 0
    vals = payoffs[:, 0]
    bars = ax.bar(actions, vals, color=[COLORS["blue"], COLORS["red"]],
                  edgecolor="black", linewidth=1.2)
    ax.set_title("Certeza: sabemos que llueve", fontsize=12, fontweight="bold")
    ax.set_ylabel("Utilidad")
    ax.set_ylim(0, 12)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.3, f"U = {v}",
                ha="center", fontsize=11, fontweight="bold")
    best_idx = np.argmax(vals)
    bars[best_idx].set_edgecolor(COLORS["green"])
    bars[best_idx].set_linewidth(3)
    ax.text(0.5, 0.88, "Optimización\n(Mod 07)",
            transform=ax.transAxes, ha="center", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#E8F8E8", alpha=0.9))

    # --- Panel 2: Risk ---
    ax = axes[1]
    prob_rain = 0.4
    probs = np.array([prob_rain, 1 - prob_rain])
    eus = payoffs @ probs  # expected utility per action
    x_pos = np.arange(len(actions))
    width = 0.35

    # Show individual payoffs as grouped bars
    for j, (state, color) in enumerate(zip(states, [COLORS["blue"], COLORS["orange"]])):
        bars = ax.bar(x_pos + j * width - width / 2, payoffs[:, j], width,
                      label=f"{state} (p={probs[j]:.1f})", color=color,
                      edgecolor="black", linewidth=0.8, alpha=0.7)

    # EU line
    for i, eu in enumerate(eus):
        ax.plot([i - 0.3, i + 0.3], [eu, eu], color=COLORS["red"],
                linewidth=3, zorder=5)
        ax.text(i + 0.32, eu, f"EU={eu:.1f}", fontsize=10, fontweight="bold",
                color=COLORS["red"], va="center")

    ax.set_xticks(x_pos)
    ax.set_xticklabels(actions)
    ax.set_title("Riesgo: P(Lluvia) = 0.4", fontsize=12, fontweight="bold")
    ax.set_ylabel("Utilidad")
    ax.set_ylim(0, 12)
    ax.legend(fontsize=9, loc="upper left")
    ax.text(0.5, 0.88, "Utilidad Esperada\n(Este módulo)",
            transform=ax.transAxes, ha="center", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF9E7", alpha=0.9))

    # --- Panel 3: Ignorance ---
    ax = axes[2]
    # Show payoffs with "?" for probabilities
    for j, (state, color) in enumerate(zip(states, [COLORS["blue"], COLORS["orange"]])):
        bars = ax.bar(x_pos + j * width - width / 2, payoffs[:, j], width,
                      label=f"{state} (p=?)", color=color,
                      edgecolor="black", linewidth=0.8, alpha=0.5)

    # Maximin: worst case per action
    worst_case = payoffs.min(axis=1)
    for i, wc in enumerate(worst_case):
        ax.plot([i - 0.3, i + 0.3], [wc, wc], color=COLORS["purple"],
                linewidth=3, zorder=5, linestyle="--")
        ax.text(i + 0.32, wc, f"min={wc}", fontsize=10, fontweight="bold",
                color=COLORS["purple"], va="center")

    ax.set_xticks(x_pos)
    ax.set_xticklabels(actions)
    ax.set_title("Ignorancia: no sabemos P(S)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Utilidad")
    ax.set_ylim(0, 12)
    ax.legend(fontsize=9, loc="upper left")
    ax.text(0.5, 0.88, "Maximin / Minimax\nRegret",
            transform=ax.transAxes, ha="center", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#F3E5F5", alpha=0.9))

    fig.suptitle("Tres regímenes de decisión", fontsize=14, y=1.02)
    fig.tight_layout()
    _save(fig, "02_three_regimes.png")


# -----------------------------------------------------------------------------
# 3) Utility functions: risk averse, neutral, seeking + Jensen
# -----------------------------------------------------------------------------


def plot_utility_functions():
    """3 utility curves (sqrt, linear, x^2) + Jensen's inequality visualization."""
    x = np.linspace(0, 100, 500)

    u_averse = np.sqrt(x)        # concave
    u_neutral = x / 10           # linear (scaled for visual)
    u_seeking = (x / 10) ** 2    # convex

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # --- Left: Three utility functions ---
    ax = axes[0]
    ax.plot(x, u_averse, color=COLORS["blue"], linewidth=2.5,
            label=r"Averso: $U(x) = \sqrt{x}$ (cóncava)")
    ax.plot(x, u_neutral, color=COLORS["gray"], linewidth=2.5, linestyle="--",
            label=r"Neutral: $U(x) = x/10$ (lineal)")
    ax.plot(x, u_seeking, color=COLORS["red"], linewidth=2.5,
            label=r"Buscador: $U(x) = (x/10)^2$ (convexa)")
    ax.set_xlabel("Riqueza (x)", fontsize=12)
    ax.set_ylabel("Utilidad U(x)", fontsize=12)
    ax.set_title("Tres tipos de preferencia al riesgo", fontsize=13)
    ax.legend(fontsize=10, loc="upper left")

    # --- Right: Jensen's inequality for concave U ---
    ax = axes[1]
    # Lottery: 50% chance of 25, 50% chance of 75
    x1, x2 = 25.0, 75.0
    p = 0.5
    ex = p * x1 + (1 - p) * x2  # E[X] = 50
    u_ex = np.sqrt(ex)           # U(E[X])
    eu = p * np.sqrt(x1) + (1 - p) * np.sqrt(x2)  # E[U(X)]

    ax.plot(x, np.sqrt(x), color=COLORS["blue"], linewidth=2.5, label=r"$U(x) = \sqrt{x}$")

    # Chord between (x1, U(x1)) and (x2, U(x2))
    ax.plot([x1, x2], [np.sqrt(x1), np.sqrt(x2)], "--",
            color=COLORS["red"], linewidth=1.5, alpha=0.8)

    # Points
    ax.scatter([x1, x2], [np.sqrt(x1), np.sqrt(x2)], color=COLORS["orange"],
               s=80, zorder=5, edgecolors="black")
    ax.scatter([ex], [u_ex], color=COLORS["green"], s=100, zorder=5,
               edgecolors="black", marker="D", label=f"U(E[X]) = {u_ex:.2f}")
    ax.scatter([ex], [eu], color=COLORS["red"], s=100, zorder=5,
               edgecolors="black", marker="s", label=f"E[U(X)] = {eu:.2f}")

    # Vertical gap: Jensen's inequality
    ax.annotate("", xy=(ex, eu), xytext=(ex, u_ex),
                arrowprops=dict(arrowstyle="<->", lw=2, color=COLORS["purple"]))
    ax.text(ex + 2, (u_ex + eu) / 2, f"Jensen's gap\n= {u_ex - eu:.2f}",
            fontsize=10, color=COLORS["purple"], fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))

    # Labels
    ax.annotate(f"({x1:.0f}, {np.sqrt(x1):.1f})", xy=(x1, np.sqrt(x1)),
                xytext=(x1 - 15, np.sqrt(x1) + 1), fontsize=9)
    ax.annotate(f"({x2:.0f}, {np.sqrt(x2):.1f})", xy=(x2, np.sqrt(x2)),
                xytext=(x2 + 3, np.sqrt(x2) - 1), fontsize=9)

    ax.set_xlabel("Riqueza (x)", fontsize=12)
    ax.set_ylabel("Utilidad U(x)", fontsize=12)
    ax.set_title("Desigualdad de Jensen: U(E[X]) > E[U(X)]", fontsize=13)
    ax.legend(fontsize=9, loc="upper left")
    ax.text(0.5, 0.05, "Para U cóncava (averso al riesgo):\nprefiere el valor seguro E[X] a la lotería",
            transform=ax.transAxes, ha="center", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF3CD", alpha=0.9))

    fig.suptitle("Utilidad, riesgo y la desigualdad de Jensen", fontsize=14, y=1.02)
    fig.tight_layout()
    _save(fig, "03_utility_functions.png")


# -----------------------------------------------------------------------------
# 4) Risk aversion lottery: certainty equivalents
# -----------------------------------------------------------------------------


def plot_risk_aversion_lottery():
    """Lottery vs sure thing under 3 utility functions, certainty equivalents."""
    # Lottery L: 50% of $100, 50% of $0
    # Sure thing: $50
    x = np.linspace(0.01, 100, 500)

    utils = {
        "Averso": (lambda w: np.sqrt(w), COLORS["blue"]),
        "Neutral": (lambda w: w / 10, COLORS["gray"]),
        "Buscador": (lambda w: (w / 10) ** 2, COLORS["red"]),
    }

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for ax, (name, (u_fn, color)) in zip(axes, utils.items()):
        ax.plot(x, u_fn(x), color=color, linewidth=2.5)

        # Lottery endpoints
        w_low, w_high = 0.01, 100.0
        p = 0.5
        eu = p * u_fn(w_low) + (1 - p) * u_fn(w_high)
        ew = p * w_low + (1 - p) * w_high  # = 50
        u_sure = u_fn(ew)

        # Chord
        ax.plot([w_low, w_high], [u_fn(w_low), u_fn(w_high)], "--",
                color="black", alpha=0.4, linewidth=1)

        # EU point on chord
        ax.scatter([ew], [eu], color=COLORS["orange"], s=80, zorder=5,
                   edgecolors="black", label=f"E[U(L)] = {eu:.2f}")

        # U(E[W]) point on curve
        ax.scatter([ew], [u_sure], color=COLORS["green"], s=80, zorder=5,
                   edgecolors="black", marker="D", label=f"U(&#36;50) = {u_sure:.2f}")

        # Certainty equivalent: find CE such that U(CE) = EU
        # For sqrt: CE = eu^2, for linear: CE = eu*10, for quadratic: CE = 10*sqrt(eu)
        from scipy.optimize import brentq
        try:
            ce = brentq(lambda w: u_fn(w) - eu, 0.01, 100)
        except ValueError:
            ce = ew
        ax.axvline(ce, color=color, linestyle=":", linewidth=1.5, alpha=0.7)
        ax.scatter([ce], [eu], color=color, s=60, zorder=5, marker="^",
                   edgecolors="black", label=f"CE = &#36;{ce:.1f}")

        ax.set_xlabel("Riqueza")
        ax.set_ylabel("Utilidad")
        ax.set_title(f"{name} al riesgo", fontsize=12, fontweight="bold")
        ax.legend(fontsize=8, loc="upper left")
        ax.set_ylim(bottom=-0.5)

    fig.suptitle("Lotería [50%: &#36;0, 50%: &#36;100] vs &#36;50 seguros", fontsize=14, y=1.02)
    fig.tight_layout()
    _save(fig, "04_risk_aversion_lottery.png")


# -----------------------------------------------------------------------------
# 5) Decision tree: oil drilling with backward induction
# -----------------------------------------------------------------------------


def plot_decision_tree():
    """Oil drilling decision tree with backward induction values."""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(-1, 13)
    ax.set_ylim(-1, 9)
    ax.axis("off")

    # Node styles
    def draw_decision(ax, x, y, label, value=None):
        """Square node = decision."""
        rect = mpatches.FancyBboxPatch((x - 0.35, y - 0.35), 0.7, 0.7,
                                        boxstyle="square,pad=0.1",
                                        facecolor=COLORS["blue"], edgecolor="black",
                                        linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, label, ha="center", va="center", fontsize=9,
                fontweight="bold", color="white")
        if value is not None:
            ax.text(x, y - 0.65, f"EU = {value}", ha="center", fontsize=8,
                    fontweight="bold", color=COLORS["blue"])

    def draw_chance(ax, x, y, label, value=None):
        """Circle node = chance."""
        circle = plt.Circle((x, y), 0.35, facecolor=COLORS["orange"],
                             edgecolor="black", linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, label, ha="center", va="center", fontsize=8,
                fontweight="bold", color="white")
        if value is not None:
            ax.text(x, y - 0.6, f"EU = {value}", ha="center", fontsize=8,
                    fontweight="bold", color=COLORS["orange"])

    def draw_terminal(ax, x, y, value, color=COLORS["green"]):
        """Triangle / value node."""
        ax.text(x, y, f"${value}k", ha="center", va="center", fontsize=10,
                fontweight="bold", color=color,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor=color, linewidth=1.5))

    def draw_edge(ax, x0, y0, x1, y1, label="", above=True):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", lw=1.5, color=COLORS["gray"]))
        if label:
            mid_x = (x0 + x1) / 2
            mid_y = (y0 + y1) / 2
            offset = 0.25 if above else -0.25
            ax.text(mid_x, mid_y + offset, label, ha="center", fontsize=8,
                    fontstyle="italic", color=COLORS["gray"])

    # Tree structure:
    # Root: Decision (Drill / Don't drill)
    #   - Don't drill -> $0
    #   - Drill -> Chance (Oil? p=0.3)
    #     - Oil (p=0.3) -> Decision (Big well / Small well)
    #       - Big well -> Chance (High/Low)
    #         - High (p=0.5) -> $800k
    #         - Low (p=0.5) -> $200k
    #       - Small well -> $300k
    #     - Dry (p=0.7) -> -$100k

    # Backward induction:
    # Big well: EU = 0.5*800 + 0.5*200 = 500
    # Oil decision: max(500, 300) = 500 (Big well)
    # Drill: EU = 0.3*500 + 0.7*(-100) = 150 - 70 = 80
    # Root: max(80, 0) = 80 (Drill)

    # Level 0: Root decision
    draw_decision(ax, 1, 5, "D1", value=80)

    # Branch: Don't drill
    draw_edge(ax, 1.35, 5, 3.5, 2, "No perforar", above=False)
    draw_terminal(ax, 4, 2, 0, color=COLORS["gray"])

    # Branch: Drill -> Chance
    draw_edge(ax, 1.35, 5, 3.5, 7, "Perforar\n(costo: -$100k)", above=True)
    draw_chance(ax, 4, 7, "C1", value=80)

    # Chance: Oil
    draw_edge(ax, 4.35, 7, 6.5, 8, "Petróleo\np=0.3", above=True)
    draw_decision(ax, 7, 8, "D2", value=500)

    # Chance: Dry
    draw_edge(ax, 4.35, 7, 6.5, 5.5, "Seco\np=0.7", above=False)
    draw_terminal(ax, 7.5, 5.5, -100, color=COLORS["red"])

    # Decision 2: Big well
    draw_edge(ax, 7.35, 8, 9.5, 8.5, "Pozo grande", above=True)
    draw_chance(ax, 10, 8.5, "C2", value=500)

    # Decision 2: Small well
    draw_edge(ax, 7.35, 8, 9.5, 7, "Pozo chico", above=False)
    draw_terminal(ax, 10.5, 7, 300)

    # Chance 2: High yield
    draw_edge(ax, 10.35, 8.5, 12, 9, "Alto p=0.5", above=True)
    draw_terminal(ax, 12.5, 9, 800)

    # Chance 2: Low yield
    draw_edge(ax, 10.35, 8.5, 12, 7.5, "Bajo p=0.5", above=False)
    draw_terminal(ax, 12.5, 7.5, 200)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=COLORS["blue"], edgecolor="black", label="Decisión"),
        mpatches.Patch(facecolor=COLORS["orange"], edgecolor="black", label="Azar"),
        mpatches.Patch(facecolor="white", edgecolor=COLORS["green"], label="Resultado"),
    ]
    ax.legend(handles=legend_elements, loc="lower left", fontsize=10,
              framealpha=0.9)

    ax.set_title("Árbol de decisión: perforación petrolera (inducción hacia atrás)",
                 fontsize=14, pad=15)
    _save(fig, "05_decision_tree.png")


# -----------------------------------------------------------------------------
# 6) Value of Information: medical test
# -----------------------------------------------------------------------------


def plot_voi_medical():
    """Left: EU bars with/without test + VoI gap. Right: VoI vs test accuracy."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Scenario: patient may have disease (prior p=0.1)
    # Action: Treat (cost=50, benefit if sick=200) or Don't treat
    # Without info:
    #   EU(Treat)   = 0.1*(200-50) + 0.9*(-50) = 15 - 45 = -30
    #   EU(NoTreat) = 0.1*(-200) + 0.9*(0) = -20
    #   Best: EU(NoTreat) = -20
    # With perfect info:
    #   If sick (p=0.1): Treat -> 150; NoTreat -> -200 => Treat (150)
    #   If healthy (p=0.9): Treat -> -50; NoTreat -> 0 => NoTreat (0)
    #   EU(perfect) = 0.1*150 + 0.9*0 = 15
    #   VPI = 15 - (-20) = 35

    p_sick = 0.1
    # Payoffs
    u_treat_sick = 150     # benefit - cost
    u_treat_healthy = -50  # just the cost
    u_no_sick = -200       # untreated disease
    u_no_healthy = 0       # nothing happens

    eu_treat = p_sick * u_treat_sick + (1 - p_sick) * u_treat_healthy
    eu_no = p_sick * u_no_sick + (1 - p_sick) * u_no_healthy
    eu_without = max(eu_treat, eu_no)
    best_without = "No tratar" if eu_no >= eu_treat else "Tratar"

    # Perfect info
    eu_perfect = p_sick * max(u_treat_sick, u_no_sick) + \
                 (1 - p_sick) * max(u_treat_healthy, u_no_healthy)
    vpi = eu_perfect - eu_without

    # --- Left panel: bar chart ---
    labels = ["EU(Tratar)", "EU(No tratar)", "EU(info perfecta)"]
    values = [eu_treat, eu_no, eu_perfect]
    colors_bars = [COLORS["blue"], COLORS["red"], COLORS["green"]]
    bars = ax1.bar(labels, values, color=colors_bars, edgecolor="black", linewidth=1.2)

    for bar, v in zip(bars, values):
        y_pos = v + 1 if v >= 0 else v - 4
        ax1.text(bar.get_x() + bar.get_width() / 2, y_pos, f"{v:.0f}",
                ha="center", fontsize=12, fontweight="bold")

    # VoI annotation
    ax1.annotate("", xy=(2, eu_perfect), xytext=(2, eu_without),
                arrowprops=dict(arrowstyle="<->", lw=2.5, color=COLORS["purple"]))
    ax1.text(2.45, (eu_perfect + eu_without) / 2,
             f"VPI = {vpi:.0f}",
             fontsize=12, fontweight="bold", color=COLORS["purple"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#F3E5F5", alpha=0.9))

    ax1.axhline(0, color="black", linewidth=0.5)
    ax1.set_ylabel("Utilidad esperada")
    ax1.set_title("Decisión médica: Valor de la Información Perfecta", fontsize=12)
    ax1.text(0.02, 0.98,
             f"P(enfermo) = {p_sick}\n"
             f"Mejor sin info: {best_without} (EU = {eu_without:.0f})\n"
             f"Con info perfecta: EU = {eu_perfect:.0f}\n"
             f"VPI = {vpi:.0f}",
             transform=ax1.transAxes, fontsize=9, va="top",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F4F8", alpha=0.9))

    # --- Right panel: VoI vs test accuracy ---
    accuracies = np.linspace(0.5, 1.0, 100)
    vois = []

    for acc in accuracies:
        # Imperfect test: P(+|sick) = acc, P(-|healthy) = acc
        # P(sick|+) = acc * p_sick / (acc*p_sick + (1-acc)*(1-p_sick))
        # P(sick|-) = (1-acc)*p_sick / ((1-acc)*p_sick + acc*(1-p_sick))
        p_pos = acc * p_sick + (1 - acc) * (1 - p_sick)
        p_neg = 1 - p_pos
        p_sick_pos = acc * p_sick / p_pos if p_pos > 0 else 0
        p_sick_neg = (1 - acc) * p_sick / p_neg if p_neg > 0 else 0

        # EU given positive test
        eu_treat_pos = p_sick_pos * u_treat_sick + (1 - p_sick_pos) * u_treat_healthy
        eu_no_pos = p_sick_pos * u_no_sick + (1 - p_sick_pos) * u_no_healthy
        best_pos = max(eu_treat_pos, eu_no_pos)

        # EU given negative test
        eu_treat_neg = p_sick_neg * u_treat_sick + (1 - p_sick_neg) * u_treat_healthy
        eu_no_neg = p_sick_neg * u_no_sick + (1 - p_sick_neg) * u_no_healthy
        best_neg = max(eu_treat_neg, eu_no_neg)

        eu_with_test = p_pos * best_pos + p_neg * best_neg
        voi = eu_with_test - eu_without
        vois.append(voi)

    ax2.plot(accuracies * 100, vois, color=COLORS["purple"], linewidth=2.5)
    ax2.fill_between(accuracies * 100, 0, vois, alpha=0.15, color=COLORS["purple"])
    ax2.axhline(vpi, color=COLORS["green"], linestyle="--", linewidth=1.5,
                label=f"VPI = {vpi:.0f}")
    ax2.set_xlabel("Precisión del test (%)", fontsize=12)
    ax2.set_ylabel("Valor de la Información", fontsize=12)
    ax2.set_title("VoI crece con la calidad del test", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.set_xlim(50, 100)
    ax2.set_ylim(bottom=0)
    ax2.text(0.5, 0.05, "Test al 50% = moneda al aire (VoI = 0)\n"
             "Test al 100% = info perfecta (VoI = VPI)",
             transform=ax2.transAxes, ha="center", fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF3CD", alpha=0.9))

    fig.suptitle("Valor de la Información en diagnóstico médico", fontsize=14, y=1.02)
    fig.tight_layout()
    _save(fig, "06_voi_medical.png")


# -----------------------------------------------------------------------------
# 7) Maximin vs MEU: different criteria pick different actions
# -----------------------------------------------------------------------------


def plot_maximin_vs_meu():
    """Two actions under 3 states: MEU vs maximin pick different actions."""
    states = ["$s_1$\n(boom)", "$s_2$\n(normal)", "$s_3$\n(crisis)"]
    actions = ["Acción A\n(agresiva)", "Acción B\n(conservadora)"]

    # Payoffs designed so MEU picks A but maximin picks B
    payoffs = np.array([
        [100, 40, -50],   # Action A: high upside, negative downside
        [30, 35, 10],     # Action B: moderate everywhere
    ])

    probs = np.array([0.3, 0.5, 0.2])

    eu_a = payoffs[0] @ probs  # 30 + 20 - 10 = 40
    eu_b = payoffs[1] @ probs  # 9 + 17.5 + 2 = 28.5
    min_a = payoffs[0].min()   # -50
    min_b = payoffs[1].min()   # 10

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    x = np.arange(len(states))
    width = 0.35

    # --- Left: MEU ---
    bars_a = ax1.bar(x - width / 2, payoffs[0], width, color=COLORS["red"],
                     edgecolor="black", linewidth=1.2, alpha=0.8, label="A (agresiva)")
    bars_b = ax1.bar(x + width / 2, payoffs[1], width, color=COLORS["blue"],
                     edgecolor="black", linewidth=1.2, alpha=0.8, label="B (conservadora)")

    # Probability labels
    for i, p in enumerate(probs):
        ax1.text(i, max(payoffs[0, i], payoffs[1, i]) + 5,
                f"p = {p}", ha="center", fontsize=9, fontstyle="italic")

    # EU lines
    ax1.axhline(eu_a, color=COLORS["red"], linewidth=2, linestyle="--",
                label=f"EU(A) = {eu_a:.1f}", alpha=0.8)
    ax1.axhline(eu_b, color=COLORS["blue"], linewidth=2, linestyle="--",
                label=f"EU(B) = {eu_b:.1f}", alpha=0.8)

    ax1.set_xticks(x)
    ax1.set_xticklabels(states, fontsize=10)
    ax1.set_ylabel("Utilidad")
    ax1.set_title("Criterio MEU: elige A", fontsize=12, fontweight="bold")
    ax1.legend(fontsize=9, loc="upper right")
    ax1.axhline(0, color="black", linewidth=0.5)

    # Winner highlight
    ax1.text(0.5, 0.92, "MEU elige A (mayor EU)",
             transform=ax1.transAxes, ha="center", fontsize=11,
             fontweight="bold", color=COLORS["red"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FDEDEC", alpha=0.9))

    # --- Right: Maximin ---
    bars_a2 = ax2.bar(x - width / 2, payoffs[0], width, color=COLORS["red"],
                      edgecolor="black", linewidth=1.2, alpha=0.8, label="A (agresiva)")
    bars_b2 = ax2.bar(x + width / 2, payoffs[1], width, color=COLORS["blue"],
                      edgecolor="black", linewidth=1.2, alpha=0.8, label="B (conservadora)")

    # Worst case highlights
    # Find worst state for each action
    worst_a_idx = np.argmin(payoffs[0])
    worst_b_idx = np.argmin(payoffs[1])
    bars_a2[worst_a_idx].set_edgecolor(COLORS["red"])
    bars_a2[worst_a_idx].set_linewidth(3)
    bars_b2[worst_b_idx].set_edgecolor(COLORS["blue"])
    bars_b2[worst_b_idx].set_linewidth(3)

    # Min lines
    ax2.axhline(min_a, color=COLORS["red"], linewidth=2, linestyle=":",
                label=f"min(A) = {min_a}", alpha=0.8)
    ax2.axhline(min_b, color=COLORS["blue"], linewidth=2, linestyle=":",
                label=f"min(B) = {min_b}", alpha=0.8)

    ax2.set_xticks(x)
    ax2.set_xticklabels(states, fontsize=10)
    ax2.set_ylabel("Utilidad")
    ax2.set_title("Criterio Maximin: elige B", fontsize=12, fontweight="bold")
    ax2.legend(fontsize=9, loc="upper right")
    ax2.axhline(0, color="black", linewidth=0.5)

    ax2.text(0.5, 0.92, "Maximin elige B (mejor peor caso)",
             transform=ax2.transAxes, ha="center", fontsize=11,
             fontweight="bold", color=COLORS["blue"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#D6EAF8", alpha=0.9))

    fig.suptitle("MEU vs Maximin: diferentes criterios, diferentes decisiones",
                 fontsize=14, y=1.02)
    fig.tight_layout()
    _save(fig, "07_maximin_vs_meu.png")


# -----------------------------------------------------------------------------
# 8) Newsvendor problem
# -----------------------------------------------------------------------------


def plot_newsvendor():
    """Expected cost vs order quantity, optimal q*, demand distribution inset."""
    # Parameters
    mu_demand = 50       # mean demand
    sigma_demand = 15    # std of demand
    c_o = 2              # overage cost (per unsold unit)
    c_u = 7              # underage cost (per unmet demand unit)

    # Critical ratio
    cr = c_u / (c_o + c_u)  # = 7/9 ≈ 0.778
    q_star = norm.ppf(cr, mu_demand, sigma_demand)  # optimal order

    # Expected cost as function of q
    qs = np.linspace(10, 90, 300)
    expected_costs = []
    for q in qs:
        # E[cost] = c_o * E[max(q-D, 0)] + c_u * E[max(D-q, 0)]
        # Using normal distribution integration
        d_vals = np.linspace(0, 120, 1000)
        p_d = norm.pdf(d_vals, mu_demand, sigma_demand)
        p_d = p_d / p_d.sum()  # normalize
        overage = np.maximum(q - d_vals, 0)
        underage = np.maximum(d_vals - q, 0)
        ec = c_o * (overage * p_d).sum() + c_u * (underage * p_d).sum()
        expected_costs.append(ec)

    expected_costs = np.array(expected_costs)
    min_cost = expected_costs.min()

    fig, ax = plt.subplots(figsize=(12, 7))

    # Main plot: expected cost vs q
    ax.plot(qs, expected_costs, color=COLORS["blue"], linewidth=2.5,
            label="Costo esperado E[C(q)]")
    ax.axvline(q_star, color=COLORS["red"], linewidth=2, linestyle="--",
               label=f"$q^{{\\ast}}$ = {q_star:.1f}")
    ax.scatter([q_star], [min_cost], color=COLORS["red"], s=120, zorder=5,
               edgecolors="black", linewidths=2)

    # Shaded regions
    ax.fill_between(qs[qs < q_star], expected_costs[qs < q_star],
                    min_cost, alpha=0.1, color=COLORS["orange"],
                    label="Costo de escasez")
    ax.fill_between(qs[qs > q_star], expected_costs[qs > q_star],
                    min_cost, alpha=0.1, color=COLORS["purple"],
                    label="Costo de exceso")

    ax.set_xlabel("Cantidad a ordenar (q)", fontsize=12)
    ax.set_ylabel("Costo esperado", fontsize=12)
    ax.set_title("Problema del vendedor de periódicos", fontsize=14)
    ax.legend(fontsize=10, loc="upper right")

    # Annotation box
    ax.text(0.02, 0.98,
            f"Demanda ~ N({mu_demand}, {sigma_demand}$^2$)\n"
            f"Costo exceso $c_o$ = &#36;{c_o}/unidad\n"
            f"Costo escasez $c_u$ = &#36;{c_u}/unidad\n"
            f"Ratio crítico: $c_u/(c_o+c_u)$ = {cr:.3f}\n"
            f"$q^{{\\ast}}$ = $F^{{-1}}$({cr:.3f}) = {q_star:.1f}",
            transform=ax.transAxes, fontsize=10, va="top",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#E8F4F8", alpha=0.9))

    # Inset: demand distribution
    ax_inset = ax.inset_axes([0.55, 0.45, 0.4, 0.35])
    d_x = np.linspace(0, 100, 300)
    d_y = norm.pdf(d_x, mu_demand, sigma_demand)
    ax_inset.plot(d_x, d_y, color=COLORS["green"], linewidth=2)
    ax_inset.fill_between(d_x, d_y, alpha=0.2, color=COLORS["green"])
    ax_inset.axvline(q_star, color=COLORS["red"], linewidth=1.5, linestyle="--")
    ax_inset.axvline(mu_demand, color=COLORS["gray"], linewidth=1, linestyle=":")
    ax_inset.set_title("Distribución de demanda", fontsize=9)
    ax_inset.set_xlabel("d", fontsize=8)
    ax_inset.set_ylabel("P(D=d)", fontsize=8)
    ax_inset.tick_params(labelsize=7)
    # Shade areas
    ax_inset.fill_between(d_x[d_x <= q_star], d_y[d_x <= q_star],
                          alpha=0.3, color=COLORS["purple"])
    ax_inset.fill_between(d_x[d_x >= q_star], d_y[d_x >= q_star],
                          alpha=0.3, color=COLORS["orange"])
    ax_inset.text(q_star + 1, max(d_y) * 0.7, "$q^{\\ast}$", fontsize=9,
                  color=COLORS["red"])

    _save(fig, "08_newsvendor.png")


# -----------------------------------------------------------------------------
# 9) Mean-variance efficient frontier
# -----------------------------------------------------------------------------


def plot_mean_variance_frontier():
    """Efficient frontier scatter: return vs std dev, labeled portfolios."""
    np.random.seed(42)

    # Generate random portfolios from 5 assets
    n_assets = 5
    n_portfolios = 3000

    # Asset parameters
    expected_returns = np.array([0.05, 0.08, 0.12, 0.15, 0.20])
    volatilities = np.array([0.08, 0.12, 0.18, 0.22, 0.30])

    # Correlation matrix
    corr = np.array([
        [1.0, 0.3, 0.1, 0.0, -0.1],
        [0.3, 1.0, 0.4, 0.2, 0.1],
        [0.1, 0.4, 1.0, 0.5, 0.3],
        [0.0, 0.2, 0.5, 1.0, 0.6],
        [-0.1, 0.1, 0.3, 0.6, 1.0],
    ])
    cov = np.outer(volatilities, volatilities) * corr

    port_returns = []
    port_stds = []
    port_sharpes = []

    for _ in range(n_portfolios):
        # Random weights (Dirichlet)
        w = np.random.dirichlet(np.ones(n_assets))
        ret = w @ expected_returns
        std = np.sqrt(w @ cov @ w)
        port_returns.append(ret)
        port_stds.append(std)
        rf = 0.02
        port_sharpes.append((ret - rf) / std if std > 0 else 0)

    port_returns = np.array(port_returns)
    port_stds = np.array(port_stds)
    port_sharpes = np.array(port_sharpes)

    fig, ax = plt.subplots(figsize=(12, 8))

    # Scatter all portfolios
    scatter = ax.scatter(port_stds * 100, port_returns * 100, c=port_sharpes,
                         cmap="viridis", s=10, alpha=0.5)
    fig.colorbar(scatter, ax=ax, label="Sharpe ratio")

    # Find efficient frontier (upper envelope)
    # Bin by return level, find min std for each
    ret_bins = np.linspace(port_returns.min(), port_returns.max(), 50)
    frontier_stds = []
    frontier_rets = []
    for i in range(len(ret_bins) - 1):
        mask = (port_returns >= ret_bins[i]) & (port_returns < ret_bins[i + 1])
        if mask.sum() > 0:
            min_std_idx = np.argmin(port_stds[mask])
            frontier_stds.append(port_stds[mask][min_std_idx])
            frontier_rets.append(port_returns[mask][min_std_idx])

    ax.plot(np.array(frontier_stds) * 100, np.array(frontier_rets) * 100,
            color=COLORS["red"], linewidth=2.5, label="Frontera eficiente", zorder=5)

    # Mark special portfolios
    # Min variance
    min_var_idx = np.argmin(port_stds)
    ax.scatter([port_stds[min_var_idx] * 100], [port_returns[min_var_idx] * 100],
               color=COLORS["green"], s=150, zorder=10, edgecolors="black",
               linewidths=2, marker="D", label="Min varianza")
    ax.annotate("Min varianza", xy=(port_stds[min_var_idx] * 100, port_returns[min_var_idx] * 100),
                xytext=(10, -15), textcoords="offset points", fontsize=9,
                fontweight="bold", color=COLORS["green"])

    # Max Sharpe
    max_sharpe_idx = np.argmax(port_sharpes)
    ax.scatter([port_stds[max_sharpe_idx] * 100], [port_returns[max_sharpe_idx] * 100],
               color=COLORS["orange"], s=150, zorder=10, edgecolors="black",
               linewidths=2, marker="*", label="Max Sharpe")
    ax.annotate("Max Sharpe", xy=(port_stds[max_sharpe_idx] * 100, port_returns[max_sharpe_idx] * 100),
                xytext=(10, 5), textcoords="offset points", fontsize=9,
                fontweight="bold", color=COLORS["orange"])

    # Individual assets
    for i, (vol, ret) in enumerate(zip(volatilities, expected_returns)):
        ax.scatter([vol * 100], [ret * 100], color="black", s=80, zorder=8,
                   edgecolors="white", linewidths=2, marker="o")
        ax.annotate(f"Activo {i + 1}", xy=(vol * 100, ret * 100),
                    xytext=(5, 5), textcoords="offset points", fontsize=8)

    # Mean-variance tradeoff annotation
    ax.text(0.02, 0.98,
            "Tradeoff media-varianza:\n"
            r"$\max_w \; E[R_p] - \lambda \cdot \mathrm{Var}(R_p)$" + "\n"
            r"$\lambda$ grande $\rightarrow$ conservador" + "\n"
            r"$\lambda$ chico $\rightarrow$ agresivo",
            transform=ax.transAxes, fontsize=9, va="top",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF3CD", alpha=0.9))

    ax.set_xlabel("Riesgo: desviación estándar (%)", fontsize=12)
    ax.set_ylabel("Retorno esperado (%)", fontsize=12)
    ax.set_title("Frontera eficiente de media-varianza", fontsize=14)
    ax.legend(fontsize=9, loc="lower right")

    _save(fig, "09_mean_variance_frontier.png")


# =============================================================================
# Main
# =============================================================================


def main():
    print("Generando imagenes para modulo 09: Teoria de la Decision\n")
    plot_decision_matrix()
    plot_three_regimes()
    plot_utility_functions()
    plot_risk_aversion_lottery()
    plot_decision_tree()
    plot_voi_medical()
    plot_maximin_vs_meu()
    plot_newsvendor()
    plot_mean_variance_frontier()
    print(f"\n  Todas las imagenes generadas en {IMAGES_DIR}")


if __name__ == "__main__":
    main()
