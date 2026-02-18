from __future__ import annotations

import math
from typing import Dict, Iterable, List, Sequence, Tuple


def entropy_bits(probs: Iterable[float]) -> float:
    """Shannon entropy in bits for a discrete distribution."""
    h = 0.0
    for p in probs:
        if p <= 0.0:
            continue
        h += p * (-math.log(p, 2))
    return h


def normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    s = sum(weights.values())
    if s <= 0:
        raise ValueError("Sum of weights must be positive")
    return {k: v / s for k, v in weights.items()}


def cross_entropy_bits(p: Sequence[float], q: Sequence[float]) -> float:
    """Cross-entropy H(p,q) in bits."""
    if len(p) != len(q):
        raise ValueError("p and q must have same length")
    h = 0.0
    for pi, qi in zip(p, q):
        if pi <= 0.0:
            continue
        if qi <= 0.0:
            return float("inf")
        h += pi * (-math.log(qi, 2))
    return h


def kl_divergence_bits(p: Sequence[float], q: Sequence[float]) -> float:
    """KL divergence D_KL(p||q) in bits."""
    if len(p) != len(q):
        raise ValueError("p and q must have same length")
    d = 0.0
    for pi, qi in zip(p, q):
        if pi <= 0.0:
            continue
        if qi <= 0.0:
            return float("inf")
        d += pi * math.log(pi / qi, 2)
    return d

