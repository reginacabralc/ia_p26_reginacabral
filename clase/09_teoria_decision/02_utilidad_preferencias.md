---
title: "Utilidad y Preferencias Racionales"
---

# Utilidad y Preferencias Racionales

> *"The question is not whether to gamble, but how to gamble wisely."*
> — John von Neumann

---

## De preferencias a axiomas

En el módulo 05 vimos cómo Jaynes derivó la probabilidad a partir de **desiderata para creencias racionales** — si quieres que tus creencias sean consistentes, deben satisfacer los axiomas de la probabilidad.

Aquí hacemos lo mismo, pero para **preferencias**. Si quieres que tus decisiones sean consistentes, tus preferencias deben satisfacer ciertos axiomas — y de esos axiomas emerge una *función de utilidad*.

### Notación de preferencias

Dado dos resultados (o "loterías") $A$ y $B$:

| Notación | Significado |
|----------|-------------|
| $A \succ B$ | Prefieres estrictamente $A$ sobre $B$ |
| $A \prec B$ | Prefieres estrictamente $B$ sobre $A$ |
| $A \sim B$ | Eres indiferente entre $A$ y $B$ |
| $A \succeq B$ | Prefieres $A$ o eres indiferente |

### Loterías

Una **lotería** es un resultado aleatorio. Se escribe:

$$L = [S_1 : p \;;\; S_2 : 1-p]$$

que significa: "obtienes $S_1$ con probabilidad $p$, o $S_2$ con probabilidad $1 - p$".

:::example{title="Lotería del paraguas"}
$L = [\text{Seco} : 0.6 \;;\; \text{Empapado} : 0.4]$

¿Prefieres esta lotería o la certeza de estar "ligeramente húmedo"? Tu respuesta revela tus preferencias.
:::

---

## Los axiomas de von Neumann-Morgenstern

Cuatro axiomas que capturan "preferencias racionales":

### Axioma 1: Completitud

> Para cualquier par $A$, $B$: o bien $A \succeq B$, o bien $B \succeq A$ (o ambas).

**Intuición:** Siempre puedes comparar dos opciones. No existe "no sé qué prefiero" como estado permanente.

**Contraejemplo:** "¿Prefieres un helado de chocolate o una sinfonía de Beethoven?" — A veces es genuinamente difícil comparar. Pero el axioma dice que, obligado a elegir, *puedes*.

### Axioma 2: Transitividad

> Si $A \succeq B$ y $B \succeq C$, entonces $A \succeq C$.

**Intuición:** Tus preferencias no forman ciclos. Si prefieres pizza a sushi y sushi a hamburguesa, entonces prefieres pizza a hamburguesa.

**Contraejemplo (money pump):** Si $A \succ B \succ C \succ A$ (preferencias cíclicas), un agente inteligente puede sacarte dinero infinito:
1. Tienes $C$. "¿Pagas &#36;1 para cambiar a $B$?" — Sí ($B \succ C$).
2. Tienes $B$. "¿Pagas &#36;1 para cambiar a $A$?" — Sí ($A \succ B$).
3. Tienes $A$. "¿Pagas &#36;1 para cambiar a $C$?" — Sí ($C \succ A$).
4. Volviste a $C$... y perdiste &#36;3.

### Axioma 3: Continuidad

> Si $A \succ B \succ C$, existe un $p \in (0, 1)$ tal que:
> $$B \sim [A : p \;;\; C : 1-p]$$

**Intuición:** No hay resultados "infinitamente buenos" ni "infinitamente malos". Siempre existe una mezcla de probabilidades que te hace indiferente.

**Contraejemplo:** Si dices "Nunca apostaría nada que involucre muerte, sin importar la probabilidad", estás violando continuidad. (Esto puede ser razonable — los axiomas describen racionalidad *formal*, no necesariamente *humana*.)

### Axioma 4: Independencia

> Si $A \succeq B$, entonces para todo $C$ y todo $p \in (0, 1)$:
> $$[A : p \;;\; C : 1-p] \succeq [B : p \;;\; C : 1-p]$$

**Intuición:** Mezclar ambas opciones con un mismo "ruido" $C$ no cambia la preferencia. Si prefieres pizza a sushi, mezclar cada uno con una moneda al aire que da "ensalada" no debería cambiar tu ranking.

Este es el axioma más controversial — veremos que los humanos lo violan sistemáticamente.

---

## Funciones de utilidad

**Teorema (von Neumann-Morgenstern):** Si las preferencias de un agente satisfacen los 4 axiomas, entonces existe una función $U: O \to \mathbb{R}$ tal que:

$$A \succeq B \iff E[U(A)] \geq E[U(B)]$$

Además, $U$ es **única salvo transformación afín**: si $U$ representa las preferencias, entonces $V = \alpha U + \beta$ (con $\alpha > 0$) también las representa.

**Qué significa:** No necesitas comparar directamente loterías complejas. Basta asignar un número a cada resultado y comparar los promedios ponderados. La utilidad es a las preferencias lo que la probabilidad es a las creencias — una cuantificación consistente.

---

## La utilidad del dinero

¿Por qué no usar simplemente dinero como utilidad? Porque la relación entre dinero y "felicidad" no es lineal.

![Funciones de utilidad]({{ '/09_teoria_decision/images/03_utility_functions.png' | url }})

### Tres perfiles de riesgo

| Perfil | Función $U(x)$ | Forma | Comportamiento |
|--------|----------------|-------|----------------|
| **Averso al riesgo** | $\sqrt{x}$, $\ln(x)$ | Cóncava | Prefiere el valor seguro a la lotería |
| **Neutral al riesgo** | $ax + b$ | Lineal | Indiferente entre lotería y su valor esperado |
| **Buscador de riesgo** | $x^2$, $e^x$ | Convexa | Prefiere la lotería al valor seguro |

### La paradoja de San Petersburgo

Un juego ofrece: lanzas una moneda repetidamente. Si sale cara en el lanzamiento $n$, ganas $2^n$ pesos.

$$E[\text{ganancia}] = \sum_{n=1}^{\infty} \frac{1}{2^n} \cdot 2^n = \sum_{n=1}^{\infty} 1 = \infty$$

El valor esperado es *infinito*, pero nadie pagaría una cantidad infinita por jugar. ¿Por qué? Porque la **utilidad esperada** es finita:

$$E[U(\text{ganancia})] = \sum_{n=1}^{\infty} \frac{1}{2^n} \cdot U(2^n) < \infty$$

siempre que $U$ sea cóncava (crece más lento que linealmente). Daniel Bernoulli propuso $U(x) = \ln(x)$ en 1738 — la primera función de utilidad de la historia.

### La desigualdad de Jensen

Para una función cóncava $U$ y una variable aleatoria $X$:

$$U(E[X]) \geq E[U(X)]$$

Esto formaliza la aversión al riesgo: **el valor seguro** $E[X]$ da más utilidad que **la lotería** con el mismo valor esperado.

La diferencia $U(E[X]) - E[U(X)]$ es la **prima de riesgo**: cuánto estarías dispuesto a pagar para eliminar la incertidumbre.

### Equivalente cierto

El **equivalente cierto** (CE) de una lotería $L$ es la cantidad segura que te da la misma utilidad:

$$U(\text{CE}) = E[U(L)]$$

![Aversión al riesgo y equivalente cierto]({{ '/09_teoria_decision/images/04_risk_aversion_lottery.png' | url }})

- Averso al riesgo: $\text{CE} < E[L]$ (pagarías por eliminar riesgo)
- Neutral: $\text{CE} = E[L]$
- Buscador: $\text{CE} > E[L]$ (pagarías por mantener riesgo)

---

## Cuando fallan los axiomas

Los humanos violan sistemáticamente los axiomas vNM. Esto importa para IA porque:
1. Los modelos de comportamiento humano deben considerar estas desviaciones.
2. Los agentes de IA pueden ser diseñados para *no* violarlos — ser "más racionales" que los humanos.

### La paradoja de Allais (viola Independencia)

Elige entre:
- **A:** &#36;1 millón seguro
- **B:** [&#36;5M : 0.10 ; &#36;1M : 0.89 ; &#36;0 : 0.01]

La mayoría elige A (certeza).

Ahora elige entre:
- **C:** [&#36;1M : 0.11 ; &#36;0 : 0.89]
- **D:** [&#36;5M : 0.10 ; &#36;0 : 0.90]

La mayoría elige D (mayor pago esperado).

Pero elegir $A$ y $D$ es inconsistente con el axioma de independencia — si restamos la parte común $[\text{&#36;1M} : 0.89]$ de A y B, obtenemos C y D.

### Efectos de framing

Cómo describes el mismo resultado cambia la decisión:
- "Este tratamiento tiene 90% de supervivencia" → la gente lo acepta.
- "Este tratamiento tiene 10% de mortalidad" → la gente lo rechaza.

Matemáticamente idénticos, psicológicamente diferentes. Un agente de IA racional no debería tener este problema.

### ¿Por qué importa para IA?

| Si diseñas un agente... | Entonces... |
|------------------------|-------------|
| Que tome decisiones autónomas | Los axiomas vNM son tu fundamento: garantizan consistencia |
| Que modele humanos | Necesitas modelos de "racionalidad limitada" (Kahneman & Tversky) |
| Que asista humanos | Debes decidir: ¿optimizar la utilidad del humano, o la "verdadera" utilidad? |

---

**Anterior:** [Anatomía de un problema de decisión](01_anatomia_decision.md) | **Siguiente:** [Decidir bajo incertidumbre →](03_decidir_bajo_incertidumbre.md)
