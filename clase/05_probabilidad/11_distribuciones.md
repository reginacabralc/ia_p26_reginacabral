# Distribuciones de Probabilidad

Las distribuciones son el "vocabulario" de la probabilidad — patrones recurrentes que aparecen una y otra vez en la naturaleza y en los modelos.

## ¿Qué es una Distribución?

Una **distribución de probabilidad** describe cómo se reparte la probabilidad sobre los posibles valores de una variable aleatoria.

### Dos Tipos Fundamentales

| Tipo | Variable | Descripción | Ejemplo |
|------|----------|-------------|---------|
| **Discreta** | Valores contables | Probabilidad en puntos específicos | Lanzamientos de dado |
| **Continua** | Valores en intervalo | Probabilidad en rangos | Altura de personas |

---

## Distribuciones Discretas

### Bernoulli

El experimento más simple: éxito o fracaso.

$$X \sim \text{Bernoulli}(p)$$

- $P(X=1) = p$ (éxito)
- $P(X=0) = 1-p$ (fracaso)
- $E[X] = p$
- $\text{Var}(X) = p(1-p)$

**Ejemplo:** Lanzar una moneda, respuesta sí/no, clic o no clic.

### Binomial

Número de éxitos en $n$ ensayos Bernoulli independientes.

$$X \sim \text{Binomial}(n, p)$$

$$P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}$$

- $E[X] = np$
- $\text{Var}(X) = np(1-p)$

**Ejemplo:** Número de caras en 10 lanzamientos de moneda.

### Poisson

Número de eventos en un intervalo fijo, cuando los eventos son raros e independientes.

$$X \sim \text{Poisson}(\lambda)$$

$$P(X=k) = \frac{\lambda^k e^{-\lambda}}{k!}$$

- $E[X] = \lambda$
- $\text{Var}(X) = \lambda$

**Ejemplo:** Número de llamadas a un call center por hora, número de errores tipográficos por página.

### Geométrica

Número de ensayos hasta el primer éxito.

$$X \sim \text{Geom}(p)$$

$$P(X=k) = (1-p)^{k-1} p$$

- $E[X] = 1/p$
- $\text{Var}(X) = (1-p)/p^2$

**Ejemplo:** Cuántas veces lanzas un dado hasta obtener un 6.

---

## Distribuciones Continuas

### Uniforme

Todos los valores en un intervalo son igualmente probables.

$$X \sim \text{Uniform}(a, b)$$

$$f(x) = \frac{1}{b-a} \quad \text{para } x \in [a,b]$$

- $E[X] = \frac{a+b}{2}$
- $\text{Var}(X) = \frac{(b-a)^2}{12}$

**Ejemplo:** Generador de números aleatorios, tiempo de llegada en un intervalo.

### Normal (Gaussiana)

La distribución más importante — aparece en todas partes gracias al Teorema del Límite Central.

$$X \sim \mathcal{N}(\mu, \sigma^2)$$

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

- $E[X] = \mu$
- $\text{Var}(X) = \sigma^2$

**Propiedades clave:**
- Simétrica alrededor de $\mu$
- ~68% de los datos dentro de $\pm 1\sigma$
- ~95% dentro de $\pm 2\sigma$
- ~99.7% dentro de $\pm 3\sigma$

**Normal Estándar:** $Z \sim \mathcal{N}(0, 1)$

### Exponencial

Tiempo hasta el primer evento (continua análoga a Poisson).

$$X \sim \text{Exp}(\lambda)$$

$$f(x) = \lambda e^{-\lambda x} \quad \text{para } x \geq 0$$

- $E[X] = 1/\lambda$
- $\text{Var}(X) = 1/\lambda^2$

**Propiedad sin memoria:** $P(X > s+t | X > s) = P(X > t)$

**Ejemplo:** Tiempo entre llegadas de clientes, tiempo de vida de componentes.

### Log-Normal

Cuando el logaritmo de una variable es normal.

$$X \sim \text{LogNormal}(\mu, \sigma^2) \iff \log(X) \sim \mathcal{N}(\mu, \sigma^2)$$

- Siempre positiva
- Asimétrica (cola derecha más larga)
- Común en fenómenos multiplicativos

**Ejemplo:** Precios de acciones, tamaños de archivos, ingresos.

---

## Distribuciones de Colas Pesadas (Fat Tails)

Estas distribuciones son fundamentales para entender fenómenos extremos.

### Pareto (Ley de Potencias)

$$X \sim \text{Pareto}(x_m, \alpha)$$

$$P(X > x) = \left(\frac{x_m}{x}\right)^\alpha \quad \text{para } x \geq x_m$$

- Si $\alpha \leq 1$: media infinita
- Si $\alpha \leq 2$: varianza infinita

**Ejemplo:** Distribución de riqueza, tamaño de ciudades, popularidad de sitios web.

### Cauchy

El caso extremo: ni media ni varianza existen.

$$X \sim \text{Cauchy}(x_0, \gamma)$$

$$f(x) = \frac{1}{\pi\gamma\left[1 + \left(\frac{x-x_0}{\gamma}\right)^2\right]}$$

- $E[X]$ no existe
- $\text{Var}(X)$ no existe
- El promedio de $n$ muestras Cauchy es... Cauchy (no converge)

**Importante:** La distribución Cauchy destruye nuestras intuiciones sobre promedios.

### Student-t

Interpolación entre Normal y Cauchy.

$$X \sim t\_\nu$$

- $\nu = 1$: es Cauchy
- $\nu \to \infty$: es Normal
- $\nu \leq 2$: varianza infinita

**Uso:** Estimación robusta, modelos financieros, cuando sospechas de colas pesadas.

---

## Comparación Visual

![Distribuciones de probabilidad]({{ '/05_probabilidad/images/distribuciones_comparacion.png' | url }})

*Nota: Esta imagen se genera automáticamente al ejecutar `lab_probabilidad.py`*

---

## Resumen: ¿Cuándo Usar Cada Una?

| Distribución | Usar cuando... |
|--------------|----------------|
| Bernoulli | Un solo ensayo binario |
| Binomial | Contar éxitos en $n$ ensayos |
| Poisson | Eventos raros en intervalo fijo |
| Normal | Sumas de muchas variables, errores |
| Exponencial | Tiempo hasta un evento |
| Log-Normal | Productos de muchas variables |
| Pareto | Fenómenos con "ganador toma todo" |
| Student-t | Datos con posibles outliers |

---

## Momentos y Colas

Una forma de caracterizar distribuciones es por sus **momentos**:

| Momento | Qué mide |
|---------|----------|
| 1º (media) | Centro |
| 2º (varianza) | Dispersión |
| 3º (asimetría) | Sesgo izq/der |
| 4º (curtosis) | Peso de las colas |

**Curtosis:**
- Normal tiene curtosis = 3
- Curtosis > 3: colas más pesadas que normal ("leptocúrtica")
- Curtosis < 3: colas más ligeras ("platicúrtica")

---

**Siguiente:** [Estadística y Estimadores →](12_estadistica_estimadores.md)
