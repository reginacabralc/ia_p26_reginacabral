# Ejercicio: El Fraude del Value at Risk (VaR)

## Objetivo

1. Demostrar **empíricamente** por qué el VaR paramétrico falla
2. Aprender a **diagnosticar** fat tails en datos financieros
3. Implementar **alternativas robustas** al VaR normal

---

## El Problema

El VaR (Value at Risk) es LA métrica de riesgo más usada en finanzas. Pero tiene un problema fundamental.

### Definición Formal

$$\text{VaR}\_\alpha = -Q\_{1-\alpha}(\mathcal{R})$$

donde $Q_p$ es el cuantil p de los retornos R.

**En palabras:**
- VaR₉₉ = "El 99% de los días, no perderemos más que esta cantidad"
- VaR₉₅ = "El 95% de los días, no perderemos más que esta cantidad"

### Cómo se Calcula: Método Paramétrico (Normal)

Asumiendo $R \sim \mathcal{N}(\mu, \sigma^2)$:

$$\text{VaR}\_\alpha = -(\mu + z\_{1-\alpha} \cdot \sigma)$$

donde $z_{1-\alpha}$ es el cuantil de la normal estándar:
- VaR₉₉: $z_{0.01} = -2.326$
- VaR₉₅: $z_{0.05} = -1.645$

### El Problema Fundamental

Si los retornos son **fat-tailed** (α ≈ 3 para acciones):

1. **Subestima la frecuencia** de violaciones
2. **Subestima la severidad** de las pérdidas
3. Da **falsa sensación de seguridad**

---

## ¿Por qué Student-t NO es la Solución?

⚠️ **ADVERTENCIA CRÍTICA:**

| Aspecto | Normal | Student-t | Pareto (real) |
|---------|--------|-----------|---------------|
| Colas | Exponencial | $\sim t^{-\nu-1}$ | $\sim x^{-\alpha}$ |
| Decaimiento | Muy rápido | Rápido | Lento |
| Eventos extremos | "Imposibles" | Raros | Frecuentes |

**Student-t subestima los eventos extremos porque sus colas decaen más rápido que power law.**

---

## Metodología del Ejercicio

### PASO 1: Diagnóstico de Fat Tails

Antes de calcular VaR, diagnosticar la distribución:

```python
# 1. Estimar α con Hill
alpha = hill_estimator(returns)

# 2. Calcular κ de Taleb
kappa = np.max(np.abs(returns)) / np.sum(np.abs(returns))

# 3. Contar eventos extremos
for k in [3, 4, 5, 6]:
    obs = (np.abs(z_scores) > k).sum()
    esp = len(returns) * 2 * (1 - stats.norm.cdf(k))
    print(f">{k}σ: obs={obs}, esp={esp:.1f}, ratio={obs/esp:.1f}x")
```

**Interpretación:**
- α ≈ 3 para S&P 500 → varianza finita pero kurtosis infinita
- VaR normal subestima ~50-100x los eventos >4σ

### PASO 2: Calcular VaR con Diferentes Métodos

El script compara 4 métodos:

| Método | Descripción | Asunciones |
|--------|-------------|------------|
| **Normal** | $-(\mu + z\sigma)$ | Normalidad |
| **Histórico** | Percentil empírico | Ninguna |
| **Cornish-Fisher** | Ajuste por skew y kurt | Momentos finitos |
| **EVT (GPD)** | Extreme Value Theory | Cola sigue GPD |

```python
# Normal (paramétrico)
VaR_normal = -(mu + stats.norm.ppf(0.01) * sigma)

# Histórico (no paramétrico)
VaR_hist = -np.percentile(returns, 1)

# EVT con GPD (Generalized Pareto)
# Modela solo la cola, más robusto
```

### PASO 3: Backtesting

Para cada método, calcular:
- Tasa de violación (esperada vs real)
- Severidad de violaciones (cuánto excede el VaR)

```python
# Una violación = pérdida > VaR predicho
violacion = -retorno_real > VaR_predicho

# Severidad = qué tan mal falla cuando falla
severidad = (-retorno_real - VaR_predicho) / VaR_predicho
```

**Métricas:**
- VaR₉₉ debería tener ~1% de violaciones
- Si tiene 2-5%, el modelo subestima riesgo

### PASO 4: Análisis de Eventos Extremos

Identificar los peores días y calcular cuántas "sigmas" representan:

```python
z_scores = (returns - mu) / sigma
worst_days = z_scores.nsmallest(20)
```

**Cita clave:**
> "We were seeing things that were 25-standard deviation moves, several days in a row."
> — David Viniar, CFO Goldman Sachs, agosto 2007

Si tu modelo dice 25σ, el problema es tu modelo.

---

## Lo Que Harás

### Parte A: Diagnóstico

1. Correr el script y examinar el diagnóstico de colas
2. Llenar la tabla:

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| α̂ (Hill) | ~? | ¿α > 2? ¿α > 4? |
| Eventos >4σ obs/esp | ~?x | ¿Cuánto subestima Normal? |
| Test Jarque-Bera | p < 0.05? | ¿Rechazamos normalidad? |

### Parte B: Comparar Métodos de VaR

Llenar tabla de backtesting:

| Método | Violaciones | Tasa | Esperada (1%) | Ratio |
|--------|-------------|------|---------------|-------|
| Normal | ? | ?% | 1% | ?x |
| Histórico | ? | ?% | 1% | ?x |
| Cornish-Fisher | ? | ?% | 1% | ?x |
| EVT | ? | ?% | 1% | ?x |

### Parte C: Severidad

¿Qué método tiene menor severidad promedio cuando falla?

| Método | Severidad promedio |
|--------|-------------------|
| Normal | ?% |
| Histórico | ?% |
| EVT | ?% |

---

## ¿Qué Hacer? Alternativas Robustas

### 1. VaR Histórico (Mínimo Viable)

```python
def var_historico(returns, alpha=0.99):
    return -np.percentile(returns, (1-alpha)*100)
```

**Pros:** No asume distribución
**Contras:** Limitado por datos históricos

### 2. VaR con EVT (Más Robusto)

```python
from scipy.stats import genpareto

def var_evt(returns, alpha=0.99, threshold_pct=90):
    losses = -returns
    u = np.percentile(losses, threshold_pct)
    excesses = losses[losses > u] - u
    
    # Ajustar GPD a los excesos
    params = genpareto.fit(excesses)
    c, loc, scale = params
    
    # Calcular VaR
    n, n_u = len(losses), len(excesses)
    Fu = n_u / n
    p = 1 - alpha
    
    var = u + (scale/c) * ((p/Fu)**(-c) - 1)
    return var
```

### 3. Expected Shortfall (ES)

```python
def expected_shortfall(returns, alpha=0.99):
    var = var_historico(returns, alpha)
    return -returns[returns < -var].mean()
```

**ES responde:** "Cuando perdemos más que VaR, ¿cuánto perdemos en promedio?"

### 4. Stress Testing

No confiar solo en métricas. Simular escenarios:
- ¿Qué pasa si mañana hay un -20%?
- ¿Sobrevivimos un 2008?
- ¿Qué si hay 3 días seguidos de -5%?

---

## Código de Adaptación Completo

```python
import numpy as np
from scipy import stats

def analisis_riesgo_robusto(returns):
    """
    Framework robusto para análisis de riesgo con fat tails.
    """
    
    # === PASO 1: DIAGNÓSTICO ===
    alpha = hill_estimator(returns)
    print(f"Índice de cola α̂ = {alpha:.2f}")
    
    if alpha <= 2:
        print("⚠️ VARIANZA INFINITA - métodos clásicos inválidos")
    elif alpha <= 4:
        print("⚡ Fat-tailed - usar métodos robustos")
    else:
        print("✓ Casi normal - métodos clásicos aceptables")
    
    # === PASO 2: MEDIDAS DE RIESGO ===
    
    # NO usar:
    # var_normal = -(returns.mean() + stats.norm.ppf(0.01) * returns.std())
    
    # SÍ usar:
    var_hist_99 = -np.percentile(returns, 1)
    var_hist_95 = -np.percentile(returns, 5)
    
    es_99 = -returns[returns < -var_hist_99].mean()
    es_95 = -returns[returns < -var_hist_95].mean()
    
    print(f"\nMedidas de riesgo (robustas):")
    print(f"  VaR 99% (histórico): {var_hist_99*100:.2f}%")
    print(f"  VaR 95% (histórico): {var_hist_95*100:.2f}%")
    print(f"  ES 99%: {es_99*100:.2f}%")
    print(f"  ES 95%: {es_95*100:.2f}%")
    
    # === PASO 3: STRESS TEST ===
    worst_day = returns.min()
    worst_week = returns.rolling(5).sum().min()
    worst_month = returns.rolling(22).sum().min()
    
    print(f"\nEscenarios históricos extremos:")
    print(f"  Peor día: {worst_day*100:.2f}%")
    print(f"  Peor semana: {worst_week*100:.2f}%")
    print(f"  Peor mes: {worst_month*100:.2f}%")
    
    return {
        'alpha': alpha,
        'var_99': var_hist_99,
        'var_95': var_hist_95,
        'es_99': es_99,
        'es_95': es_95
    }
```

---

## Preguntas de Reflexión

1. **¿Por qué el VaR normal subestima el riesgo?** Relaciona con α ≈ 3.

2. **¿Por qué el VaR histórico funciona mejor?** ¿Tiene limitaciones?

3. **David Viniar dijo "25 sigmas". ¿Qué debería haber concluido?**

4. **¿Por qué Expected Shortfall es mejor que VaR para fat tails?**

5. **Si α = 2.5 para tus datos, ¿puedes usar la varianza para medir riesgo?**

6. **¿Cómo harías stress testing si no hay datos históricos de crisis?**

---

## Ejecutar

```bash
cd clase/05_probabilidad/ejercicios
source .venv/bin/activate
python ejercicio_var.py
```

El script generará:
- Diagnóstico de colas con α̂
- Tabla de backtesting por método
- `var_backtesting.png`: Comparación visual de métodos
- `var_eventos_extremos.png`: Los peores días y sus "sigmas"

---

## Conexión con la Crisis de 2008

El VaR paramétrico fue uno de los culpables:
- Los bancos pensaban que tenían el riesgo "controlado"
- Los modelos decían que ciertos eventos eran "imposibles"
- Cuando ocurrieron los "imposibles", el sistema colapsó

**Lección:** No confíes en modelos que subestiman las colas.

---

## Referencia

- Taleb, N.N. (2020). *Statistical Consequences of Fat Tails*
- Taleb, N.N. (2007). *The Black Swan*
- Embrechts, P. et al. (1997). *Modelling Extremal Events*
