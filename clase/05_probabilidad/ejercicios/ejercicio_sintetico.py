#!/usr/bin/env python3
"""
Ejercicio: Diagnóstico de Fat Tails (Metodología Taleb)

¿Cómo saber si una distribución tiene colas largas?
Este ejercicio enseña los métodos correctos para detectar fat tails.

IMPORTANTE: Student-t NO es fat-tailed suficiente porque tiene momentos finitos.
Las verdaderas fat tails (Pareto, Cauchy, Lévy) tienen momentos infinitos.

Ejecutar:
    python ejercicio_sintetico.py

Autor: Módulo de Probabilidad - IA P26
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# Configuración
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'DejaVu Sans'  # Supports Unicode glyphs (✓, ✗, etc.)

# Crear directorio de outputs organizado
OUTPUT_DIR = Path(__file__).parent / "images" / "sintetico"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Semilla para reproducibilidad
np.random.seed(42)


# =============================================================================
# DISTRIBUCIONES DE PRUEBA
# =============================================================================

def generar_distribuciones(n=10000):
    """
    Genera muestras de diferentes distribuciones.
    
    CLASIFICACIÓN según Taleb:
    - Thin-tailed: Normal, Exponencial (todos los momentos existen)
    - Sub-exponencial pero no power-law: Lognormal, Weibull
    - Fat-tailed (power-law): Pareto, Cauchy, Student-t con ν pequeño
    
    La diferencia clave: ¿Existe E[X^k] para todo k?
    """
    distribuciones = {
        # === THIN TAILS (Mediocristan) ===
        'Normal': {
            'data': np.random.normal(0, 1, n),
            'tipo': 'thin',
            'alpha': np.inf,  # Todos los momentos existen
            'descripcion': 'Todos los momentos finitos, colas exponenciales'
        },
        'Exponencial': {
            'data': np.random.exponential(1, n),
            'tipo': 'thin', 
            'alpha': np.inf,
            'descripcion': 'Todos los momentos finitos'
        },
        
        # === TRANSICIÓN (cuidado!) ===
        'Lognormal': {
            'data': np.random.lognormal(0, 1, n),
            'tipo': 'sub-exponential',
            'alpha': np.inf,  # Momentos finitos pero colas pesadas
            'descripcion': 'Momentos finitos pero concentración alta'
        },
        
        # === FAT TAILS (Extremistan) ===
        'Pareto(α=3)': {
            'data': (np.random.pareto(3, n) + 1),  # Pareto shifted
            'tipo': 'fat',
            'alpha': 3,  # Media y varianza existen, pero kurtosis infinita
            'descripcion': 'E[X], Var[X] existen, kurtosis infinita'
        },
        'Pareto(α=2)': {
            'data': (np.random.pareto(2, n) + 1),
            'tipo': 'fat',
            'alpha': 2,  # Solo media existe, varianza infinita!
            'descripcion': 'E[X] existe, Var[X] = ∞'
        },
        'Pareto(α=1.5)': {
            'data': (np.random.pareto(1.5, n) + 1),
            'tipo': 'fat',
            'alpha': 1.5,  # Media infinita!
            'descripcion': 'E[X] = ∞, no converge nunca'
        },
        'Cauchy': {
            'data': np.random.standard_cauchy(n),
            'tipo': 'fat',
            'alpha': 1,  # Ningún momento existe
            'descripcion': 'Ningún momento existe, α=1'
        },
        
        # === FALSO FAT TAIL (¡Trampa común!) ===
        'Student-t(ν=4)': {
            'data': np.random.standard_t(4, n),
            'tipo': 'pseudo-fat',  # Parece fat pero no lo es realmente
            'alpha': 4,  # Kurtosis infinita, pero momentos 1,2,3 finitos
            'descripcion': '¡TRAMPA! Parece fat pero todos los momentos <4 existen'
        },
    }
    
    return distribuciones


# =============================================================================
# DIAGNÓSTICOS DE FAT TAILS (Metodología Taleb)
# =============================================================================

def hill_estimator(data, k=None):
    """
    Estimador de Hill para el índice de cola α.
    
    Solo usa las k observaciones más grandes.
    α < 2: varianza infinita
    α < 1: media infinita
    
    Referencia: Taleb, "Statistical Consequences of Fat Tails"
    """
    sorted_data = np.sort(np.abs(data))[::-1]  # Ordenar descendente
    n = len(sorted_data)
    
    if k is None:
        k = int(np.sqrt(n))  # Regla de dedo
    
    k = min(k, n - 1)
    
    # Estimador de Hill
    log_ratios = np.log(sorted_data[:k] / sorted_data[k])
    alpha_hat = k / np.sum(log_ratios)
    
    return alpha_hat


def kappa_taleb(data):
    """
    Criterio Kappa de Taleb.
    
    κ = max(X) / sum(X)
    
    Interpretación:
    - κ → 0: thin tails (muchas observaciones contribuyen)
    - κ → 1: fat tails (una observación domina)
    
    En Mediocristan: κ ≈ 1/n → 0
    En Extremistan: κ permanece alto
    """
    data_pos = np.abs(data)
    return np.max(data_pos) / np.sum(data_pos)


def mean_excess_function(data, thresholds=None):
    """
    Función de Exceso Medio: E[X - u | X > u]
    
    Para distribuciones fat-tailed, esta función CRECE con u.
    Para thin-tails (exponencial), es CONSTANTE.
    
    Es el diagnóstico más importante según Taleb.
    """
    data_pos = np.abs(data)
    
    if thresholds is None:
        thresholds = np.percentile(data_pos, np.linspace(50, 99, 50))
    
    mean_excess = []
    for u in thresholds:
        excesses = data_pos[data_pos > u] - u
        if len(excesses) > 10:
            mean_excess.append(np.mean(excesses))
        else:
            mean_excess.append(np.nan)
    
    return thresholds, np.array(mean_excess)


def log_log_survival(data, bins=50):
    """
    Gráfico log-log de la función de supervivencia.
    
    Si P(X > x) ~ x^(-α), entonces en log-log es lineal con pendiente -α.
    
    Thin tails: curva hacia abajo (caída exponencial)
    Fat tails: línea recta (power law)
    """
    data_pos = np.abs(data[data != 0])
    sorted_data = np.sort(data_pos)
    n = len(sorted_data)
    
    # Función de supervivencia empírica
    survival = 1 - np.arange(1, n + 1) / n
    
    return sorted_data, survival


def max_to_sum_ratio_evolution(data, window_sizes=None):
    """
    Evolución del ratio max/sum con el tamaño de muestra.
    
    En thin tails: converge a 0 como O(1/n)
    En fat tails: permanece alto o converge muy lentamente
    """
    if window_sizes is None:
        window_sizes = np.logspace(1, np.log10(len(data)), 50).astype(int)
        window_sizes = np.unique(window_sizes)
    
    ratios = []
    for n in window_sizes:
        sample = np.abs(data[:n])
        ratios.append(np.max(sample) / np.sum(sample))
    
    return window_sizes, np.array(ratios)


# =============================================================================
# VISUALIZACIÓN
# =============================================================================

def plot_diagnosticos_completos(distribuciones):
    """
    Genera un panel completo de diagnósticos para cada distribución.
    """
    print("="*70)
    print("DIAGNÓSTICOS DE FAT TAILS (Metodología Taleb)")
    print("="*70)
    
    # 1. Panel comparativo de todos los diagnósticos
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    colores = plt.cm.Set1(np.linspace(0, 1, len(distribuciones)))
    
    # --- Panel 1: Log-Log Survival ---
    ax = axes[0, 0]
    for (nombre, info), color in zip(distribuciones.items(), colores):
        x, surv = log_log_survival(info['data'])
        # Submuestrear para visualización
        idx = np.logspace(0, np.log10(len(x)-1), 200).astype(int)
        ax.plot(x[idx], surv[idx], label=nombre, color=color, alpha=0.7)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('x')
    ax.set_ylabel('P(X > x)')
    ax.set_title('Función de Supervivencia (Log-Log)\nLineal = Power Law = Fat Tail')
    ax.legend(fontsize=8, loc='lower left')
    ax.grid(True, alpha=0.3)
    
    # --- Panel 2: Mean Excess Function ---
    ax = axes[0, 1]
    for (nombre, info), color in zip(distribuciones.items(), colores):
        u, me = mean_excess_function(info['data'])
        # Normalizar para comparar
        if not np.all(np.isnan(me)):
            me_norm = me / np.nanmax(me)
            ax.plot(u / np.max(u), me_norm, label=nombre, color=color, alpha=0.7)
    
    ax.set_xlabel('Umbral u (normalizado)')
    ax.set_ylabel('E[X-u | X>u] (normalizado)')
    ax.set_title('Mean Excess Function\nCreciente = Fat Tail')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # --- Panel 3: Kappa Evolution ---
    ax = axes[0, 2]
    for (nombre, info), color in zip(distribuciones.items(), colores):
        ns, kappas = max_to_sum_ratio_evolution(info['data'])
        ax.plot(ns, kappas, label=nombre, color=color, alpha=0.7)
    
    ax.set_xscale('log')
    ax.set_xlabel('n (tamaño de muestra)')
    ax.set_ylabel('κ = max/sum')
    ax.set_title('Criterio Kappa de Taleb\nAlto = Fat Tail')
    ax.axhline(y=0.01, color='gray', linestyle='--', alpha=0.5, label='κ=0.01')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # --- Panel 4: Histograma con colas ---
    ax = axes[1, 0]
    for (nombre, info), color in zip(distribuciones.items(), colores):
        data = info['data']
        # Solo valores absolutos, enfocarse en la cola
        data_abs = np.abs(data)
        p95 = np.percentile(data_abs, 95)
        tail_data = data_abs[data_abs > p95]
        if len(tail_data) > 10:
            ax.hist(tail_data, bins=30, alpha=0.4, label=nombre, 
                   color=color, density=True)
    
    ax.set_xlabel('|x| (cola: >95 percentil)')
    ax.set_ylabel('Densidad')
    ax.set_title('Distribución de la Cola (>95%)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # --- Panel 5: Hill Estimator por k ---
    ax = axes[1, 1]
    for (nombre, info), color in zip(distribuciones.items(), colores):
        data = info['data']
        ks = np.arange(10, int(np.sqrt(len(data))*2), 10)
        alphas = [hill_estimator(data, k) for k in ks]
        ax.plot(ks, alphas, label=f"{nombre} (α={info['alpha']})", 
               color=color, alpha=0.7)
    
    ax.axhline(y=2, color='red', linestyle='--', label='α=2 (Var=∞)')
    ax.axhline(y=1, color='darkred', linestyle='--', label='α=1 (E[X]=∞)')
    ax.set_xlabel('k (observaciones usadas)')
    ax.set_ylabel('α estimado (Hill)')
    ax.set_title('Estimador de Hill\nα<2 → Varianza infinita')
    ax.legend(fontsize=7, loc='upper right')
    ax.set_ylim(0, 6)
    ax.grid(True, alpha=0.3)
    
    # --- Panel 6: Tabla resumen ---
    ax = axes[1, 2]
    ax.axis('off')
    
    # Calcular métricas
    table_data = []
    for nombre, info in distribuciones.items():
        data = info['data']
        alpha_hill = hill_estimator(data)
        kappa = kappa_taleb(data)
        tipo = info['tipo']
        
        table_data.append([
            nombre[:15],
            f"{info['alpha']:.1f}" if info['alpha'] != np.inf else "∞",
            f"{alpha_hill:.2f}",
            f"{kappa:.4f}",
            tipo
        ])
    
    table = ax.table(
        cellText=table_data,
        colLabels=['Distribución', 'α real', 'α̂ (Hill)', 'κ', 'Tipo'],
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    
    # Colorear por tipo
    for i, row in enumerate(table_data):
        tipo = row[4]
        if tipo == 'fat':
            color = '#ffcccc'
        elif tipo == 'thin':
            color = '#ccffcc'
        elif tipo == 'pseudo-fat':
            color = '#ffffcc'
        else:
            color = '#cce5ff'
        for j in range(5):
            table[(i+1, j)].set_facecolor(color)
    
    ax.set_title('Resumen de Diagnósticos\n[Red] Fat | [Green] Thin | [Blue] Pseudo-fat')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'diagnosticos_fattails.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Guardado: diagnosticos_fattails.png")


def plot_convergencia_comparativa(distribuciones, n_runs=20):
    """
    Muestra por qué fat tails rompen la Ley de Grandes Números.
    """
    print("\n" + "="*70)
    print("CONVERGENCIA DE LA MEDIA (¿Por qué falla LGN?)")
    print("="*70)
    
    n_max = 10000
    ns = np.arange(1, n_max + 1)
    
    # Seleccionar distribuciones representativas
    seleccion = ['Normal', 'Pareto(α=3)', 'Pareto(α=1.5)', 'Cauchy']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    for ax, nombre in zip(axes.flat, seleccion):
        info = distribuciones[nombre]
        alpha = info['alpha']
        
        for _ in range(n_runs):
            # Generar nueva muestra
            if 'Pareto' in nombre:
                a = float(nombre.split('=')[1].rstrip(')'))
                data = (np.random.pareto(a, n_max) + 1)
            elif nombre == 'Normal':
                data = np.random.normal(0, 1, n_max)
            elif nombre == 'Cauchy':
                data = np.random.standard_cauchy(n_max)
            
            running_mean = np.cumsum(data) / ns
            ax.plot(ns, running_mean, alpha=0.3, linewidth=0.5)
        
        # Anotaciones
        if alpha > 1:
            # Calcular media teórica para Pareto
            if 'Pareto' in nombre:
                a = float(nombre.split('=')[1].rstrip(')'))
                media = a / (a - 1) if a > 1 else np.nan
            else:
                media = 0
            
            if not np.isnan(media):
                ax.axhline(y=media, color='red', linestyle='--', linewidth=2)
                
            if alpha > 2:
                ax.annotate('LGN ✓ TLC ✓\nConverge rápido',
                           xy=(0.98, 0.98), xycoords='axes fraction',
                           ha='right', va='top',
                           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
            else:
                ax.annotate('LGN ✓ (lento)\nTLC ✗',
                           xy=(0.98, 0.98), xycoords='axes fraction',
                           ha='right', va='top',
                           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        else:
            ax.annotate('LGN ✗ TLC ✗\n¡NO CONVERGE!\nμ = ∞',
                       xy=(0.98, 0.98), xycoords='axes fraction',
                       ha='right', va='top', fontweight='bold',
                       bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
        
        ax.set_xscale('log')
        ax.set_xlabel('n')
        ax.set_ylabel('Promedio acumulado')
        ax.set_title(f'{nombre}\nα = {alpha}')
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('Convergencia del Promedio: Fat Tails vs Thin Tails', fontsize=14)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'convergencia_fattails.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Guardado: convergencia_fattails.png")


def plot_impacto_cisne_negro(distribuciones):
    """
    Demuestra cómo UN evento extremo cambia todo en fat tails.
    """
    print("\n" + "="*70)
    print("IMPACTO DEL CISNE NEGRO")
    print("="*70)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    n = 1000
    
    # Normal: un extremo no importa
    ax = axes[0]
    normal_data = np.random.normal(0, 1, n)
    medias_sin = np.cumsum(normal_data) / np.arange(1, n+1)
    
    # Agregar "cisne negro" en posición 500
    normal_con_cisne = normal_data.copy()
    normal_con_cisne[500] = 10  # 10 sigmas - "imposible"
    medias_con = np.cumsum(normal_con_cisne) / np.arange(1, n+1)
    
    ax.plot(medias_sin, label='Sin cisne negro', alpha=0.7)
    ax.plot(medias_con, label='Con cisne negro (10σ)', alpha=0.7)
    ax.axvline(x=500, color='red', linestyle='--', alpha=0.5)
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax.set_xlabel('n')
    ax.set_ylabel('Media acumulada')
    ax.set_title('Normal: Cisne negro se "absorbe"')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Pareto α=2: un extremo importa más
    ax = axes[1]
    pareto_data = np.random.pareto(2, n) + 1
    medias_sin = np.cumsum(pareto_data) / np.arange(1, n+1)
    
    pareto_con_cisne = pareto_data.copy()
    cisne = np.max(pareto_data) * 10  # Cisne negro = 10x el máximo
    pareto_con_cisne[500] = cisne
    medias_con = np.cumsum(pareto_con_cisne) / np.arange(1, n+1)
    
    ax.plot(medias_sin, label='Sin cisne negro', alpha=0.7)
    ax.plot(medias_con, label=f'Con cisne negro ({cisne:.0f})', alpha=0.7)
    ax.axvline(x=500, color='red', linestyle='--', alpha=0.5)
    ax.set_xlabel('n')
    ax.set_ylabel('Media acumulada')
    ax.set_title('Pareto(α=2): Cisne negro distorsiona')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Cauchy: un extremo domina todo
    ax = axes[2]
    cauchy_data = np.random.standard_cauchy(n)
    # Limitar para visualización
    cauchy_data = np.clip(cauchy_data, -100, 100)
    medias_sin = np.cumsum(cauchy_data) / np.arange(1, n+1)
    
    cauchy_con_cisne = cauchy_data.copy()
    cauchy_con_cisne[500] = 1000  # Cisne negro extremo
    medias_con = np.cumsum(cauchy_con_cisne) / np.arange(1, n+1)
    
    ax.plot(medias_sin, label='Sin cisne negro', alpha=0.7)
    ax.plot(medias_con, label='Con cisne negro (1000)', alpha=0.7)
    ax.axvline(x=500, color='red', linestyle='--', alpha=0.5)
    ax.set_xlabel('n')
    ax.set_ylabel('Media acumulada')
    ax.set_title('Cauchy: Cisne negro DOMINA')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.suptitle('Una Observación Cambia Todo (en Fat Tails)', fontsize=14)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'cisne_negro_impacto.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Guardado: cisne_negro_impacto.png")


def plot_student_t_trampa():
    """
    Explica por qué Student-t es una TRAMPA como modelo de fat tails.
    """
    print("\n" + "="*70)
    print("¿POR QUÉ STUDENT-T ES UNA TRAMPA?")
    print("="*70)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    n = 50000
    
    # Panel 1: Comparación de colas
    ax = axes[0]
    
    # Generar datos
    normal = np.random.normal(0, 1, n)
    t4 = np.random.standard_t(4, n)  # Student-t con 4 gl
    pareto = np.random.pareto(2, n) + 1 - 2  # Centrada aprox en 0
    cauchy = np.random.standard_cauchy(n)
    
    # Función de supervivencia en log-log
    for data, nombre, color in [
        (normal, 'Normal', 'blue'),
        (t4, 'Student-t(ν=4)', 'orange'),
        (pareto, 'Pareto(α=2)', 'red'),
        (cauchy, 'Cauchy(α=1)', 'purple')
    ]:
        x, surv = log_log_survival(data)
        idx = np.logspace(0, np.log10(len(x)-1), 200).astype(int)
        ax.plot(x[idx], surv[idx], label=nombre, color=color, linewidth=2, alpha=0.7)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('|x|')
    ax.set_ylabel('P(|X| > x)')
    ax.set_title('Student-t: ¿Fat tail de verdad?\n(Log-log: línea recta = power law)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Panel 2: Tabla de momentos
    ax = axes[1]
    ax.axis('off')
    
    table_data = [
        ['Normal', '∞', '✓', '✓', '✓', '✓', 'Thin'],
        ['Student-t(ν=4)', '4', '✓', '✓', '✓', '✗', '¡TRAMPA!'],
        ['Student-t(ν=3)', '3', '✓', '✓', '✗', '✗', '¡TRAMPA!'],
        ['Pareto(α=3)', '3', '✓', '✓', '✗', '✗', 'Fat'],
        ['Pareto(α=2)', '2', '✓', '✗', '✗', '✗', 'Fat'],
        ['Cauchy', '1', '✗', '✗', '✗', '✗', 'Fat'],
    ]
    
    table = ax.table(
        cellText=table_data,
        colLabels=['Distribución', 'α', 'E[X]', 'E[X²]', 'E[X³]', 'E[X⁴]', 'Tipo'],
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.3, 2)
    
    # Colorear
    colors = ['#ccffcc', '#ffffcc', '#ffffcc', '#ffcccc', '#ffcccc', '#ffcccc']
    for i, color in enumerate(colors):
        for j in range(7):
            table[(i+1, j)].set_facecolor(color)
    
    ax.set_title('Momentos Existentes\n✓ = finito, ✗ = infinito\n\n'
                'Student-t(ν) tiene α=ν, pero NO es igual a Pareto(α=ν)!\n'
                'Student-t converge más rápido en la cola.',
                fontsize=11)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'student_t_trampa.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Guardado: student_t_trampa.png")
    
    print("\n⚠️  CONCLUSIÓN:")
    print("   Student-t tiene el mismo α que Pareto, pero:")
    print("   - Sus colas decaen como t^(-α-1), no como x^(-α)")
    print("   - Converge a Normal más rápido")
    print("   - NO captura los eventos extremos reales")
    print("   - Usar Student-t para 'modelar fat tails' es SUBESTIMAR el riesgo")


def imprimir_resumen(distribuciones):
    """Imprime un resumen de los diagnósticos."""
    print("\n" + "="*70)
    print("RESUMEN: CÓMO DETECTAR FAT TAILS")
    print("="*70)
    
    print("\n📊 Resultados por distribución:\n")
    print(f"{'Distribución':<20} {'α real':>8} {'α̂ Hill':>8} {'κ':>10} {'Tipo':<15}")
    print("-" * 65)
    
    for nombre, info in distribuciones.items():
        alpha_real = info['alpha']
        alpha_hill = hill_estimator(info['data'])
        kappa = kappa_taleb(info['data'])
        tipo = info['tipo']
        
        alpha_str = f"{alpha_real:.1f}" if alpha_real != np.inf else "∞"
        print(f"{nombre:<20} {alpha_str:>8} {alpha_hill:>8.2f} {kappa:>10.5f} {tipo:<15}")
    
    print("\n" + "="*70)
    print("REGLAS PRÁCTICAS (Taleb):")
    print("="*70)
    print("""
    1. ESTIMADOR DE HILL (α):
       - α > 2: Varianza finita, TLC funciona (pero puede ser lento)
       - 1 < α ≤ 2: Varianza infinita, TLC NO funciona
       - α ≤ 1: Media infinita, LGN NO funciona
    
    2. KAPPA (κ = max/sum):
       - κ → 0 cuando n→∞: Thin tails (Mediocristan)
       - κ permanece alto: Fat tails (Extremistan)
       - Regla: κ > 0.01 con n=10000 es sospechoso
    
    3. MEAN EXCESS FUNCTION:
       - Constante: Exponencial (thin)
       - Creciente: Fat tail
       - Decreciente: Thin tail
    
    4. LOG-LOG SURVIVAL:
       - Línea recta: Power law (fat tail)
       - Curva hacia abajo: Thin tail
    
    ⚠️  ADVERTENCIA: Student-t NO es suficiente para modelar riesgo real.
        Usar Student-t es subestimar los eventos extremos.
    """)


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*70)
    print("EJERCICIO: DIAGNÓSTICO DE FAT TAILS")
    print("Metodología de Nassim Taleb")
    print("="*70)
    
    # Generar distribuciones
    print("\n📊 Generando distribuciones de prueba...")
    distribuciones = generar_distribuciones(n=10000)
    
    # Diagnósticos
    plot_diagnosticos_completos(distribuciones)
    plot_convergencia_comparativa(distribuciones)
    plot_impacto_cisne_negro(distribuciones)
    plot_student_t_trampa()
    
    # Resumen
    imprimir_resumen(distribuciones)
    
    print("\n" + "="*70)
    print("✅ Ejercicio completado!")
    print(f"   Imágenes guardadas en: {OUTPUT_DIR}")
    print("="*70)


if __name__ == "__main__":
    main()
