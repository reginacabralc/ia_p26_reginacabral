# Ejercicio: Diagnóstico de Fat Tails (Metodología Taleb)

## Objetivo

Aprender la **metodología completa** para:
1. **Detectar** si unos datos tienen fat tails
2. **Estimar** el índice de cola α
3. **Decidir** qué hacer según el resultado

Usaremos distribuciones sintéticas donde **conocemos la respuesta** para validar los métodos.

---

## El Problema con Student-t

⚠️ **ADVERTENCIA IMPORTANTE:**

Student-t es una **trampa** como modelo de fat tails:
- Student-t(ν) tiene los mismos momentos finitos que Pareto(α=ν) para k < ν
- PERO la cola de Student-t decae como $t^{-\nu-1}$, no como $x^{-\alpha}$
- Esto significa que Student-t **subestima** los eventos extremos reales
- Usar Student-t da una **falsa sensación de seguridad**

---

## Metodología de Detección: Paso a Paso

### PASO 1: Visualización Inicial

Antes de calcular nada, siempre visualiza:

#### 1.1 Log-Log Survival Plot

```python
sorted_data = np.sort(np.abs(data))[::-1]
survival = np.arange(1, len(sorted_data)+1) / len(sorted_data)
plt.loglog(sorted_data, survival)
```

**¿Qué buscar?**
- **Línea recta** → Power law → Fat tails con α = -pendiente
- **Curva hacia abajo** → Decaimiento más rápido → Thin tails

#### 1.2 Mean Excess Function

$e(u) = E[X - u | X > u]$

**¿Qué buscar?**
- **Constante** → Exponencial (thin)
- **Creciente** → Fat tails
- **Decreciente** → Thin tails truncadas

#### 1.3 QQ-Plot vs Normal

```python
scipy.stats.probplot(data, dist="norm", plot=plt)
```

**¿Qué buscar?**
- **Línea recta** → Datos normales
- **Curvatura en los extremos** → Colas más pesadas

---

### PASO 2: Estimación Cuantitativa

#### 2.1 Estimador de Hill para α

```python
def hill_estimator(data, k=None):
    sorted_data = np.sort(np.abs(data))[::-1]
    if k is None:
        k = int(np.sqrt(len(data)))
    log_ratios = np.log(sorted_data[:k] / sorted_data[k])
    return k / np.sum(log_ratios)
```

**Importante:** Graficar α̂ vs k para ver estabilidad.

#### 2.2 Kappa de Taleb

```python
def kappa_taleb(data):
    return np.max(np.abs(data)) / np.sum(np.abs(data))
```

**Regla:** Si κ no decrece significativamente con n → fat tails.

---

### PASO 3: Interpretación

| α̂ estimado | Diagnóstico | Qué momentos existen |
|-------------|-------------|---------------------|
| > 4 | Casi thin-tailed | Media, Var, Kurtosis ✓ |
| 3-4 | Fat-tailed leve | Media, Var ✓, Kurtosis ∞ |
| 2-3 | Fat-tailed moderado | Media, Var ✓, Kurtosis ∞ |
| 1-2 | Fat-tailed severo | Media ✓, **Var ∞** |
| < 1 | Extremo | **Media ∞**, Var ∞ |

---

### PASO 4: ¿Qué Hacer?

#### Si α > 4 (Casi normal):
- Métodos clásicos funcionan razonablemente
- IC normales son aproximadamente válidos
- Pero siempre verificar con bootstrap

#### Si 2 < α ≤ 4 (Fat-tailed con varianza finita):
- **Media:** Usar mediana en lugar de promedio
- **Dispersión:** Usar MAD en lugar de desviación estándar
- **IC:** Usar bootstrap, no IC normales
- **Riesgo:** Usar Expected Shortfall, no VaR paramétrico

#### Si α ≤ 2 (Varianza infinita):
- ⚠️ **ALARMA** ⚠️
- El promedio muestral es completamente inestable
- La varianza muestral no tiene sentido
- Usar **solo cuantiles** (mediana, percentiles)
- Considerar si el modelo tiene sentido

#### Si α ≤ 1 (Media infinita):
- 🚨 **EMERGENCIA** 🚨
- Ni siquiera la LGN funciona
- El promedio literalmente no existe
- Ejemplo: Cauchy
- Repensar completamente el problema

---

## El Experimento

### Distribuciones de Prueba

El script genera 8 distribuciones con diferentes propiedades:

| Distribución | α real | Tipo | ¿Qué testea? |
|--------------|--------|------|--------------|
| Normal | ∞ | Thin | Caso base |
| Exponencial | ∞ | Thin | Colas exponenciales |
| Lognormal | ∞ | Sub-exponencial | Colas pesadas pero momentos finitos |
| Pareto(α=3) | 3 | Fat | Kurtosis infinita |
| Pareto(α=2) | 2 | Fat | Varianza infinita |
| Pareto(α=1.5) | 1.5 | Fat | Varianza muy infinita |
| Cauchy | 1 | Fat | Media infinita |
| Student-t(ν=4) | 4 | **Pseudo-fat** | ¡La trampa! |

### Lo Que Harás

#### Parte A: Aplicar Diagnósticos

Para cada distribución:
1. Examinar el log-log survival plot
2. Calcular α̂ con Hill
3. Calcular κ de Taleb
4. Comparar α̂ con α real

**Llenar tabla:**

| Distribución | α real | α̂ (Hill) | κ | Diagnóstico correcto? |
|--------------|--------|-----------|---|----------------------|
| Normal | ∞ | ? | ? | ? |
| Pareto(α=3) | 3 | ? | ? | ? |
| ... | ... | ... | ... | ... |

#### Parte B: Convergencia del Promedio

Observar cómo converge (o no) el promedio para cada distribución:

- Normal: Converge rápido y limpio
- Pareto α=3: Converge pero con volatilidad
- Pareto α=1.5: Converge muy lento con saltos
- Cauchy: NO CONVERGE

**Pregunta:** ¿Cuántas observaciones necesitas para convergencia al 10%?

| Distribución | n para convergencia 10% |
|--------------|-------------------------|
| Normal | ~100 |
| Pareto α=3 | ~1,000 |
| Pareto α=2 | ~10,000+ |
| Pareto α=1.5 | >100,000 |
| Cauchy | **Nunca** |

#### Parte C: Impacto del Cisne Negro

El script muestra cómo UNA observación extrema afecta la media:

| Distribución | Cambio en media por 1 cisne negro |
|--------------|-----------------------------------|
| Normal | ~1% |
| Pareto α=2 | ~10-20% |
| Cauchy | Puede ser >100% |

#### Parte D: La Trampa de Student-t

Comparar Student-t(ν=4) con Pareto(α=4):
- Ambos tienen α=4
- PERO Student-t tiene colas que decaen más rápido
- Usar Student-t para modelar fat tails = **subestimar riesgo**

---

## Preguntas de Reflexión

1. **¿Por qué el estimador de Hill solo usa las k observaciones más extremas?** ¿Qué pasa si usas todas?

2. **Si α̂ = 2.5, ¿puedes confiar en la varianza muestral?** ¿Por qué sí o por qué no?

3. **¿Por qué κ es mejor que α̂ para detectar fat tails en la práctica?**

4. **¿Cómo explicarías a alguien sin matemáticas que "la varianza es infinita"?**

5. **Si te dan datos de un fenómeno desconocido, ¿cuál es tu primer diagnóstico?**

6. **¿Por qué Student-t es una trampa?** ¿Qué usarías en su lugar?

---

## Adaptaciones Concretas

### Código para Datos Fat-Tailed

```python
import numpy as np
from scipy.stats import median_abs_deviation, bootstrap

# === TENDENCIA CENTRAL ===
# MAL (si α < 4):
media = np.mean(data)

# BIEN:
mediana = np.median(data)

# === DISPERSIÓN ===
# MAL (si α < 4):
std = np.std(data)

# BIEN:
mad = median_abs_deviation(data)

# === INTERVALOS DE CONFIANZA ===
# MAL:
ic = (media - 1.96*std, media + 1.96*std)

# BIEN:
result = bootstrap((data,), np.median, confidence_level=0.95)
ic = result.confidence_interval

# === RIESGO ===
# MAL:
VaR_99 = media - 2.33 * std  # Paramétrico normal

# BIEN:
VaR_99 = np.percentile(data, 1)  # Histórico
ES_99 = data[data < VaR_99].mean()  # Expected Shortfall
```

---

## Ejecutar

```bash
cd clase/05_probabilidad/ejercicios
source .venv/bin/activate
python ejercicio_sintetico.py
```

El script generará:
- `diagnosticos_fattails.png`: Panel completo de diagnósticos para cada distribución
- `convergencia_fattails.png`: Cómo converge (o no) el promedio
- `cisne_negro_impacto.png`: Impacto de una observación extrema
- `student_t_trampa.png`: Por qué Student-t no es suficiente

---

## Referencia

- Taleb, N.N. (2020). *Statistical Consequences of Fat Tails*. STEM Academic Press.
- Capítulo 3: "How to recognize fat tails"
- Capítulo 4: "The Hill estimator"
