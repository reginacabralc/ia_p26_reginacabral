#!/usr/bin/env python3
"""
Ejercicio: Los Eventos Imposibles del S&P 500

Este script demuestra que los retornos financieros NO son normales,
usando datos históricos reales.

Ejecutar:
    python ejercicio_sp500.py

Autor: Módulo de Probabilidad - IA P26
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import yfinance as yf
from pathlib import Path
from datetime import datetime

# Configuración
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# Crear directorio de outputs
OUTPUT_DIR = Path(__file__).parent / "images" / "sp500"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def descargar_datos(ticker="^GSPC", start="1950-01-01"):
    """
    Descarga datos históricos del S&P 500.
    
    Args:
        ticker: Símbolo del activo (default: S&P 500)
        start: Fecha de inicio
    
    Returns:
        DataFrame con precios y retornos
    """
    print(f"📥 Descargando datos de {ticker} desde {start}...")
    
    data = yf.download(ticker, start=start, progress=False, auto_adjust=True)
    
    # Manejar MultiIndex columns (yfinance >= 0.2.40)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    # Calcular retornos logarítmicos
    data['Returns'] = np.log(data['Close'] / data['Close'].shift(1))
    data = data.dropna()
    
    print(f"   ✓ {len(data)} observaciones descargadas")
    print(f"   ✓ Período: {data.index[0].strftime('%Y-%m-%d')} a {data.index[-1].strftime('%Y-%m-%d')}")
    
    return data


def hill_estimator(data, k=None):
    """
    Estimador de Hill para el índice de cola α.
    
    α < 2: varianza infinita
    α < 1: media infinita
    """
    sorted_data = np.sort(np.abs(data))[::-1]
    n = len(sorted_data)
    
    if k is None:
        k = int(np.sqrt(n))
    
    k = min(k, n - 1)
    log_ratios = np.log(sorted_data[:k] / sorted_data[k])
    alpha_hat = k / np.sum(log_ratios)
    
    return alpha_hat


def kappa_taleb(data):
    """
    Criterio Kappa de Taleb: κ = max(|X|) / sum(|X|)
    
    κ → 0: thin tails
    κ alto: fat tails (una observación domina)
    """
    data_pos = np.abs(data)
    return np.max(data_pos) / np.sum(data_pos)


def calcular_estadisticas(returns):
    """Calcula estadísticas básicas y diagnósticos de fat tails."""
    mu = returns.mean()
    sigma = returns.std()
    
    print(f"\n📊 Estadísticas de retornos diarios:")
    print(f"   Media (μ):     {mu*100:.4f}%")
    print(f"   Desv. Est (σ): {sigma*100:.4f}%")
    print(f"   Asimetría:     {stats.skew(returns):.3f}")
    print(f"   Curtosis:      {stats.kurtosis(returns):.3f} (normal = 0)")
    
    # Diagnósticos de fat tails (Metodología Taleb)
    alpha = hill_estimator(returns.values)
    kappa = kappa_taleb(returns.values)
    
    print(f"\n🎯 Diagnósticos de Fat Tails (Metodología Taleb):")
    print(f"   Estimador de Hill (α̂): {alpha:.2f}")
    print(f"   Kappa (max/sum):        {kappa:.6f}")
    
    if alpha > 4:
        print(f"   → α > 4: Kurtosis finita, cerca de thin tails")
    elif alpha > 2:
        print(f"   → 2 < α ≤ 4: Varianza finita, kurtosis INFINITA")
        print(f"     El TLC funciona pero MUY LENTO")
    elif alpha > 1:
        print(f"   → 1 < α ≤ 2: ¡VARIANZA INFINITA!")
        print(f"     TLC NO funciona, LGN muy lento")
    else:
        print(f"   → α ≤ 1: ¡MEDIA INFINITA!")
        print(f"     Ningún teorema límite funciona")
    
    return mu, sigma


def contar_eventos_extremos(returns, mu, sigma):
    """
    Cuenta eventos extremos y compara con lo esperado bajo normalidad.
    
    Retorna un DataFrame con la comparación.
    """
    n_days = len(returns)
    n_years = n_days / 252  # Aproximadamente 252 días de trading por año
    
    # Umbrales a analizar
    umbrales = [3, 4, 5, 6, 7, 8, 10]
    
    resultados = []
    
    for k in umbrales:
        # Eventos observados (ambas colas)
        eventos_obs = np.sum(np.abs(returns - mu) > k * sigma)
        
        # Probabilidad teórica bajo normalidad (ambas colas)
        prob_normal = 2 * (1 - stats.norm.cdf(k))
        eventos_esperados = prob_normal * n_days
        
        # Frecuencia esperada en años
        if eventos_esperados > 0:
            freq_esperada_años = n_years / eventos_esperados
        else:
            freq_esperada_años = np.inf
        
        # Factor de subestimación
        if eventos_esperados > 0:
            factor = eventos_obs / eventos_esperados
        else:
            factor = np.inf if eventos_obs > 0 else 0
        
        resultados.append({
            'Umbral': f'>{k}σ',
            'Prob. Normal': f'{prob_normal:.2e}',
            'Esperados': f'{eventos_esperados:.1f}',
            'Observados': eventos_obs,
            'Frecuencia Normal': f'1 cada {freq_esperada_años:.0f} años' if freq_esperada_años < 1e6 else 'Casi nunca',
            'Factor': f'{factor:.1f}x' if factor < 1000 else f'{factor:.0f}x'
        })
    
    return pd.DataFrame(resultados)


def identificar_cisnes_negros(data, mu, sigma, top_n=25):
    """
    Identifica los eventos más extremos en la historia.
    
    Retorna DataFrame con fechas, retornos y sigmas.
    """
    returns = data['Returns']
    
    # Calcular número de sigmas para cada retorno
    z_scores = (returns - mu) / sigma
    
    # Ordenar por valor absoluto
    extreme_idx = np.abs(z_scores).nlargest(top_n).index
    
    eventos = []
    for idx in extreme_idx:
        ret = returns[idx]
        z = z_scores[idx]
        
        # Probabilidad bajo normal
        prob = 2 * (1 - stats.norm.cdf(abs(z)))
        
        eventos.append({
            'Fecha': idx.strftime('%Y-%m-%d'),
            'Retorno': f'{ret*100:+.2f}%',
            'Sigmas': f'{z:.1f}σ',
            'Prob. Normal': f'{prob:.2e}',
            'Descripción': ''  # El estudiante llenará esto
        })
    
    return pd.DataFrame(eventos)


def plot_histograma_vs_normal(returns, mu, sigma):
    """
    Histograma de retornos vs distribución normal teórica.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histograma normal
    ax = axes[0]
    ax.hist(returns, bins=100, density=True, alpha=0.7, color='steelblue', 
            edgecolor='white', label='Retornos reales')
    
    x = np.linspace(returns.min(), returns.max(), 1000)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2, 
            label='Normal teórica')
    
    ax.set_xlabel('Retorno diario')
    ax.set_ylabel('Densidad')
    ax.set_title('Histograma de Retornos vs Normal')
    ax.legend()
    
    # Histograma en escala log (para ver las colas)
    ax = axes[1]
    counts, bins, _ = ax.hist(returns, bins=100, density=True, alpha=0.7, 
                               color='steelblue', edgecolor='white', 
                               label='Retornos reales')
    ax.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2, 
            label='Normal teórica')
    
    ax.set_yscale('log')
    ax.set_xlabel('Retorno diario')
    ax.set_ylabel('Densidad (log)')
    ax.set_title('Escala Log: Las colas son MÁS PESADAS que Normal')
    ax.legend()
    ax.set_ylim(1e-4, None)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'sp500_histograma.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Guardado: {OUTPUT_DIR / 'sp500_histograma.png'}")


def plot_qqplot(returns):
    """
    QQ-plot para comparar con distribución normal.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    stats.probplot(returns, dist="norm", plot=ax)
    ax.get_lines()[0].set_markersize(3)
    ax.get_lines()[0].set_alpha(0.5)
    
    ax.set_title('QQ-Plot: Retornos vs Normal\n'
                'La curvatura en los extremos indica COLAS PESADAS')
    
    # Añadir anotaciones
    ax.annotate('Cola izquierda\nmás pesada', xy=(-4, -0.1), fontsize=10,
               bbox=dict(boxstyle='round', facecolor='lightyellow'))
    ax.annotate('Cola derecha\nmás pesada', xy=(2, 0.08), fontsize=10,
               bbox=dict(boxstyle='round', facecolor='lightyellow'))
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'sp500_qqplot.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Guardado: {OUTPUT_DIR / 'sp500_qqplot.png'}")


def plot_eventos_tiempo(data, mu, sigma):
    """
    Gráfica de eventos extremos a lo largo del tiempo.
    """
    returns = data['Returns']
    z_scores = (returns - mu) / sigma
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Panel 1: Retornos en el tiempo
    ax = axes[0]
    ax.plot(returns.index, returns * 100, alpha=0.7, linewidth=0.5)
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axhline(y=3*sigma*100, color='red', linestyle='--', alpha=0.5, label='+3σ')
    ax.axhline(y=-3*sigma*100, color='red', linestyle='--', alpha=0.5, label='-3σ')
    ax.set_ylabel('Retorno diario (%)')
    ax.set_title('Retornos Diarios del S&P 500')
    ax.legend()
    
    # Marcar eventos extremos
    extremos = np.abs(z_scores) > 4
    ax.scatter(returns.index[extremos], returns[extremos] * 100, 
               color='red', s=20, zorder=5, label='Eventos >4σ')
    
    # Panel 2: Eventos extremos (>4σ) a lo largo del tiempo
    ax = axes[1]
    eventos_4sigma = returns[np.abs(z_scores) > 4]
    
    ax.stem(eventos_4sigma.index, eventos_4sigma * 100, 
            linefmt='r-', markerfmt='ro', basefmt='k-')
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.set_ylabel('Retorno (%)')
    ax.set_xlabel('Fecha')
    ax.set_title(f'Eventos >4σ: {len(eventos_4sigma)} ocurrencias '
                f'(Normal predice ~{0.006 * len(returns) / 100:.0f})')
    
    # Anotar algunos eventos famosos
    eventos_famosos = {
        '1987-10-19': 'Lunes Negro',
        '2008-10-15': 'Crisis Financiera',
        '2020-03-16': 'COVID Crash',
    }
    
    for fecha, nombre in eventos_famosos.items():
        try:
            idx = pd.Timestamp(fecha)
            if idx in eventos_4sigma.index:
                ret = eventos_4sigma[idx] * 100
                ax.annotate(nombre, xy=(idx, ret), 
                           xytext=(10, 10 if ret < 0 else -10),
                           textcoords='offset points',
                           fontsize=9,
                           arrowprops=dict(arrowstyle='->', color='black'))
        except:
            pass
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'sp500_eventos_tiempo.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Guardado: {OUTPUT_DIR / 'sp500_eventos_tiempo.png'}")


def plot_diagnosticos_fattails(returns):
    """
    Gráficos de diagnóstico de fat tails (Metodología Taleb).
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    data = returns.values
    
    # Panel 1: Log-log survival plot
    ax = axes[0, 0]
    sorted_data = np.sort(np.abs(data))[::-1]
    n = len(sorted_data)
    survival = np.arange(1, n + 1) / n
    
    ax.loglog(sorted_data, survival, 'b.', alpha=0.3, markersize=2)
    ax.set_xlabel('|Retorno|')
    ax.set_ylabel('P(|X| > x)')
    ax.set_title('Log-Log Survival Plot\n(Línea recta = Power Law = Fat Tail)')
    ax.grid(True, alpha=0.3)
    
    # Panel 2: Hill estimator para diferentes k
    ax = axes[0, 1]
    ks = np.arange(20, int(np.sqrt(n) * 3), 10)
    alphas = [hill_estimator(data, k) for k in ks]
    
    ax.plot(ks, alphas, 'b-', linewidth=2)
    ax.axhline(y=2, color='red', linestyle='--', linewidth=2, label='α=2 (Var=∞)')
    ax.axhline(y=3, color='orange', linestyle='--', linewidth=1, label='α=3')
    ax.axhline(y=4, color='green', linestyle='--', linewidth=1, label='α=4')
    ax.set_xlabel('k (observaciones en la cola)')
    ax.set_ylabel('α̂ (Hill)')
    ax.set_title(f'Estimador de Hill\nα̂ ≈ {hill_estimator(data):.2f}')
    ax.legend()
    ax.set_ylim(0, 6)
    ax.grid(True, alpha=0.3)
    
    # Panel 3: Evolución de kappa
    ax = axes[1, 0]
    ns = np.logspace(2, np.log10(len(data)), 50).astype(int)
    kappas = [kappa_taleb(data[:n]) for n in ns]
    
    ax.semilogx(ns, kappas, 'b-', linewidth=2)
    ax.axhline(y=0.01, color='red', linestyle='--', label='κ=0.01 (umbral)')
    ax.set_xlabel('n (tamaño de muestra)')
    ax.set_ylabel('κ = max/sum')
    ax.set_title('Criterio Kappa de Taleb\n(Alto = una observación domina)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Panel 4: Mean Excess Function
    ax = axes[1, 1]
    data_pos = np.abs(data)
    thresholds = np.percentile(data_pos, np.linspace(50, 99, 50))
    mean_excess = []
    
    for u in thresholds:
        excesses = data_pos[data_pos > u] - u
        if len(excesses) > 10:
            mean_excess.append(np.mean(excesses))
        else:
            mean_excess.append(np.nan)
    
    ax.plot(thresholds * 100, mean_excess, 'b-', linewidth=2)
    ax.set_xlabel('Umbral u (%)')
    ax.set_ylabel('E[|X| - u | |X| > u]')
    ax.set_title('Mean Excess Function\n(Creciente = Fat Tail, Constante = Exponencial)')
    ax.grid(True, alpha=0.3)
    
    plt.suptitle('Diagnósticos de Fat Tails (Metodología Taleb)', fontsize=14)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'sp500_fattails_diagnosticos.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Guardado: {OUTPUT_DIR / 'sp500_fattails_diagnosticos.png'}")


def main():
    """Ejecuta el análisis completo."""
    print("="*60)
    print("EJERCICIO: Los Eventos Imposibles del S&P 500")
    print("="*60)
    
    # 1. Descargar datos
    data = descargar_datos()
    returns = data['Returns']
    
    # 2. Calcular estadísticas
    mu, sigma = calcular_estadisticas(returns)
    
    # 3. Contar eventos extremos
    print("\n" + "="*60)
    print("COMPARACIÓN: Normal vs Realidad")
    print("="*60)
    
    tabla_eventos = contar_eventos_extremos(returns, mu, sigma)
    print("\n" + tabla_eventos.to_string(index=False))
    
    # 4. Identificar cisnes negros
    print("\n" + "="*60)
    print("TOP 25 EVENTOS MÁS EXTREMOS")
    print("="*60)
    print("(Investiga qué pasó en estas fechas)")
    
    cisnes = identificar_cisnes_negros(data, mu, sigma)
    print("\n" + cisnes.to_string(index=False))
    
    # 5. Generar visualizaciones
    print("\n" + "="*60)
    print("GENERANDO VISUALIZACIONES")
    print("="*60)
    
    plot_histograma_vs_normal(returns, mu, sigma)
    plot_qqplot(returns)
    plot_eventos_tiempo(data, mu, sigma)
    plot_diagnosticos_fattails(returns)
    
    # 6. Resumen final
    print("\n" + "="*60)
    print("CONCLUSIÓN")
    print("="*60)
    
    eventos_4sigma_obs = np.sum(np.abs(returns - mu) > 4 * sigma)
    eventos_4sigma_esp = 2 * (1 - stats.norm.cdf(4)) * len(returns)
    
    alpha_hill = hill_estimator(returns.values)
    
    print(f"""
    En {len(returns)} días de trading del S&P 500:
    
    📊 EVENTOS EXTREMOS:
    • Eventos >4σ esperados (si fuera normal): {eventos_4sigma_esp:.1f}
    • Eventos >4σ observados:                  {eventos_4sigma_obs}
    • Factor de subestimación:                 {eventos_4sigma_obs/eventos_4sigma_esp:.0f}x
    
    🎯 DIAGNÓSTICO DE COLAS (Taleb):
    • Índice de cola estimado (Hill): α̂ = {alpha_hill:.2f}
    • Interpretación: {'Varianza finita, kurtosis infinita' if alpha_hill > 2 else '¡VARIANZA INFINITA!'}
    
    ⚠️  CONCLUSIONES:
    
    1. El S&P 500 tiene colas MUCHO más pesadas que la normal
    2. El modelo normal subestima eventos extremos por ~{eventos_4sigma_obs/eventos_4sigma_esp:.0f}x
    3. El índice de cola α ≈ {alpha_hill:.1f} implica que:
       {'- La varianza es finita pero la kurtosis es infinita' if alpha_hill > 2 else '- ¡La varianza es infinita!'}
       - El Teorema del Límite Central converge MUY lentamente
       - Los modelos de riesgo basados en varianza son inadecuados
    
    ⛔ ADVERTENCIA: Student-t NO es suficiente para modelar estos datos.
       Student-t tiene colas que decaen más rápido que power law real.
       Usar Student-t = SUBESTIMAR el riesgo.
    
    ¡Investiga las fechas de los cisnes negros!
    """)
    
    print(f"\n📁 Resultados guardados en: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
