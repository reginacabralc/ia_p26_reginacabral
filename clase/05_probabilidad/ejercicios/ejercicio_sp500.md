# Ejercicio: Los Eventos Imposibles del S&P 500

## Objetivo

1. Demostrar que los retornos financieros **NO** siguen una distribución normal
2. Aprender a **detectar** y **estimar** fat tails en datos reales
3. Entender **qué hacer** cuando confirmamos fat tails

---

## Contexto Teórico

### La Hipótesis de Mercados Eficientes y Normalidad

Durante décadas, la teoría financiera asumió que los retornos de acciones siguen una distribución normal (o log-normal). Esta suposición es conveniente porque:

1. La normal está completamente caracterizada por μ y σ
2. El TLC sugiere que sumas de muchos factores → normal
3. Permite fórmulas cerradas (Black-Scholes, VaR, etc.)

### El Problema

Si los retornos fueran normales:

| Evento | Probabilidad | Frecuencia esperada |
|--------|--------------|---------------------|
| > 3σ | 0.27% | 1 vez cada ~370 días (~1.5 años) |
| > 4σ | 0.006% | 1 vez cada ~15,800 días (~63 años) |
| > 5σ | 0.00006% | 1 vez cada ~1.7 millones de días (~6,900 años) |
| > 6σ | 2×10⁻⁷% | 1 vez cada ~500 millones de días (~1.4 millones de años) |

Un evento de 6σ debería ocurrir aproximadamente **una vez desde que existían los dinosaurios**.

### La Realidad

El Lunes Negro (19 de octubre de 1987), el S&P 500 cayó **22.6%** en un solo día. Con la volatilidad histórica de ~1% diario, esto es un evento de aproximadamente **20-25 sigmas**.

La probabilidad de un evento de 20σ en una distribución normal es aproximadamente $10^{-88}$. Para contexto, hay aproximadamente $10^{80}$ átomos en el universo observable.

**O los modelos están mal, o presenciamos un milagro estadístico.**

---

## Metodología: Paso a Paso

### PASO 1: Obtener y Preparar Datos

```python
# Descargar datos
data = yf.download("^GSPC", start="1950-01-01")
returns = np.log(data['Close'] / data['Close'].shift(1))
```

### PASO 2: Diagnósticos Visuales

El script genera automáticamente:

1. **Histograma vs Normal** (`sp500_histograma.png`)
   - Ver si las colas reales son más pesadas

2. **QQ-Plot** (`sp500_qqplot.png`)
   - Línea recta = normal
   - Curvatura en extremos = fat tails

3. **Diagnósticos de Fat Tails** (`sp500_fattails_diagnosticos.png`)
   - Log-log survival plot
   - Estimador de Hill vs k
   - Evolución de κ
   - Mean excess function

### PASO 3: Estimación de α (Índice de Cola)

El script calcula:

```python
α_hill = hill_estimator(returns)  # Típicamente α ≈ 3 para S&P500
```

**Interpretación:**
- α > 4: Casi normal (improbable para retornos)
- 2 < α ≤ 4: Varianza finita, kurtosis infinita ← **típico de acciones**
- α ≤ 2: Varianza infinita (extremo)

### PASO 4: Contar Eventos Extremos

Para cada umbral (3σ, 4σ, 5σ, 6σ):
- Contar días con retorno más extremo
- Comparar con expectativa normal
- Calcular ratio de subestimación

### PASO 5: Identificar Cisnes Negros

- Listar los 20-25 eventos más extremos
- Calcular cuántos sigmas representa cada uno
- Investigar qué pasó esos días

---

## Lo Que Harás

### Parte A: Ejecutar Diagnósticos

1. Correr el script y examinar las gráficas generadas
2. Verificar que el QQ-plot muestra curvatura
3. Confirmar que el log-log plot es aproximadamente lineal

### Parte B: Interpretar Resultados

Llenar esta tabla con los resultados del script:

| Diagnóstico | Valor | Interpretación |
|-------------|-------|----------------|
| α̂ (Hill) | ≈ ? | ¿Varianza finita? ¿Kurtosis finita? |
| κ (Taleb) | ≈ ? | ¿El máximo domina la suma? |
| Eventos >4σ observados/esperados | ? | ¿Cuántas veces subestima Normal? |
| Test Jarque-Bera p-value | ? | ¿Rechazamos normalidad? |

### Parte C: Investigar Cisnes Negros

Para los 5 eventos más extremos, investigar:

| Fecha | Retorno | Sigmas | ¿Qué pasó? |
|-------|---------|--------|------------|
| 1987-10-19 | -22.6% | ~22σ | Lunes Negro: pánico, trading automático |
| ... | ... | ... | (investigar) |

---

## ¿Qué Hacer con estos Resultados?

### Si α ≈ 3 (típico para acciones):

1. **Varianza es finita** pero puede ser inestable
2. **Kurtosis es infinita** → intervalos de confianza normales son incorrectos
3. **TLC converge muy lento** → necesitarías ~10⁶ datos para normalidad

### Acciones Concretas:

| Antes (asumiendo Normal) | Después (sabiendo Fat Tails) |
|--------------------------|------------------------------|
| Usar media como estimador | Usar **mediana** |
| IC = ±1.96σ | Usar **bootstrap** o **cuantiles empíricos** |
| VaR paramétrico | VaR **histórico** o **EVT** |
| Riesgo = σ² | Usar **Expected Shortfall** |
| Diversificar linealmente | Considerar **correlación de colas** |

### Código para Adaptaciones:

```python
# En lugar de media y desv est:
centro = np.median(returns)
dispersion = scipy.stats.median_abs_deviation(returns)

# En lugar de IC normal:
from scipy.stats import bootstrap
result = bootstrap((returns,), np.median, confidence_level=0.95)

# VaR histórico en lugar de paramétrico:
VaR_95 = -np.percentile(returns, 5)
VaR_99 = -np.percentile(returns, 1)

# Expected Shortfall:
ES_95 = -returns[returns < -VaR_95].mean()
```

---

## Preguntas de Reflexión

1. **¿Cuántos eventos "imposibles" encontraste?** ¿Cuántos de ellos ocurrieron en tu vida?

2. **Con α ≈ 3, ¿qué significa esto para la estimación de riesgo?** ¿Puedes confiar en la varianza muestral?

3. **¿Por qué el estimador de Hill se calcula solo con las observaciones más extremas?** ¿Qué pasaría si usaras todos los datos?

4. **Si trabajaras en un banco, ¿cómo explicarías a tu jefe que el VaR normal subestima el riesgo ~100x?**

5. **Investiga el Lunes Negro (1987).** ¿Qué lo causó? ¿Podría pasar de nuevo?

---

## Extensiones Sugeridas

1. **Otros activos:** Repite con Bitcoin (`BTC-USD`), oro (`GC=F`), o TSLA
   - ¿Tienen α mayor o menor que el S&P 500?

2. **Estimar α para diferentes períodos:**
   - ¿Ha cambiado α con el tiempo?
   - ¿Es diferente en bull markets vs bear markets?

3. **Comparar métodos de VaR:**
   - Calcular VaR normal, histórico, y EVT
   - Hacer backtesting: ¿cuál viola menos?

4. **Simular el impacto:**
   - Genera 10,000 años de datos con α=3 (Pareto)
   - ¿Cuántos "Lunes Negros" ocurren?

---

## Ejecutar

```bash
cd clase/05_probabilidad/ejercicios
source .venv/bin/activate
python ejercicio_sp500.py
```

El script generará:
- Diagnósticos de fat tails con α̂ y κ
- Tabla de eventos esperados vs observados
- Lista de los eventos más extremos con fechas
- 4 gráficas en `outputs/`:
  - `sp500_histograma.png`
  - `sp500_qqplot.png`
  - `sp500_eventos_tiempo.png`
  - `sp500_fattails_diagnosticos.png`
