---
title: "Optimización Estocástica"
---

# Optimización Estocástica

> *"The future ain't what it used to be."*
> — Yogi Berra

---

## De determinista a estocástica

En el módulo 07, optimizábamos funciones deterministas: dado $x$, el valor $f(x)$ es conocido. Pero en la vida real, el resultado de una decisión depende de factores inciertos.

La transición es directa:

| Optimización determinista (mod 07) | Optimización estocástica (mod 09) |
|-------------------------------------|-------------------------------------|
| $\min_x f(x)$ | $\min_x E_\theta[f(x, \theta)]$ |
| Variables de decisión $x$ | Variables de decisión $x$ |
| Resultado conocido $f(x)$ | Resultado aleatorio $f(x, \theta)$ |
| Una solución $x^{∗}$ | Una solución $x^{∗}$ (o una política $\pi$) |
| Restricciones $g(x) \leq 0$ | Restricciones pueden ser estocásticas |

Aquí $\theta$ representa la incertidumbre — un estado del mundo que no controlamos. Lo que la sección 9.1 llamaba $S$ (estados), aquí lo llamamos $\theta$ para mantener la notación de optimización.

**La conexión:** La teoría de la decisión bajo riesgo *es* optimización estocástica con $f(x, \theta) = -U(x, \theta)$ (negamos porque optimización suele minimizar).

---

## El problema del vendedor de periódicos

El **newsvendor problem** es el ejemplo canónico de optimización estocástica. Es elegante porque tiene solución cerrada y conecta predicción con decisión.

### Planteamiento

Un vendedor debe decidir cuántos periódicos ordenar ($q$) **antes** de saber la demanda ($D$):

- Si ordena **de más** ($q > D$): pierde $c_o$ por cada periódico sobrante (*overage cost*)
- Si ordena **de menos** ($q < D$): pierde $c_u$ por cada cliente no atendido (*underage cost*)

El objetivo es minimizar el costo esperado:

$$\min_q \; E_D\left[c_o \cdot \max(q - D, 0) + c_u \cdot \max(D - q, 0)\right]$$

### Solución

La cantidad óptima es:

$$q^{∗} = F^{-1}\left(\frac{c_u}{c_o + c_u}\right)$$

donde $F$ es la **función de distribución acumulada** de la demanda $D$.

**La fracción $c_u / (c_o + c_u)$ se llama *critical ratio*** — es la probabilidad de que la demanda no exceda $q^{∗}$.

![Problema del newsvendor]({{ '/09_teoria_decision/images/08_newsvendor.png' | url }})

### ¿De dónde sale $F$?

De la **predicción** (mod 08). Si tienes un modelo que predice la distribución de demanda $P(D \mid X)$ dado features $X$ (día de la semana, clima, eventos), entonces $F$ es la CDF de esa distribución condicional.

**Conexión completa:**
1. **Predicción** te da $P(D \mid X)$ → la distribución $F$
2. **Decisión** usa $F$ para calcular $q^{∗}$
3. **Optimización** minimiza el costo esperado

Si mejoras tu modelo predictivo (mejor $F$), reduces tu costo esperado. Pero solo vale la pena si la mejora en $F$ **cambia** la decisión $q^{∗}$.

:::example{title="Newsvendor con Normal"}
Demanda $D \sim N(50, 15^2)$, costo exceso $c_o = 2$, costo escasez $c_u = 7$.

Ratio crítico: $c_u / (c_o + c_u) = 7/9 \approx 0.778$

$q^{∗} = F^{-1}(0.778) = 50 + 15 \times \Phi^{-1}(0.778) \approx 50 + 15 \times 0.765 \approx 61.5$

Ordena ~62 periódicos. Nota que $q^{∗} > E[D] = 50$ porque el costo de escasez es mayor que el de exceso.
:::

:::exercise{title="Varía los costos"}
¿Qué pasa con $q^{∗}$ si:
1. $c_o = c_u$? (costos simétricos)
2. $c_u \gg c_o$? (escasez es mucho peor)
3. $c_o \gg c_u$? (exceso es mucho peor)

¿Cómo se relaciona con aversión al riesgo?
:::

---

## Políticas

En optimización determinista, la solución es un **número** $x^{∗}$. En optimización estocástica, la solución puede ser una **función** — una **política**:

$$\pi: S \to A$$

que mapea cada estado observado a una acción.

### ¿Por qué funciones en vez de números?

Porque podemos **observar información** antes de decidir. En el newsvendor:
- Sin información: la política es un número fijo $q^{∗}$ (misma orden cada día)
- Con features $X$: la política es $q^{∗}(X) = F^{-1}_{D \mid X}(c_u / (c_o + c_u))$ (ajusta según el contexto)

| Tipo de solución | Cuándo | Ejemplo |
|-----------------|--------|---------|
| Acción fija $a^{∗}$ | No observas nada antes de decidir | Ordenar 62 periódicos siempre |
| Política $\pi(x)$ | Observas features antes de decidir | Ordenar $\pi(\text{lunes, lluvia}) = 45$, $\pi(\text{viernes, sol}) = 70$ |

Las políticas son un concepto central en **procesos de decisión de Markov** (MDPs) y **aprendizaje por refuerzo** — módulos futuros.

---

## Varianza, riesgo y robustez

Maximizar $E[U]$ no siempre es suficiente. A veces nos importa la **dispersión** de los resultados.

### Tradeoff media-varianza

En finanzas, el objetivo clásico de Markowitz es:

$$\max_w \; E[R_p] - \lambda \cdot \text{Var}(R_p)$$

donde $w$ son los pesos del portafolio, $R_p = w^T R$ es el retorno del portafolio, y $\lambda > 0$ controla la aversión al riesgo.

![Frontera eficiente]({{ '/09_teoria_decision/images/09_mean_variance_frontier.png' | url }})

- $\lambda = 0$: solo maximiza retorno (ignora riesgo)
- $\lambda \to \infty$: solo minimiza varianza (ignora retorno)
- $\lambda$ intermedio: tradeoff

La **frontera eficiente** es el conjunto de portafolios que no pueden mejorar en retorno sin empeorar en riesgo (ni viceversa). Es una curva de Pareto — exactamente el concepto de optimización multiobjetivo del mod 07.

### Value at Risk (VaR)

$$\text{VaR}_\alpha = -Q_\alpha[R]$$

El VaR al nivel $\alpha$ es la pérdida máxima que esperas con probabilidad $1 - \alpha$. Ejemplo: "Con 95% de confianza, no perderás más de &#36;10,000".

### Optimización robusta

Cuando no confías en la distribución $P(\theta)$, puedes optimizar para el peor caso:

$$\min_x \max_{\theta \in \Theta} f(x, \theta)$$

Esto es el **maximin** de la sección 9.3, pero formulado como problema de optimización. No necesita probabilidades — solo un *conjunto* de escenarios posibles $\Theta$.

| Enfoque | Necesita $P(\theta)$ | Actitud |
|---------|----------------------|---------|
| **Estocástico** ($\min E[f]$) | Sí | Neutral al modelo |
| **Media-varianza** | Sí | Averso al riesgo |
| **Robusto** ($\min\max f$) | No | Pesimista |

---

## Monte Carlo: cuando no hay fórmulas cerradas

¿Qué pasa cuando $E[f(x, \theta)]$ no tiene solución analítica? Usamos **aproximación por muestreo** (Sample Average Approximation, SAA):

$$E_\theta[f(x, \theta)] \approx \frac{1}{N} \sum_{i=1}^{N} f(x, \theta_i), \quad \theta_i \sim P(\theta)$$

El algoritmo:
1. Genera $N$ muestras $\theta_1, \ldots, \theta_N$ de $P(\theta)$
2. Para cada $x$ candidato, evalúa el promedio $\frac{1}{N} \sum_i f(x, \theta_i)$
3. Minimiza este promedio (usando los algoritmos del mod 07)

Es la unión de Monte Carlo (mod 05) + optimización (mod 07).

:::exercise{title="SAA para el newsvendor"}
Si en vez de asumir $D \sim N(50, 15^2)$, solo tienes datos históricos $d_1, \ldots, d_{100}$:
1. ¿Cómo usarías SAA para encontrar $q^{∗}$?
2. ¿Qué tan grande debe ser $N$ para una buena aproximación?
3. ¿Es esto equivalente a usar la CDF empírica en la fórmula cerrada?
:::

---

**Anterior:** [Decidir bajo incertidumbre](03_decidir_bajo_incertidumbre.md) | **Siguiente:** [El agente que decide →](05_el_agente_que_decide.md)
