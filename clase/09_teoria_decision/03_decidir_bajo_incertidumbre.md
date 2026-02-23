---
title: "Decidir Bajo Incertidumbre"
---

# Decidir Bajo Incertidumbre

> *"In any moment of decision, the best thing you can do is the right thing. The worst thing you can do is nothing."*
> — Theodore Roosevelt

---

## El principio de Máxima Utilidad Esperada (MEU)

Si aceptamos los axiomas vNM (sección anterior), la forma racional de decidir bajo riesgo es:

$$a^{∗} = \arg\max_{a \in A} \sum_{s \in S} P(s) \cdot U(o(a, s))$$

o más compactamente:

$$a^{∗} = \arg\max_{a \in A} \; E_S[U(a, S)]$$

**Observación clave:** Esto es optimización (mod 07), pero con un ingrediente nuevo — la probabilidad. En lugar de maximizar $f(x)$ directamente, maximizamos el *promedio ponderado* de $U$ sobre los posibles estados.

| Componente | Viene de... |
|-----------|------------|
| $\arg\max$ | Optimización (mod 07) |
| $P(s)$ | Probabilidad (mod 05) |
| $U(o(a,s))$ | Preferencias (sección 9.2) |
| $P(s)$ estimado | Predicción (mod 08) |

:::example{title="Paraguas con MEU"}
Con $P(\text{Lluvia}) = 0.4$, $P(\text{Sol}) = 0.6$:

$E[U(\text{Llevar})] = 0.4 \times 8 + 0.6 \times 5 = 3.2 + 3.0 = 6.2$

$E[U(\text{No llevar})] = 0.4 \times 1 + 0.6 \times 10 = 0.4 + 6.0 = 6.4$

$a^{∗} = \text{No llevar}$ (6.4 > 6.2)

Pero si $P(\text{Lluvia}) = 0.7$:

$E[U(\text{Llevar})] = 0.7 \times 8 + 0.3 \times 5 = 5.6 + 1.5 = 7.1$

$E[U(\text{No llevar})] = 0.7 \times 1 + 0.3 \times 10 = 0.7 + 3.0 = 3.7$

$a^{∗} = \text{Llevar}$ (7.1 > 3.7)

El **punto de cruce** es el valor de $p$ donde ambas acciones son equivalentes. ¿Puedes calcularlo?
:::

---

## Árboles de decisión

Cuando las decisiones son **secuenciales** (una decisión depende de información revelada después de la primera), usamos **árboles de decisión**.

### Elementos del árbol

| Nodo | Forma | Significado |
|------|-------|-------------|
| **Decisión** | Cuadrado | El agente elige |
| **Azar** | Círculo | La naturaleza "elige" (probabilidades) |
| **Terminal** | Valor | Utilidad del resultado final |

### Inducción hacia atrás (backward induction)

Para resolver un árbol de decisión:

1. **Empieza por las hojas** (resultados terminales).
2. **En cada nodo de azar:** calcula la utilidad esperada (promedio ponderado de hijos).
3. **En cada nodo de decisión:** elige la rama con mayor utilidad esperada.
4. **Propaga hacia la raíz.**

![Árbol de decisión]({{ '/09_teoria_decision/images/05_decision_tree.png' | url }})

:::example{title="Perforación petrolera"}
1. **Decisión 1:** ¿Perforar o no?
   - No perforar → &#36;0k
   - Perforar → costo de &#36;100k + incertidumbre

2. **Azar 1:** ¿Hay petróleo? ($p = 0.3$)
   - Seco ($p = 0.7$) → -&#36;100k
   - Petróleo ($p = 0.3$) → Decisión 2

3. **Decisión 2:** ¿Pozo grande o chico?
   - Pozo chico → &#36;300k
   - Pozo grande → Azar 2

4. **Azar 2:** ¿Alto o bajo rendimiento? ($p = 0.5$ cada uno)
   - Alto → &#36;800k
   - Bajo → &#36;200k

**Resolución (hacia atrás):**
- Azar 2: $EU = 0.5 \times 800 + 0.5 \times 200 = 500$
- Decisión 2: $\max(500, 300) = 500$ → Pozo grande
- Azar 1: $EU = 0.3 \times 500 + 0.7 \times (-100) = 150 - 70 = 80$
- Decisión 1: $\max(80, 0) = 80$ → Perforar

**Respuesta:** Perforar, y si hay petróleo, hacer pozo grande. $EU = 80k$.
:::

---

## Redes de decisión

Las redes de decisión (influence diagrams) son una extensión de las redes Bayesianas que incorporan decisiones y utilidades:

| Tipo de nodo | Forma | Significado |
|-------------|-------|-------------|
| **Azar** (chance) | Óvalo | Variable aleatoria (como en Bayes nets) |
| **Decisión** | Rectángulo | Variable que el agente controla |
| **Utilidad** | Diamante | Función de utilidad (depende de otros nodos) |

Las flechas representan:
- **Hacia nodos de azar:** dependencias probabilísticas
- **Hacia nodos de decisión:** información disponible al decidir
- **Hacia nodos de utilidad:** variables que afectan la utilidad

La ventaja sobre árboles: representación compacta cuando hay muchas variables. Un árbol con 5 variables binarias tiene $2^5 = 32$ hojas; una red tiene 5 nodos.

---

## Valor de la Información

Una de las preguntas más poderosas en teoría de la decisión es: **¿cuánto vale obtener más información antes de decidir?**

### Definición

$$\text{VoI}(E) = EU(\text{con info } E) - EU(\text{sin info})$$

donde $EU(\text{con info } E)$ significa: primero observamos $E$, luego decidimos óptimamente.

**Propiedad fundamental:** $\text{VoI}(E) \geq 0$ — la información nunca tiene valor negativo (siempre puedes ignorarla).

### Valor de la Información Perfecta (VPI)

Si pudiéramos saber *exactamente* qué estado ocurrirá antes de decidir:

$$\text{VPI} = \left(\sum_{s} P(s) \cdot \max_a U(a, s)\right) - \max_a E[U(a)]$$

El primer término es la EU cuando podemos adaptar nuestra acción a cada estado. El segundo es la EU cuando debemos elegir una acción fija.

![Valor de la Información]({{ '/09_teoria_decision/images/06_voi_medical.png' | url }})

:::example{title="VoI en diagnóstico médico"}
Con $P(\text{enfermo}) = 0.1$:

**Sin información:**
- $EU(\text{Tratar}) = 0.1 \times 150 + 0.9 \times (-50) = -30$
- $EU(\text{No tratar}) = 0.1 \times (-200) + 0.9 \times 0 = -20$
- Mejor: No tratar ($EU = -20$)

**Con información perfecta:**
- Si enfermo ($p = 0.1$): tratar ($150 > -200$)
- Si sano ($p = 0.9$): no tratar ($0 > -50$)
- $EU = 0.1 \times 150 + 0.9 \times 0 = 15$

$\text{VPI} = 15 - (-20) = 35$

Un test diagnóstico perfecto vale 35 unidades de utilidad. Si el test cuesta menos que eso, **vale la pena hacerlo**.
:::

### Cuándo obtener más datos vs actuar ahora

El VoI da una respuesta cuantitativa a esta pregunta:

| Situación | VoI | Acción |
|-----------|-----|--------|
| Info no cambia la decisión | $\text{VoI} = 0$ | Actuar ahora |
| Info podría cambiar la decisión | $\text{VoI} > 0$ | Evaluar costo de info vs VoI |
| Costo de info $<$ VoI | — | Obtener más datos |
| Costo de info $>$ VoI | — | Actuar con lo que sabes |

**Implicación para ML:** Un modelo predictivo solo tiene valor si **cambia la decisión** que tomarías sin él. Un modelo con 95% de accuracy puede tener $\text{VoI} = 0$ si la decisión óptima es la misma con o sin la predicción.

---

## Criterios sin probabilidades

Cuando no tenemos (o no confiamos en) las probabilidades, usamos criterios de decisión bajo ignorancia.

### Maximin (Wald)

$$a^{∗} = \arg\max_{a \in A} \min_{s \in S} U(a, s)$$

**Filosofía:** Pesimista. Prepárate para el peor caso. Elige la acción cuyo peor resultado es el menos malo.

### Minimax regret (Savage)

Primero, calcula el *regret* (arrepentimiento) de cada combinación $(a, s)$:

$$R(a, s) = \max_{a'} U(a', s) - U(a, s)$$

Luego minimiza el máximo regret:

$$a^{∗} = \arg\min_{a \in A} \max_{s \in S} R(a, s)$$

**Filosofía:** No te preocupa el peor *resultado*, sino el peor *arrepentimiento* — la diferencia entre lo que obtuviste y lo que *hubieras podido* obtener.

### MEU vs Maximin: diferentes criterios, diferentes decisiones

![MEU vs Maximin]({{ '/09_teoria_decision/images/07_maximin_vs_meu.png' | url }})

| Criterio | Cuándo usarlo |
|----------|---------------|
| **MEU** | Tienes probabilidades confiables y puedes repetir la decisión muchas veces |
| **Maximin** | Las consecuencias del peor caso son inaceptables (seguridad, medicina) |
| **Minimax regret** | No tienes probabilidades pero quieres evitar decisiones "obvialmente malas" |

:::exercise{title="Compara los criterios"}
Dada la siguiente matriz de pagos:

| | $s_1$ (boom) | $s_2$ (normal) | $s_3$ (crisis) |
|---|:---:|:---:|:---:|
| **A (agresiva)** | 100 | 40 | -50 |
| **B (conservadora)** | 30 | 35 | 10 |

1. Calcula $a^{∗}$ bajo MEU con $P = (0.3, 0.5, 0.2)$.
2. Calcula $a^{∗}$ bajo maximin.
3. Calcula la matriz de regret y $a^{∗}$ bajo minimax regret.
4. ¿Algún criterio da la misma respuesta? ¿Por qué o por qué no?
:::

---

**Anterior:** [Utilidad y preferencias racionales](02_utilidad_preferencias.md) | **Siguiente:** [Optimización estocástica →](04_optimizacion_estocastica.md)
