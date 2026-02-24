from typing import Union, Any
import math
import numpy as np

class NZA:
    &quot;&quot;&quot;
    N-Zero Arithmetic (NZA) number: ν = (λ_local, ∞_universe)

    From v4_super paper: Local label λ_local ∈ ℤ or ℝ_labels, true value always ∞.
    Supports semiring ops: ⊕ (+), ⊖ (-), ⊗ (*), / with 1/0_local → ∞_density + ∞_universe.

    Core Axioms (paper Sec 2):
    1. Conservation: ∀ states, ∑_universe = ∞ (invariant total positivity).
    2. Labeling: Subtraction yields λ_local = a - b, compensated by +(a + b)_universe.
    3. No Negative Entities: All entities ≥ 0; negatives are directional labels only.

    Theorem 1 (Conservation Preservation): ∀ ν_i ∈ U, ∑ ν_i = (∑ λ_local) + k·∞_universe = ∞ (k ≥ 1).
    Proof: By Axiom 1, finite ∑λ + ∞ = ∞.

    Theorem 2 (No Annihilation): ∀ a,b > 0, a ⊖ b ≠ 0_entity.
    Proof: a ⊖ b = (a-b)_local + ∞_universe ≠ (0, 0). Ontology: universe always ∞ > 0.

    Structure: Conservation semiring U = (ℕ_∞ ∪ ℤ_labels, ⊕, ⊗).
    &quot;&quot;&quot;
    def __init__(self, local: Union[int, float, np.ndarray] = 0):
        self.local: float | np.ndarray = np.asarray(float(local)) if np.isscalar(local) else np.asarray(local, dtype=float)
        self.universe = float('inf')

    def __repr__(self) -> str:
        if np.isinf(self.local).any():
            return "∞_density + ∞_universe"
        sign = "-" if np.min(self.local) < 0 else ""
        abs_local = np.abs(self.local)
        if np.isscalar(abs_local):
            return f"{sign}{abs_local}_local + ∞_universe" if abs_local != 0 else "0_local + ∞_universe"
        return f"[{sign}{abs_local}_local] + ∞_universe"

    def __str__(self) -> str:
        return repr(self)

    @property
    def total(self) -> float:
        &quot;&quot;&quot;Always ∞ due to conservation (Theorem 1).&quot;&quot;&quot;
        return self.local + self.universe if np.isscalar(self.local) else np.full_like(self.local, np.inf)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, NZA):
            return NotImplemented
        return np.allclose(self.local, other.local, atol=1e-9)

    def __add__(self, other: Any) -> 'NZA':
        &quot;&quot;&quot;⊕ Addition: ν₁ ⊕ ν₂ = (λ₁ + λ₂)_local + ∞_universe. Commutative, associative (ℤ).&quot;&quot;&quot;
        if not isinstance(other, NZA):
            other = NZA(other)
        return NZA(self.local + other.local)

    __radd__ = __add__

    def __sub__(self, other: Any) -> 'NZA':
        &quot;&quot;&quot;⊖ Subtraction: ν₁ ⊖ ν₂ = (λ₁ - λ₂)_local + ∞_universe. Preserves total ∞ (Axiom 1).&quot;&quot;&quot;
        if not isinstance(other, NZA):
            other = NZA(other)
        return NZA(self.local - other.local)

    def __rsub__(self, other) -> 'NZA':
        return NZA(other) - self

    def __mul__(self, other: Any) -> 'NZA':
        &quot;&quot;&quot;⊗ Multiplication: ν₁ ⊗ ν₂ = (λ₁ · λ₂)_local + ∞_universe. Distributive over ⊕.&quot;&quot;&quot;
        if not isinstance(other, NZA):
            other = NZA(other)
        return NZA(self.local * other.local)

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> 'NZA':
        &quot;&quot;&quot;Division: ν₁ / ν₂ = (λ₁ / λ₂)_local + ∞_universe; 1/0 → ∞_density (paper Sec 2.1).&quot;&quot;&quot;
        if not isinstance(other, NZA):
            other = NZA(other)
        if np.isclose(other.local, 0, atol=1e-9).any():
            return NZA(np.full_like(self.local, np.inf))
        return NZA(self.local / other.local)

    def __rtruediv__(self, other) -> 'NZA':
        return NZA(other) / self

    def __neg__(self) -> 'NZA':
        return NZA(-self.local)

    def __pos__(self) -> 'NZA':
        return self

    @classmethod
    def zero(cls) -> 'NZA':
        &quot;&quot;&quot;Additive identity: 0_local + ∞_universe (no true zero, Theorem 2).&quot;&quot;&quot;
        return cls(0)

    @classmethod
    def infinity(cls) -> 'NZA':
        &quot;&quot;&quot;Division by zero: ∞_density + ∞_universe.&quot;&quot;&quot;
        return cls(np.inf)


__version__ = "0.1.0"
__all__ = ["NZA"]