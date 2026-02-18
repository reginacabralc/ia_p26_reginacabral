# Ejercicios de Fat Tails

Ejercicios prácticos para entender colas largas, riesgo financiero y las limitaciones de los modelos normales.

## Setup con uv

[uv](https://github.com/astral-sh/uv) es un gestor de paquetes Python ultrarrápido. Es la forma recomendada de configurar el entorno.

### Instalación de uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Crear entorno e instalar dependencias

```bash
# Navegar al directorio de ejercicios
cd clase/05_probabilidad/ejercicios

# Crear entorno virtual
uv venv

# Activar entorno
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Instalar dependencias
uv pip install -r requirements.txt
```

### Alternativa: pip tradicional

Si prefieres usar pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Ejercicios Disponibles

### 1. Eventos Imposibles del S&P 500 (`ejercicio_sp500.py`)

**Objetivo:** Demostrar que los retornos financieros NO son normales usando datos reales.

**Lo que aprenderás:**
- Cuántos eventos "imposibles" han ocurrido en la historia del S&P 500
- Por qué los modelos normales subestiman el riesgo
- Fechas de los principales cisnes negros financieros

**Ejecutar:**
```bash
python ejercicio_sp500.py
```

---

### 2. El Fraude del VaR (`ejercicio_var.py`)

**Objetivo:** Entender por qué el Value at Risk (VaR) falla en la práctica.

**Lo que aprenderás:**
- Cómo se calcula el VaR
- Por qué las violaciones son más frecuentes de lo esperado
- Qué tan mal subestima las pérdidas extremas

**Ejecutar:**
```bash
python ejercicio_var.py
```

---

### 3. Anatomía de Fat Tails (`ejercicio_sintetico.py`)

**Objetivo:** Experimentar con distribuciones fat-tailed en un entorno controlado.

**Lo que aprenderás:**
- Cómo converge (o no) el promedio en diferentes distribuciones
- El efecto de una sola observación extrema
- El criterio κ de Taleb

**Ejecutar:**
```bash
python ejercicio_sintetico.py
```

---

## Cómo Usar Estos Ejercicios

### Para estudiantes

1. **Lee primero** el markdown correspondiente (`ejercicio_*.md`) para entender el contexto
2. **Ejecuta** el código Python para ver los resultados
3. **Modifica** los parámetros para explorar:
   - ¿Qué pasa si cambio el nivel de confianza del VaR?
   - ¿Qué pasa con diferentes valores de α en Pareto?
   - ¿Qué otras acciones/índices muestran fat tails?
4. **Investiga** los eventos que encuentres (googlea las fechas)
5. **Responde** las preguntas de reflexión

### Con Cursor/AI

Puedes pedirle a Cursor que:
- Modifique el código para analizar otros activos (Bitcoin, oro, etc.)
- Añada nuevos análisis o visualizaciones
- Explique partes del código que no entiendas
- Ayude a responder las preguntas de reflexión

---

## Estructura de Archivos

```
ejercicios/
├── README.md                 # Este archivo
├── requirements.txt          # Dependencias
├── ejercicio_sp500.md        # Teoría y contexto del ejercicio S&P 500
├── ejercicio_sp500.py        # Código ejecutable
├── ejercicio_var.md          # Teoría y contexto del ejercicio VaR
├── ejercicio_var.py          # Código ejecutable
├── ejercicio_sintetico.md    # Teoría y contexto del ejercicio sintético
├── ejercicio_sintetico.py    # Código ejecutable
└── outputs/                  # Gráficas generadas (se crean al ejecutar)
```

---

## Preguntas Frecuentes

**¿Necesito conexión a internet?**
Sí, para descargar datos del S&P 500 en el ejercicio 1. Los otros ejercicios funcionan offline.

**¿Qué hago si yfinance no funciona?**
A veces Yahoo Finance cambia su API. Prueba actualizar: `uv pip install --upgrade yfinance`

**¿Puedo usar otros datos financieros?**
¡Sí! Modifica el ticker en el código. Ejemplos:
- `^IXIC` - NASDAQ
- `^DJI` - Dow Jones
- `BTC-USD` - Bitcoin
- `AAPL` - Apple

---

## Referencias

- Taleb, N.N. *Statistical Consequences of Fat Tails* (2020)
- Taleb, N.N. *The Black Swan* (2007)
- Mandelbrot, B. *The Misbehavior of Markets* (2004)
