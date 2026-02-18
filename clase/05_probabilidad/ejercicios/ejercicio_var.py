#!/usr/bin/env python3
"""
Ejercicio: El Fraude del Value at Risk (VaR)

Este script demuestra por qué el VaR paramétrico falla con fat tails.

IMPORTANTE según Taleb:
- Student-t NO es suficiente para modelar colas reales
- Los retornos financieros tienen α ≈ 3 (varianza finita pero kurtosis infinita)
- El VaR subestima sistemáticamente el riesgo

Metodología:
1. Estimar el índice de cola α con Hill
2. Comparar VaR paramétrico vs histórico vs EVT
3. Mostrar las violaciones y su severidad

Ejecutar:
    python ejercicio_var.py

Autor: Módulo de Probabilidad - IA P26
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import yfinance as yf
from pathlib import Path
import warnings
import multiprocessing as mp

warnings.filterwarnings('ignore')

# Number of parallel workers
N_WORKERS = mp.cpu_count() - 1

# Configuración
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11

# Crear directorio de outputs
OUTPUT_DIR = Path(__file__).parent / "images" / "var"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# DESCARGA DE DATOS
# =============================================================================

def descargar_datos(ticker="^GSPC", start="1990-01-01"):
    """Descarga datos históricos."""
    print(f"📥 Descargando datos de {ticker}...")
    
    data = yf.download(ticker, start=start, progress=False, auto_adjust=True)
    
    # Manejar MultiIndex columns (yfinance >= 0.2.40)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    data['Returns'] = np.log(data['Close'] / data['Close'].shift(1))
    data = data.dropna()
    
    print(f"   ✓ {len(data)} observaciones ({data.index[0].strftime('%Y-%m-%d')} - {data.index[-1].strftime('%Y-%m-%d')})")
    return data


# =============================================================================
# DIAGNÓSTICO DE COLAS (Metodología Taleb)
# =============================================================================

def hill_estimator(data, k=None):
    """
    Estimador de Hill para el índice de cola α.
    """
    sorted_data = np.sort(np.abs(data))[::-1]
    n = len(sorted_data)
    
    if k is None:
        k = int(np.sqrt(n))
    
    k = min(k, n - 1)
    log_ratios = np.log(sorted_data[:k] / sorted_data[k])
    alpha_hat = k / np.sum(log_ratios)
    
    return alpha_hat


def diagnostico_colas(returns):
    """
    Diagnóstico completo de las colas de la distribución.
    """
    print("\n" + "="*60)
    print("DIAGNÓSTICO DE COLAS (Metodología Taleb)")
    print("="*60)
    
    # Estadísticas básicas
    mu = returns.mean()
    sigma = returns.std()
    skew = stats.skew(returns)
    kurt = stats.kurtosis(returns)  # Excess kurtosis
    
    print(f"\n📊 Estadísticas básicas:")
    print(f"   Media:      {mu*100:.4f}% diario")
    print(f"   Desv. Est:  {sigma*100:.4f}% diario")
    print(f"   Skewness:   {skew:.4f}")
    print(f"   Kurtosis:   {kurt:.4f} (Normal = 0)")
    
    # Estimador de Hill
    alpha_hill = hill_estimator(returns.values)
    
    print(f"\n🎯 Estimador de Hill:")
    print(f"   α̂ = {alpha_hill:.2f}")
    
    if alpha_hill > 4:
        print("   → Kurtosis finita (pero revisar!)")
    elif alpha_hill > 2:
        print("   → Varianza finita, kurtosis infinita")
        print("   → TLC funciona pero LENTO")
    elif alpha_hill > 1:
        print("   → ¡VARIANZA INFINITA!")
        print("   → TLC NO funciona")
    else:
        print("   → ¡MEDIA INFINITA!")
        print("   → LGN NO funciona")
    
    # Test de normalidad
    jb_stat, jb_p = stats.jarque_bera(returns)
    print(f"\n📉 Test de Jarque-Bera:")
    print(f"   Estadístico: {jb_stat:.2f}")
    print(f"   p-value:     {jb_p:.2e}")
    print(f"   → {'RECHAZAMOS normalidad' if jb_p < 0.05 else 'No rechazamos normalidad'}")
    
    return {
        'mu': mu,
        'sigma': sigma,
        'alpha_hill': alpha_hill,
        'kurtosis': kurt
    }


# =============================================================================
# MÉTODOS DE VaR
# =============================================================================

def var_normal(returns, alpha=0.99):
    """VaR paramétrico asumiendo normalidad."""
    mu = returns.mean()
    sigma = returns.std()
    z = stats.norm.ppf(1 - alpha)
    return -(mu + z * sigma)


def var_historico(returns, alpha=0.99):
    """VaR usando simulación histórica (no paramétrico)."""
    return -np.percentile(returns, (1 - alpha) * 100)


def var_cornish_fisher(returns, alpha=0.99):
    """
    VaR con expansión de Cornish-Fisher.
    Ajusta el cuantil normal por skewness y kurtosis.
    """
    mu = returns.mean()
    sigma = returns.std()
    S = stats.skew(returns)
    K = stats.kurtosis(returns)  # Excess kurtosis
    
    z = stats.norm.ppf(1 - alpha)
    
    # Expansión de Cornish-Fisher
    z_cf = (z + (z**2 - 1)*S/6 + 
            (z**3 - 3*z)*(K)/24 - 
            (2*z**3 - 5*z)*(S**2)/36)
    
    return -(mu + z_cf * sigma)


def var_evt(returns, alpha=0.99, threshold_pct=90):
    """
    VaR usando Extreme Value Theory (EVT) con GPD.
    
    Teoría de Valores Extremos:
    - Modela solo la cola de la distribución
    - Usa Generalized Pareto Distribution (GPD)
    - Más robusto para eventos extremos
    """
    # Trabajar con pérdidas (valores negativos)
    losses = -returns.values
    
    # Umbral: percentil alto de pérdidas
    u = np.percentile(losses, threshold_pct)
    
    # Excesos sobre el umbral
    excesses = losses[losses > u] - u
    n_u = len(excesses)
    n = len(losses)
    
    if n_u < 20:
        return np.nan  # Muy pocos datos
    
    # Ajustar GPD a los excesos
    # GPD: F(x) = 1 - (1 + ξx/β)^(-1/ξ)
    try:
        params = stats.genpareto.fit(excesses)
        c, loc, scale = params  # c = ξ (shape), scale = β
        
        # VaR con EVT
        # VaR = u + (β/ξ) * [((n/n_u)*(1-α))^(-ξ) - 1]
        p = 1 - alpha
        Fu = n_u / n  # Probabilidad de exceder u
        
        if c != 0:
            var_evt = u + (scale/c) * ((p/Fu)**(-c) - 1)
        else:
            var_evt = u - scale * np.log(p/Fu)
        
        return var_evt
    except:
        return np.nan


# =============================================================================
# BACKTESTING (PARALLELIZED)
# =============================================================================

# Global variables for worker processes (initialized once per worker)
_WORKER_DATA = {}


def _init_worker(returns_values, window, alpha):
    """Initialize worker with shared data."""
    _WORKER_DATA['returns'] = returns_values
    _WORKER_DATA['window'] = window
    _WORKER_DATA['alpha'] = alpha


def _compute_var_for_index(args):
    """
    Compute VaR for a single index using worker's cached data.
    Args: (var_func_name, i)
    Returns: (i, var, ret_real)
    """
    var_func_name, i = args
    returns = _WORKER_DATA['returns']
    window = _WORKER_DATA['window']
    alpha = _WORKER_DATA['alpha']
    
    # Get training window
    train = pd.Series(returns[i-window:i])
    
    # Select VaR function
    if var_func_name == 'normal':
        var = var_normal(train, alpha)
    elif var_func_name == 'historico':
        var = var_historico(train, alpha)
    elif var_func_name == 'cornish_fisher':
        var = var_cornish_fisher(train, alpha)
    elif var_func_name == 'evt':
        var = var_evt(train, alpha)
    else:
        var = np.nan
    
    ret_real = returns[i]
    return (i, var, ret_real)


def _backtest_single_method(returns_values, returns_index, window, alpha, var_func_name, n_workers):
    """
    Backtest a single VaR method with parallel window computation.
    Uses multiprocessing.Pool with initializer for efficient data sharing.
    """
    n = len(returns_values)
    indices = list(range(window, n))
    
    # Create work items: (var_func_name, index)
    work_items = [(var_func_name, i) for i in indices]
    
    # Use Pool with initializer to share data efficiently
    with mp.Pool(
        processes=n_workers,
        initializer=_init_worker,
        initargs=(returns_values, window, alpha)
    ) as pool:
        results_list = pool.map(_compute_var_for_index, work_items, chunksize=100)
    
    # Build results DataFrame
    results_list.sort(key=lambda x: x[0])  # Sort by index
    
    fechas = [returns_index[i] for i, _, _ in results_list]
    vars_predichos = [var for _, var, _ in results_list]
    retornos_reales = [ret for _, _, ret in results_list]
    
    results = pd.DataFrame({
        'fecha': fechas,
        'VaR': vars_predichos,
        'Retorno': retornos_reales
    })
    results['Violacion'] = -results['Retorno'] > results['VaR']
    results['Severidad'] = np.where(
        results['Violacion'],
        (-results['Retorno'] - results['VaR']) / results['VaR'],
        0
    )
    
    return results


def backtest_completo(data, window=252, alpha=0.99):
    """
    Backtesting de todos los métodos de VaR (parallelized).
    
    Strategy: Process each method sequentially, but parallelize window 
    calculations within each method using multiprocessing.Pool.
    """
    print("\n" + "="*60)
    print(f"BACKTESTING VaR {alpha:.0%} (parallelized with {N_WORKERS} workers)")
    print("="*60)
    
    returns = data['Returns']
    returns_values = returns.values
    returns_index = returns.index.tolist()
    
    # Method configurations
    metodos_config = {
        'Normal': {'var_func_name': 'normal', 'color': '#3498db'},
        'Histórico': {'var_func_name': 'historico', 'color': '#2ecc71'},
        'Cornish-Fisher': {'var_func_name': 'cornish_fisher', 'color': '#9b59b6'},
        'EVT (GPD)': {'var_func_name': 'evt', 'color': '#e74c3c'},
    }
    
    all_results = {}
    metodos = {}
    
    for nombre, config in metodos_config.items():
        print(f"   ⏳ Procesando {nombre}...", end=" ", flush=True)
        
        results = _backtest_single_method(
            returns_values, returns_index, window, alpha,
            config['var_func_name'], N_WORKERS
        )
        
        all_results[nombre] = results
        metodos[nombre] = {
            'var_func': None,
            'color': config['color'],
            'results': results
        }
        print("✓")
    
    # Print summary
    print(f"\n{'Método':<20} {'Violaciones':>12} {'Tasa':>10} {'Esperada':>10} {'Severidad Avg':>15}")
    print("-"*70)
    
    expected_rate = 1 - alpha
    
    for nombre in metodos_config.keys():
        results = all_results[nombre]
        n_violations = results['Violacion'].sum()
        n_total = len(results)
        rate = n_violations / n_total
        avg_severity = results.loc[results['Violacion'], 'Severidad'].mean()
        
        # Indicador de problema
        ratio = rate / expected_rate
        if ratio > 2:
            status = "⚠️ PELIGRO"
        elif ratio > 1.5:
            status = "⚡ Alto"
        else:
            status = "✓"
        
        print(f"{nombre:<20} {n_violations:>12} {rate:>10.2%} {expected_rate:>10.2%} {avg_severity:>14.2%} {status}")
    
    return all_results, metodos


def plot_backtesting(data, all_results, metodos, alpha=0.99):
    """
    Visualización completa del backtesting.
    """
    fig, axes = plt.subplots(3, 2, figsize=(16, 14))
    
    # Panel 1: VaR a lo largo del tiempo
    ax = axes[0, 0]
    for nombre, config in metodos.items():
        results = config['results']
        ax.plot(results['fecha'], results['VaR'], 
               label=nombre, color=config['color'], alpha=0.7, linewidth=1)
    ax.set_ylabel('VaR')
    ax.set_title(f'VaR {alpha:.0%} Predicho por Método')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Panel 2: Violaciones del VaR Normal
    ax = axes[0, 1]
    results_normal = metodos['Normal']['results']
    retornos = -results_normal['Retorno']  # Pérdidas
    ax.plot(results_normal['fecha'], retornos, 
           color='gray', alpha=0.5, linewidth=0.5, label='Pérdidas')
    ax.plot(results_normal['fecha'], results_normal['VaR'],
           color='red', linewidth=1, label='VaR Normal')
    
    # Marcar violaciones
    violaciones = results_normal[results_normal['Violacion']]
    ax.scatter(violaciones['fecha'], -violaciones['Retorno'],
              color='red', s=20, zorder=5, label=f'Violaciones ({len(violaciones)})')
    
    ax.set_ylabel('Pérdida')
    ax.set_title('VaR Normal: Violaciones')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Panel 3: Comparación de tasas de violación
    ax = axes[1, 0]
    nombres = list(metodos.keys())
    tasas = [config['results']['Violacion'].mean() for config in metodos.values()]
    colores = [config['color'] for config in metodos.values()]
    
    bars = ax.bar(nombres, tasas, color=colores, alpha=0.7)
    ax.axhline(y=1-alpha, color='red', linestyle='--', linewidth=2, 
              label=f'Esperada ({(1-alpha)*100:.1f}%)')
    ax.set_ylabel('Tasa de Violación')
    ax.set_title('Comparación de Métodos: Tasa de Violación')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores
    for bar, tasa in zip(bars, tasas):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
               f'{tasa:.2%}', ha='center', va='bottom', fontsize=10)
    
    # Panel 4: Severidad de violaciones
    ax = axes[1, 1]
    severidades = []
    for config in metodos.values():
        results = config['results']
        sev = results.loc[results['Violacion'], 'Severidad'].values
        severidades.append(sev)
    
    bp = ax.boxplot(severidades, labels=nombres, patch_artist=True)
    for patch, color in zip(bp['boxes'], colores):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
    
    ax.set_ylabel('Severidad (exceso/VaR)')
    ax.set_title('Severidad de las Violaciones')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Panel 5: QQ-Plot de retornos vs Normal
    ax = axes[2, 0]
    returns = data['Returns'].dropna()
    stats.probplot(returns, dist="norm", plot=ax)
    ax.set_title('QQ-Plot: Retornos vs Normal\n(Colas pesadas = puntos fuera de la línea)')
    ax.grid(True, alpha=0.3)
    
    # Panel 6: Distribución de retornos con colas
    ax = axes[2, 1]
    
    # Histograma
    returns_pct = returns * 100
    ax.hist(returns_pct, bins=100, density=True, alpha=0.7, color='steelblue',
           label='Retornos reales')
    
    # Ajustar normal
    x = np.linspace(returns_pct.min(), returns_pct.max(), 1000)
    normal_pdf = stats.norm.pdf(x, returns_pct.mean(), returns_pct.std())
    ax.plot(x, normal_pdf, 'r-', linewidth=2, label='Normal ajustada')
    
    ax.set_xlabel('Retorno (%)')
    ax.set_ylabel('Densidad')
    ax.set_title('Distribución de Retornos\n(Colas más pesadas que Normal)')
    ax.legend()
    ax.set_yscale('log')  # Log scale para ver las colas
    ax.grid(True, alpha=0.3)
    
    plt.suptitle(f'Backtesting VaR {alpha:.0%} - S&P 500', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'var_backtesting.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✓ Guardado: var_backtesting.png")


def plot_eventos_extremos(data, all_results):
    """
    Análisis de los eventos más extremos.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Los 20 peores días
    returns = data['Returns'].sort_values()
    worst_20 = returns.head(20)
    
    ax = axes[0]
    bars = ax.barh(range(len(worst_20)), -worst_20.values * 100, color='crimson', alpha=0.7)
    ax.set_yticks(range(len(worst_20)))
    ax.set_yticklabels([d.strftime('%Y-%m-%d') for d in worst_20.index])
    ax.set_xlabel('Pérdida (%)')
    ax.set_title('Top 20 Peores Días del S&P 500')
    ax.grid(True, alpha=0.3, axis='x')
    
    # ¿Cuántas sigmas?
    mu = data['Returns'].mean()
    sigma = data['Returns'].std()
    
    ax = axes[1]
    sigmas = (worst_20 - mu) / sigma
    bars = ax.barh(range(len(sigmas)), -sigmas.values, color='darkred', alpha=0.7)
    ax.set_yticks(range(len(sigmas)))
    ax.set_yticklabels([d.strftime('%Y-%m-%d') for d in sigmas.index])
    ax.set_xlabel('Desviaciones estándar (σ)')
    ax.set_title('¿Cuántas σ? (En Normal, >6σ es "imposible")')
    ax.axvline(x=6, color='orange', linestyle='--', label='6σ')
    ax.axvline(x=4, color='yellow', linestyle='--', label='4σ')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'var_eventos_extremos.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Guardado: var_eventos_extremos.png")
    
    # Imprimir análisis
    print("\n" + "="*60)
    print("EVENTOS EXTREMOS: ¿Por qué el VaR Normal falla?")
    print("="*60)
    
    # Contar eventos por número de sigmas
    all_sigmas = np.abs((data['Returns'] - mu) / sigma)
    
    print(f"\n{'Evento':>15} {'Observados':>12} {'Esperados (Normal)':>20} {'Ratio':>10}")
    print("-"*60)
    
    n = len(data)
    for threshold in [3, 4, 5, 6, 7, 8]:
        observed = (all_sigmas > threshold).sum()
        # Probabilidad en normal de exceder threshold sigmas (dos colas)
        expected = n * 2 * (1 - stats.norm.cdf(threshold))
        ratio = observed / expected if expected > 0 else np.inf
        print(f">{threshold}σ{' ':>12} {observed:>12} {expected:>20.2f} {ratio:>10.1f}x")


def imprimir_conclusiones(diagnostico):
    """Imprime las conclusiones del análisis."""
    print("\n" + "="*70)
    print("CONCLUSIONES")
    print("="*70)
    
    alpha = diagnostico['alpha_hill']
    
    print(f"""
    📊 Índice de cola estimado: α̂ = {alpha:.2f}
    
    🎯 ¿Qué significa esto?
    """)
    
    if alpha > 4:
        print("    - Kurtosis finita → distribución 'casi' normal")
        print("    - VaR Normal puede funcionar razonablemente")
    elif alpha > 2:
        print("    - Varianza finita, kurtosis INFINITA")
        print("    - VaR Normal SUBESTIMA el riesgo")
        print("    - Los eventos extremos son MÁS frecuentes de lo que Normal predice")
    else:
        print("    - ¡VARIANZA INFINITA!")
        print("    - VaR es fundamentalmente inestable")
        print("    - Cualquier estimación paramétrica es poco confiable")
    
    print("""
    ⚠️  POR QUÉ STUDENT-T NO ES LA SOLUCIÓN:
    
        - Student-t(ν=4) tiene α=4, lo que da kurtosis infinita
        - PERO los momentos 1, 2, 3 son finitos
        - La cola de Student-t decae como t^(-ν-1), no como x^(-α)
        - Esto significa que Student-t SUBESTIMA los eventos extremos
        - Es una "falsa solución" que da sensación de seguridad
    
    ✅ MEJORES ALTERNATIVAS:
    
        1. VaR Histórico: No asume ninguna distribución
        2. EVT (GPD): Modela solo la cola, más robusto
        3. Expected Shortfall: Captura la severidad, no solo la frecuencia
        4. Simulación Monte Carlo con colas pesadas reales (Pareto)
    
    📚 Referencia: Taleb, "Statistical Consequences of Fat Tails"
    """)


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*70)
    print("EJERCICIO: EL FRAUDE DEL VALUE AT RISK")
    print("¿Por qué las métricas tradicionales de riesgo fallan?")
    print("="*70)
    
    # Descargar datos
    data = descargar_datos()
    
    # Diagnóstico de colas
    diagnostico = diagnostico_colas(data['Returns'])
    
    # Backtesting
    all_results, metodos = backtest_completo(data)
    
    # Visualizaciones
    print("\n📊 Generando visualizaciones...")
    plot_backtesting(data, all_results, metodos)
    plot_eventos_extremos(data, all_results)
    
    # Conclusiones
    imprimir_conclusiones(diagnostico)
    
    print("\n" + "="*70)
    print("✅ Ejercicio completado!")
    print(f"   Imágenes guardadas en: {OUTPUT_DIR}")
    print("="*70)


if __name__ == "__main__":
    main()
