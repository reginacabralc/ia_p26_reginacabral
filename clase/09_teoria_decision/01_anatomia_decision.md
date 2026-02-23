---
title: "Anatomía de un Problema de Decisión"
---

# Anatomía de un Problema de Decisión

> *"El que predice sin decidir es un espectador. El que decide sin predecir es un temerario."*

---

## De predecir a decidir

El módulo anterior terminó con una observación: la predicción es una herramienta, no un fin. Un modelo que estima $P(Y \mid X)$ responde la pregunta *"¿qué va a pasar?"*, pero no responde *"¿qué debo hacer?"*.

Considera un médico con un modelo predictivo perfecto:

- El modelo dice: *"Este paciente tiene 30% de probabilidad de tener la enfermedad."*
- El médico pregunta: *"¿Lo trato o no?"*

La predicción sola no contesta. Necesitamos saber:
- ¿Qué pasa si trato y está sano? (Costos del tratamiento innecesario)
- ¿Qué pasa si no trato y está enfermo? (Consecuencias de no tratar)
- ¿Cuánto "vale" cada resultado para el paciente?

Eso es **teoría de la decisión**: un marco para combinar lo que *creemos* (probabilidades) con lo que *queremos* (utilidades) para determinar lo que *debemos hacer* (acciones).

---

## Los ingredientes

Todo problema de decisión tiene 5 componentes:

| Ingrediente | Símbolo | Significado | Ejemplo (paraguas) |
|-------------|---------|-------------|---------------------|
| **Estados** | $S$ | Lo que el mundo puede ser (no controlamos) | {Lluvia, Sol} |
| **Acciones** | $A$ | Lo que podemos hacer | {Llevar paraguas, No llevar} |
| **Resultados** | $O$ | Lo que sucede dado $(a, s)$ | "Seco con paraguas bajo lluvia" |
| **Creencias** | $P(S)$ | Probabilidad sobre estados | $P(\text{Lluvia}) = 0.4$ |
| **Preferencias** | $U: O \to \mathbb{R}$ | Cuánto valoramos cada resultado | $U(\text{seco}) = 8$ |

Nota la analogía con optimización (mod 07):

| Optimización (mod 07) | Decisión (mod 09) |
|------------------------|-------------------|
| Variables de decisión $x$ | Acciones $A$ |
| Función objetivo $f(x)$ | Utilidad esperada $E[U(a)]$ |
| Restricciones $g(x) \leq 0$ | Acciones factibles |
| — | Estados $S$ (novedad) |
| — | Creencias $P(S)$ (novedad) |

La diferencia clave: en optimización, el resultado de elegir $x$ es determinista ($f(x)$). En decisión, el resultado depende del *estado del mundo*, que es incierto.

---

## Matriz de decisión

La forma más simple de representar un problema de decisión es una **matriz de pagos** (payoff matrix):

![Matriz de decisión]({{ '/09_teoria_decision/images/01_decision_matrix.png' | url }})

Las filas son acciones, las columnas son estados, y cada celda contiene la utilidad $U(a, s)$.

:::example{title="El paraguas"}
| | Lluvia | Sol |
|---|:---:|:---:|
| **Llevar paraguas** | 8 (seco, manos ocupadas) | 5 (seco, cargando innecesario) |
| **No llevar** | 1 (empapado) | 10 (libre, día perfecto) |

- Si sabemos que llueve → llevar (8 > 1).
- Si sabemos que habrá sol → no llevar (10 > 5).
- Si **no sabemos**... necesitamos las probabilidades.
:::

:::example{title="Test médico"}
| | Enfermo ($p = 0.1$) | Sano ($p = 0.9$) |
|---|:---:|:---:|
| **Tratar** | 150 (beneficio - costo) | -50 (solo costo) |
| **No tratar** | -200 (enfermedad avanza) | 0 (nada pasa) |

¿Tratar o no? Depende de cuánto pesamos cada escenario.
:::

---

## Tres regímenes de decisión

No todos los problemas de decisión son iguales. Dependiendo de cuánto sabemos sobre los estados, estamos en uno de tres regímenes:

![Tres regímenes]({{ '/09_teoria_decision/images/02_three_regimes.png' | url }})

### 1. Certeza: sabemos qué estado ocurrirá

Si sabemos que llueve, el problema colapsa a:

$$a^{∗} = \arg\max_{a \in A} U(a, s_{\text{conocido}})$$

Esto es **optimización determinista** — exactamente lo que vimos en el módulo 07. No necesitamos probabilidades.

### 2. Riesgo: conocemos $P(S)$

Si $P(\text{Lluvia}) = 0.4$, podemos calcular la **utilidad esperada** de cada acción:

$$E[U(a)] = \sum_{s \in S} P(s) \cdot U(a, s)$$

Y elegir la acción que maximiza:

$$a^{∗} = \arg\max_{a \in A} E[U(a)]$$

Este es el **principio de máxima utilidad esperada** (MEU) — el corazón de este módulo.

### 3. Ignorancia: no conocemos $P(S)$

Si no tenemos probabilidades (o no confiamos en ellas), usamos criterios alternativos:

| Criterio | Fórmula | Filosofía |
|----------|---------|-----------|
| **Maximin** (Wald) | $a^{∗} = \arg\max_a \min_s U(a, s)$ | Pesimista: maximizar el peor caso |
| **Minimax regret** (Savage) | $a^{∗} = \arg\min_a \max_s R(a, s)$ | Minimizar el arrepentimiento máximo |
| **Maximax** | $a^{∗} = \arg\max_a \max_s U(a, s)$ | Optimista: maximizar el mejor caso |

Donde el *regret* (arrepentimiento) es:

$$R(a, s) = \max_{a'} U(a', s) - U(a, s)$$

Es decir: la diferencia entre lo que obtuve y lo que hubiera obtenido con la mejor acción *ex post*.

---

## Receta para formular un problema de decisión

Análoga a la receta de formulación del módulo 07:

1. **¿Qué no controlo?** → Identifica los estados $S$
2. **¿Qué controlo?** → Identifica las acciones $A$
3. **¿Qué resulta?** → Define los resultados $O = O(a, s)$
4. **¿Qué creo?** → Asigna probabilidades $P(S)$ (si las tienes)
5. **¿Qué prefiero?** → Define utilidades $U: O \to \mathbb{R}$

:::exercise{title="Formula la decisión"}
Un inversionista puede poner su dinero en acciones o bonos. El mercado puede estar en boom, estable, o en crisis. Formula:
- ¿Cuáles son los estados $S$?
- ¿Cuáles son las acciones $A$?
- ¿Cómo asignarías probabilidades?
- ¿Cómo definirías las utilidades?
:::

---

**Anterior:** [Índice del módulo](00_index.md) | **Siguiente:** [Utilidad y preferencias racionales →](02_utilidad_preferencias.md)
