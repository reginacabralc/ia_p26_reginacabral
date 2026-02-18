#!/usr/bin/env python3
"""
Laboratorio de Probabilidad: Simulaciones Interactivas

Este script genera visualizaciones para entender:
1. Ley de los Grandes Números (LGN)
2. Teorema del Límite Central (TLC)
3. Colas Largas (Fat Tails) y su comportamiento

Estilo inspirado en: Taleb, "Statistical Consequences of Fat Tails" (2020)

Uso:
    python lab_probabilidad.py

Genera imágenes en la carpeta 'images/' que se referencian en las notas de clase.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Configuración global de estilo
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 10

# Colores consistentes
COLORS = {
    'normal': '#2E86AB',      # Azul
    'pareto': '#E94F37',      # Rojo
    'cauchy': '#F39C12',      # Naranja
    'true_mean': '#27AE60',   # Verde
    'convergence_band': '#BDC3C7',
}

# Crear directorio de imágenes si no existe
IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Semilla para reproducibilidad
np.random.seed(42)


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def add_convergence_annotation(ax, convergence_type, n_convergence=None):
    """
    Añade anotación sobre convergencia.
    convergence_type: 'fast', 'slow', 'none'
    """
    if convergence_type == 'fast':
        ax.annotate(f'LGN ✓ TLC ✓\nConverge rápido', 
                   xy=(0.95, 0.95), xycoords='axes fraction',
                   ha='right', va='top',
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
                   fontsize=9)
    elif convergence_type == 'slow':
        ax.annotate('LGN ✓ (lento) TLC ✗\nConverge pero MUY lento', 
                   xy=(0.95, 0.95), xycoords='axes fraction',
                   ha='right', va='top',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8),
                   fontsize=9)
    elif convergence_type == 'none':
        ax.annotate('LGN ✗ TLC ✗\nNO CONVERGE\n(μ no existe)', 
                   xy=(0.95, 0.95), xycoords='axes fraction',
                   ha='right', va='top',
                   bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8),
                   fontsize=9, fontweight='bold')


def compute_running_stats(data):
    """Calcula estadísticas acumuladas."""
    n = len(data)
    ns = np.arange(1, n + 1)
    running_mean = np.cumsum(data) / ns
    
    # Running max contribution (κ de Taleb)
    running_max = np.maximum.accumulate(data)
    running_sum = np.cumsum(data)
    running_kappa = running_max / np.maximum(running_sum, 1e-10)
    
    return running_mean, running_kappa


# =============================================================================
# 1. DISTRIBUCIONES DE PROBABILIDAD
# =============================================================================

def plot_distribuciones_comparacion():
    """
    Compara las principales distribuciones de probabilidad.
    Énfasis en la diferencia entre colas ligeras y pesadas.
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Normal
    ax = axes[0, 0]
    x = np.linspace(-4, 4, 1000)
    for mu, sigma, label in [(0, 1, 'μ=0, σ=1'), (0, 0.5, 'μ=0, σ=0.5'), (1, 1, 'μ=1, σ=1')]:
        ax.plot(x, stats.norm.pdf(x, mu, sigma), label=label, linewidth=2)
    ax.set_title('Normal (Gaussiana)\nμ y σ² finitas')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    
    # Exponencial
    ax = axes[0, 1]
    x = np.linspace(0, 5, 1000)
    for lam in [0.5, 1, 2]:
        ax.plot(x, stats.expon.pdf(x, scale=1/lam), label=f'λ={lam}', linewidth=2)
    ax.set_title('Exponencial\nCola ligera (decae exp.)')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    
    # Log-Normal
    ax = axes[0, 2]
    x = np.linspace(0.01, 8, 1000)
    for sigma in [0.25, 0.5, 1]:
        ax.plot(x, stats.lognorm.pdf(x, sigma), label=f'σ={sigma}', linewidth=2)
    ax.set_title('Log-Normal\nAsimétrica, cola moderada')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    
    # Pareto (Fat-tailed)
    ax = axes[1, 0]
    x = np.linspace(1, 10, 1000)
    for alpha in [1.5, 2, 3]:
        label = f'α={alpha}'
        if alpha <= 2:
            label += ' (σ²=∞)'
        ax.plot(x, stats.pareto.pdf(x, alpha), label=label, linewidth=2)
    ax.set_title('Pareto (Fat-tailed)\nP(X>x) ~ x⁻ᵅ')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    
    # Student-t vs Normal
    ax = axes[1, 1]
    x = np.linspace(-6, 6, 1000)
    ax.plot(x, stats.norm.pdf(x), label='Normal', linewidth=2, color='gray', linestyle='--')
    for df, color in [(1, COLORS['cauchy']), (3, COLORS['pareto']), (30, COLORS['normal'])]:
        label = f'ν={df}'
        if df == 1:
            label += ' (Cauchy)'
        ax.plot(x, stats.t.pdf(x, df), label=label, linewidth=2)
    ax.set_title('Student-t\nν→∞ se vuelve Normal')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    
    # Cauchy vs Normal (log scale) - CLAVE para ver las colas
    ax = axes[1, 2]
    x = np.linspace(-10, 10, 1000)
    ax.semilogy(x, stats.norm.pdf(x), label='Normal', linewidth=2, color=COLORS['normal'])
    ax.semilogy(x, stats.cauchy.pdf(x), label='Cauchy', linewidth=2, color=COLORS['cauchy'])
    ax.set_title('Cauchy vs Normal (escala log)\n¡Mira las colas!')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('f(x) [log scale]')
    ax.set_ylim(1e-6, 1)
    
    # Añadir anotación sobre las colas
    ax.annotate('Cauchy: colas\nmucho más pesadas', xy=(6, 0.01), 
                fontsize=9, color=COLORS['cauchy'])
    ax.annotate('Normal: colas\nligeras', xy=(4, 1e-5), 
                fontsize=9, color=COLORS['normal'])
    
    plt.suptitle('Comparación de Distribuciones de Probabilidad', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'distribuciones_comparacion.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: distribuciones_comparacion.png")


# =============================================================================
# 2. LEY DE LOS GRANDES NÚMEROS (LGN)
# =============================================================================

def plot_lgn_convergencia():
    """
    Demuestra la Ley de los Grandes Números con diferentes distribuciones.
    Muestra claramente la media teórica y la convergencia.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    n_max = 10000
    ns = np.arange(1, n_max + 1)
    
    distributions = [
        ('Moneda Justa (Bernoulli p=0.5)', lambda n: np.random.binomial(1, 0.5, n), 0.5, 0.5),
        ('Dado Justo (Uniforme 1-6)', lambda n: np.random.randint(1, 7, n), 3.5, np.sqrt(35/12)),
        ('Exponencial (λ=1)', lambda n: np.random.exponential(1, n), 1.0, 1.0),
        ('Uniforme [0,1]', lambda n: np.random.uniform(0, 1, n), 0.5, np.sqrt(1/12)),
    ]
    
    for ax, (name, sampler, true_mean, true_std) in zip(axes.flat, distributions):
        # Generar datos y calcular promedios acumulados
        data = sampler(n_max)
        running_mean = np.cumsum(data) / ns
        
        # Banda de convergencia teórica (±2σ/√n)
        band_upper = true_mean + 2 * true_std / np.sqrt(ns)
        band_lower = true_mean - 2 * true_std / np.sqrt(ns)
        
        # Plot
        ax.fill_between(ns, band_lower, band_upper, alpha=0.2, color=COLORS['convergence_band'],
                       label='Banda 95% teórica')
        ax.plot(ns, running_mean, color=COLORS['normal'], alpha=0.8, linewidth=1,
               label='Promedio acumulado')
        ax.axhline(y=true_mean, color=COLORS['true_mean'], linestyle='--', linewidth=2, 
                  label=f'μ verdadera = {true_mean}')
        
        ax.set_xlabel('Número de muestras (n)')
        ax.set_ylabel('Promedio muestral X̄ₙ')
        ax.set_title(name)
        ax.set_xscale('log')
        ax.legend(loc='upper right', fontsize=9)
        
        # Anotación del error final
        final_error = abs(running_mean[-1] - true_mean)
        ax.annotate(f'Error final: {final_error:.4f}', 
                   xy=(0.02, 0.02), xycoords='axes fraction',
                   fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.suptitle('Ley de los Grandes Números: X̄ₙ → μ cuando n → ∞', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'lgn_convergencia.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: lgn_convergencia.png")


# =============================================================================
# 3. TEOREMA DEL LÍMITE CENTRAL (TLC)
# =============================================================================

def plot_tlc_demo():
    """
    Demostración visual del TLC con diferentes distribuciones originales.
    """
    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    
    n_samples = 10000
    sample_sizes = [1, 2, 10, 30]
    
    distributions = [
        ('Uniforme [0,1]', lambda n: np.random.uniform(0, 1, n), 0.5, np.sqrt(1/12)),
        ('Exponencial (λ=1)', lambda n: np.random.exponential(1, n), 1.0, 1.0),
        ('Bernoulli (p=0.3)', lambda n: np.random.binomial(1, 0.3, n), 0.3, np.sqrt(0.3*0.7)),
    ]
    
    for row, (dist_name, sampler, mu, sigma) in enumerate(distributions):
        for col, n in enumerate(sample_sizes):
            ax = axes[row, col]
            
            # Generar muchas muestras de tamaño n y calcular su promedio
            means = np.array([sampler(n).mean() for _ in range(n_samples)])
            
            # Histograma
            ax.hist(means, bins=50, density=True, alpha=0.7, color=COLORS['normal'], 
                   edgecolor='white', label='Empírico')
            
            # Normal teórica según TLC
            theoretical_std = sigma / np.sqrt(n)
            x = np.linspace(means.min(), means.max(), 100)
            ax.plot(x, stats.norm.pdf(x, mu, theoretical_std), 
                   color=COLORS['true_mean'], linewidth=2, label='Normal (TLC)')
            
            # Línea vertical en la media
            ax.axvline(x=mu, color=COLORS['pareto'], linestyle='--', linewidth=1.5)
            
            if row == 0:
                ax.set_title(f'n = {n}', fontweight='bold')
            if col == 0:
                ax.set_ylabel(dist_name + '\n\nDensidad')
            if col == 3:
                ax.legend(fontsize=8)
            
            ax.set_xlabel('X̄ₙ')
    
    plt.suptitle('Teorema del Límite Central: La distribución de X̄ₙ se vuelve Normal', 
                fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'tlc_demo.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: tlc_demo.png")


# =============================================================================
# 4. FAT TAILS - ESTILO TALEB
# =============================================================================

def plot_tlc_vs_fattail():
    """
    CLAVE: Contrasta el TLC en distribuciones thin-tailed vs fat-tailed.
    Muestra claramente la media teórica y si converge o no.
    """
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    n_samples = 3000
    sample_sizes = [10, 100, 1000]
    
    # Fila 1: Normal (thin-tailed) - TLC FUNCIONA
    true_mean_normal = 0
    for col, n in enumerate(sample_sizes):
        ax = axes[0, col]
        means = np.array([np.random.normal(0, 1, n).mean() for _ in range(n_samples)])
        
        ax.hist(means, bins=50, density=True, alpha=0.7, color=COLORS['normal'], 
               edgecolor='white')
        
        # Normal teórica
        theoretical_std = 1 / np.sqrt(n)
        x = np.linspace(means.min(), means.max(), 100)
        ax.plot(x, stats.norm.pdf(x, 0, theoretical_std), 
               color=COLORS['true_mean'], linewidth=2, label='Normal teórica')
        
        ax.axvline(x=true_mean_normal, color=COLORS['true_mean'], linestyle='--', 
                  linewidth=2, label=f'μ = {true_mean_normal}')
        
        ax.set_title(f'n = {n}', fontweight='bold')
        ax.set_xlabel('X̄ₙ')
        if col == 0:
            ax.set_ylabel('NORMAL\n(TLC funciona)\n\nDensidad')
        ax.legend(fontsize=8)
        
        # Anotación de convergencia
        sample_mean = means.mean()
        ax.annotate(f'E[X̄] = {sample_mean:.3f}', xy=(0.02, 0.98), 
                   xycoords='axes fraction', va='top', fontsize=9,
                   bbox=dict(facecolor='lightgreen', alpha=0.8))
    
    # Fila 2: Pareto (fat-tailed, α=1.5) - TLC NO FUNCIONA
    alpha = 1.5
    # Para Pareto con α > 1, la media es α*xm/(α-1). Con xm=1: media = 1.5/0.5 = 3
    true_mean_pareto = alpha / (alpha - 1)  # = 3
    
    for col, n in enumerate(sample_sizes):
        ax = axes[1, col]
        means = np.array([stats.pareto.rvs(alpha, size=n).mean() for _ in range(n_samples)])
        
        # Limitar para visualización (hay outliers extremos)
        plot_max = np.percentile(means, 99)
        means_plot = means[means < plot_max]
        
        ax.hist(means_plot, bins=50, density=True, alpha=0.7, color=COLORS['pareto'], 
               edgecolor='white')
        
        ax.axvline(x=true_mean_pareto, color=COLORS['true_mean'], linestyle='--', 
                  linewidth=2, label=f'μ teórica = {true_mean_pareto:.1f}')
        
        ax.set_title(f'n = {n}', fontweight='bold')
        ax.set_xlabel('X̄ₙ')
        if col == 0:
            ax.set_ylabel(f'PARETO (α={alpha})\n(σ²=∞, TLC FALLA)\n\nDensidad')
        ax.legend(fontsize=8)
        
        # Anotación - notar que NO converge bien
        sample_mean = means.mean()
        sample_median = np.median(means)
        ax.annotate(f'E[X̄] = {sample_mean:.1f}\nMediana = {sample_median:.1f}', 
                   xy=(0.98, 0.98), xycoords='axes fraction', va='top', ha='right',
                   fontsize=9, bbox=dict(facecolor='lightyellow', alpha=0.8))
    
    plt.suptitle('TLC: Normal (σ² finita) vs Pareto (σ² = ∞)\n'
                'Con varianza infinita, el TLC NO aplica', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'tlc_vs_fattail.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: tlc_vs_fattail.png")


def plot_convergencia_fattail():
    """
    ESTILO TALEB: Muestra la convergencia (o falta de ella) del promedio.
    Cada línea es una simulación independiente.
    
    Tres regímenes:
    - α > 2: LGN y TLC funcionan (convergencia rápida)
    - 1 < α ≤ 2: LGN funciona pero MUY lento, TLC falla
    - α ≤ 1: Ni LGN ni TLC (media no existe)
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    n_max = 10000
    ns = np.arange(1, n_max + 1)
    n_runs = 30
    
    # (título, sampler, media_teórica, tipo_convergencia, color)
    scenarios = [
        ('Normal (μ=0, σ²=1)', 
         lambda n: np.random.normal(0, 1, n), 0, 'fast', COLORS['normal']),
        ('Pareto (α=3, μ=1.5, σ² finita)', 
         lambda n: stats.pareto.rvs(3, size=n), 1.5, 'fast', COLORS['normal']),
        ('Pareto (α=2, μ=2, σ²=∞)', 
         lambda n: stats.pareto.rvs(2, size=n), 2, 'slow', COLORS['pareto']),
        ('Pareto (α=1.5, μ=3, σ²=∞)', 
         lambda n: stats.pareto.rvs(1.5, size=n), 3, 'slow', COLORS['pareto']),
    ]
    
    for (title, sampler, true_mean, conv_type, color), ax in zip(scenarios, axes.flat):
        for i in range(n_runs):
            data = sampler(n_max)
            running_mean = np.cumsum(data) / ns
            ax.plot(ns, running_mean, alpha=0.4, linewidth=0.7, color=color)
        
        # Media teórica
        ax.axhline(y=true_mean, color=COLORS['true_mean'], linewidth=3, 
                  linestyle='--', label=f'μ teórica = {true_mean}')
        
        # Banda de "convergencia aceptable" (±20% de la media para ver mejor)
        band = 0.2 * abs(true_mean) if true_mean != 0 else 0.2
        ax.axhspan(true_mean - band, true_mean + band, alpha=0.15, 
                  color=COLORS['true_mean'], label='±20% de μ')
        
        ax.set_xlabel('Número de muestras (n)')
        ax.set_ylabel('Promedio acumulado X̄ₙ')
        ax.set_title(title, fontsize=11)
        ax.set_xscale('log')
        ax.legend(loc='upper right', fontsize=9)
        
        # Anotación de convergencia
        add_convergence_annotation(ax, conv_type)
        
        # Ajustar límites Y para mejor visualización
        if conv_type == 'fast':
            ax.set_ylim(true_mean - 1, true_mean + 1)
    
    plt.suptitle('Convergencia del Promedio: Comparando regímenes\n'
                '(30 simulaciones, n hasta 10,000)', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'convergencia_fattail.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: convergencia_fattail.png")


def plot_cauchy_no_convergencia():
    """
    CRÍTICO: Demuestra que el promedio de Cauchy NO converge.
    La media de Cauchy NO EXISTE (no es infinita, simplemente no existe).
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    n_max = 50000
    ns = np.arange(1, n_max + 1)
    n_runs = 30
    
    # Normal: converge a 0
    ax = axes[0]
    for i in range(n_runs):
        data = np.random.normal(0, 1, n_max)
        running_mean = np.cumsum(data) / ns
        ax.plot(ns, running_mean, alpha=0.5, linewidth=0.5, color=COLORS['normal'])
    
    ax.axhline(y=0, color=COLORS['true_mean'], linewidth=3, linestyle='--', label='μ = 0')
    ax.axhspan(-0.1, 0.1, alpha=0.2, color=COLORS['true_mean'])
    ax.set_xlabel('n')
    ax.set_ylabel('Promedio acumulado X̄ₙ')
    ax.set_title('Normal(0,1)\nμ = 0, σ² = 1', fontsize=12)
    ax.set_xscale('log')
    ax.set_ylim(-0.5, 0.5)
    ax.legend()
    add_convergence_annotation(ax, 'fast')
    
    # Cauchy: NO converge (la media NO EXISTE)
    ax = axes[1]
    for i in range(n_runs):
        data = stats.cauchy.rvs(size=n_max)
        running_mean = np.cumsum(data) / ns
        ax.plot(ns, running_mean, alpha=0.5, linewidth=0.5, color=COLORS['cauchy'])
    
    ax.axhline(y=0, color='gray', linewidth=1, linestyle=':', alpha=0.5)
    ax.set_xlabel('n')
    ax.set_ylabel('Promedio acumulado X̄ₙ')
    ax.set_title('Cauchy(0,1)\n¡La media NO EXISTE!', fontsize=12)
    ax.set_xscale('log')
    ax.legend(['Simulaciones'])
    add_convergence_annotation(ax, 'none')
    
    # Texto explicativo
    ax.text(0.5, 0.05, 
           'El promedio de n variables Cauchy\n'
           'sigue siendo Cauchy.\n'
           'No importa cuántos datos tengas,\n'
           'el promedio NUNCA converge.',
           transform=ax.transAxes, fontsize=10,
           verticalalignment='bottom', horizontalalignment='center',
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    plt.suptitle('Normal (converge) vs Cauchy (NO converge) — 30 simulaciones cada una', 
                fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'cauchy_no_convergencia.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: cauchy_no_convergencia.png")


def plot_kappa_taleb():
    """
    ESTILO TALEB: El criterio κ = max(X)/sum(X)
    Mide qué tan concentrada está la distribución en los extremos.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    n = 1000
    n_simulations = 500
    
    distributions = [
        ('Normal |X|', lambda: np.abs(np.random.normal(0, 1, n)), COLORS['normal']),
        ('Exponencial', lambda: np.random.exponential(1, n), COLORS['normal']),
        ('Pareto (α=2.5)', lambda: stats.pareto.rvs(2.5, size=n), COLORS['pareto']),
        ('Pareto (α=1.5)', lambda: stats.pareto.rvs(1.5, size=n), COLORS['pareto']),
    ]
    
    for ax, (name, sampler, color) in zip(axes.flat, distributions):
        kappas = []
        max_contributions = []
        
        for _ in range(n_simulations):
            data = sampler()
            kappa = data.max() / data.sum()
            kappas.append(kappa)
            max_contributions.append(data.max())
        
        ax.hist(kappas, bins=50, density=True, alpha=0.7, color=color, edgecolor='white')
        
        mean_kappa = np.mean(kappas)
        ax.axvline(x=mean_kappa, color='black', linestyle='--', linewidth=2,
                  label=f'κ medio = {mean_kappa:.3f}')
        
        # Línea de referencia: si todos contribuyen igual, κ = 1/n
        ax.axvline(x=1/n, color=COLORS['true_mean'], linestyle=':', linewidth=2,
                  label=f'1/n = {1/n:.4f}')
        
        ax.set_xlabel('κ = max(X) / sum(X)')
        ax.set_ylabel('Densidad')
        ax.set_title(f'{name}\n(n = {n})', fontsize=11)
        ax.legend(fontsize=9)
        
        # Anotación interpretativa
        if mean_kappa > 0.1:
            ax.annotate('¡Concentración alta!\nUna obs. domina', 
                       xy=(0.95, 0.7), xycoords='axes fraction',
                       ha='right', fontsize=9,
                       bbox=dict(facecolor='lightyellow', alpha=0.8))
    
    plt.suptitle('Criterio κ de Taleb: ¿Cuánto contribuye el máximo al total?\n'
                'κ grande = distribución concentrada (fat-tailed)', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'kappa_taleb.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: kappa_taleb.png")


def plot_extremos_importan():
    """
    ESTILO TALEB: Muestra que en fat tails los extremos dominan.
    Curva de Lorenz de contribución.
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    n = 1000
    
    scenarios = [
        ('Normal |X|', np.abs(np.random.normal(0, 1, n)), COLORS['normal']),
        ('Pareto (α=2.5)', stats.pareto.rvs(2.5, size=n), COLORS['pareto']),
        ('Pareto (α=1.5)', stats.pareto.rvs(1.5, size=n), COLORS['cauchy']),
    ]
    
    for ax, (name, data, color) in zip(axes, scenarios):
        sorted_data = np.sort(data)[::-1]  # Ordenar de mayor a menor
        cumsum = np.cumsum(sorted_data) / sorted_data.sum()
        percentiles = np.arange(1, n+1) / n * 100
        
        ax.plot(percentiles, cumsum * 100, color=color, linewidth=2, label='Empírico')
        ax.fill_between(percentiles, 0, cumsum * 100, alpha=0.3, color=color)
        
        # Línea de igualdad perfecta
        ax.plot([0, 100], [0, 100], 'k--', alpha=0.5, label='Contribución uniforme')
        
        ax.set_xlabel('% de observaciones (de mayor a menor)')
        ax.set_ylabel('% del total acumulado')
        ax.set_title(name, fontsize=12)
        ax.legend(fontsize=9)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Anotaciones de concentración
        for pct in [1, 10, 20]:
            idx = int(n * pct / 100)
            contribution = cumsum[idx] * 100
            if contribution > pct + 5:  # Solo anotar si hay concentración significativa
                ax.annotate(f'Top {pct}% →\n{contribution:.0f}% del total',
                           xy=(pct, contribution),
                           xytext=(pct + 15, contribution - 10),
                           fontsize=9,
                           arrowprops=dict(arrowstyle='->', color='black', lw=0.5))
                break  # Solo una anotación por gráfica
    
    plt.suptitle('Concentración: ¿Qué porcentaje del total aportan los más grandes?\n'
                '(Estilo Pareto: "El 20% tiene el 80%")', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'extremos_importan.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: extremos_importan.png")


def plot_una_observacion_cambia_todo():
    """
    ESTILO TALEB: Una sola observación puede cambiar drásticamente el promedio
    en distribuciones fat-tailed.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    n = 100
    n_simulations = 1000
    
    # Normal: añadir una observación más no cambia mucho
    ax = axes[0]
    changes_normal = []
    for _ in range(n_simulations):
        data = np.random.normal(0, 1, n)
        mean_before = data.mean()
        new_obs = np.random.normal(0, 1, 1)[0]
        mean_after = np.append(data, new_obs).mean()
        changes_normal.append(abs(mean_after - mean_before) / abs(mean_before + 1e-10))
    
    ax.hist(changes_normal, bins=50, density=True, alpha=0.7, 
           color=COLORS['normal'], edgecolor='white')
    ax.set_xlabel('|Cambio relativo en X̄|')
    ax.set_ylabel('Densidad')
    ax.set_title(f'Normal: Añadir 1 obs. a n={n}\nCambio típico: {np.median(changes_normal):.1%}', 
                fontsize=11)
    ax.set_xlim(0, 0.5)
    
    # Pareto: añadir una observación puede cambiar mucho
    ax = axes[1]
    changes_pareto = []
    alpha = 1.5
    for _ in range(n_simulations):
        data = stats.pareto.rvs(alpha, size=n)
        mean_before = data.mean()
        new_obs = stats.pareto.rvs(alpha, size=1)[0]
        mean_after = np.append(data, new_obs).mean()
        changes_pareto.append(abs(mean_after - mean_before) / abs(mean_before))
    
    # Limitar para visualización
    changes_plot = [c for c in changes_pareto if c < 5]
    ax.hist(changes_plot, bins=50, density=True, alpha=0.7, 
           color=COLORS['pareto'], edgecolor='white')
    ax.set_xlabel('|Cambio relativo en X̄|')
    ax.set_ylabel('Densidad')
    ax.set_title(f'Pareto (α={alpha}): Añadir 1 obs. a n={n}\n'
                f'Cambio típico: {np.median(changes_pareto):.1%}, '
                f'pero puede ser {np.max(changes_pareto):.0%}!', fontsize=11)
    
    # Anotación
    ax.annotate(f'{sum(1 for c in changes_pareto if c > 1)}/{n_simulations}\n'
               f'casos con\ncambio >100%',
               xy=(0.95, 0.95), xycoords='axes fraction',
               ha='right', va='top', fontsize=10,
               bbox=dict(facecolor='lightyellow', alpha=0.9))
    
    plt.suptitle('Fragilidad del Promedio: ¿Cuánto cambia X̄ₙ al añadir UNA observación?', 
                fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'una_observacion_cambia_todo.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: una_observacion_cambia_todo.png")


def plot_fattail_diagnostics():
    """
    Diagnósticos visuales para detectar fat tails.
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    n = 5000
    
    # Generar datos
    normal_data = np.random.normal(0, 1, n)
    pareto_data = stats.pareto.rvs(2.5, size=n)
    cauchy_data = stats.cauchy.rvs(size=n)
    
    datasets = [
        ('Normal', normal_data, COLORS['normal']),
        ('Pareto (α=2.5)', pareto_data, COLORS['pareto']),
        ('Cauchy', cauchy_data, COLORS['cauchy']),
    ]
    
    # Fila 1: QQ-plots contra Normal
    for col, (name, data, color) in enumerate(datasets):
        ax = axes[0, col]
        stats.probplot(data, dist="norm", plot=ax)
        ax.get_lines()[0].set_color(color)
        ax.get_lines()[0].set_markersize(2)
        ax.get_lines()[1].set_color('gray')
        ax.set_title(f'QQ-plot: {name}')
        
        if col > 0:
            ax.annotate('Desviación en colas\n= fat tails',
                       xy=(0.05, 0.95), xycoords='axes fraction',
                       va='top', fontsize=9,
                       bbox=dict(facecolor='lightyellow', alpha=0.8))
    
    # Fila 2: Log-log plot de cola (CCDF)
    for col, (name, data, color) in enumerate(datasets):
        ax = axes[1, col]
        
        # Calcular CCDF empírica (solo valores positivos)
        pos_data = np.abs(data)
        sorted_data = np.sort(pos_data)[::-1]
        ccdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        
        ax.loglog(sorted_data, ccdf, 'o', markersize=2, alpha=0.5, color=color)
        
        # Ajustar línea de potencia si es Pareto
        if 'Pareto' in name or 'Cauchy' in name:
            # Ajuste lineal en log-log para los datos de cola
            tail_start = int(len(sorted_data) * 0.1)
            x_tail = np.log10(sorted_data[:tail_start])
            y_tail = np.log10(ccdf[:tail_start])
            slope, intercept = np.polyfit(x_tail, y_tail, 1)
            x_fit = np.logspace(np.log10(sorted_data[0]), np.log10(sorted_data[tail_start]), 50)
            y_fit = 10**(slope * np.log10(x_fit) + intercept)
            ax.loglog(x_fit, y_fit, '--', color='black', linewidth=2, 
                     label=f'Pendiente ≈ {slope:.2f}')
            ax.legend(fontsize=9)
        
        ax.set_xlabel('|X|')
        ax.set_ylabel('P(|X| > x)')
        ax.set_title(f'Cola log-log: {name}')
    
    plt.suptitle('Diagnósticos de Fat Tails\n'
                'QQ-plot: desviación en extremos = colas pesadas\n'
                'Log-log: línea recta = ley de potencias', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'fattail_diagnostics.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: fattail_diagnostics.png")


# =============================================================================
# 5. MÁXIMA VEROSIMILITUD
# =============================================================================

def plot_likelihood_example():
    """
    Visualiza la función de verosimilitud para un ejemplo simple.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Ejemplo 1: Bernoulli
    ax = axes[0]
    n, k = 10, 7
    p_values = np.linspace(0.01, 0.99, 200)
    likelihood = p_values**k * (1-p_values)**(n-k)
    
    ax.plot(p_values, likelihood / likelihood.max(), 'b-', linewidth=2, label='L(p)')
    ax.axvline(x=k/n, color=COLORS['true_mean'], linestyle='--', linewidth=2, 
              label=f'MLE = k/n = {k/n:.1f}')
    ax.fill_between(p_values, 0, likelihood / likelihood.max(), alpha=0.3)
    ax.set_xlabel('p')
    ax.set_ylabel('L(p) / max(L)')
    ax.set_title(f'Bernoulli: {k} éxitos en {n} intentos\nMLE = proporción muestral')
    ax.legend()
    
    # Ejemplo 2: Normal (estimando μ)
    ax = axes[1]
    true_mu = 5
    np.random.seed(123)
    data = np.random.normal(true_mu, 1, 20)
    
    mu_values = np.linspace(3, 7, 200)
    log_likelihoods = np.array([-0.5 * np.sum((data - mu)**2) for mu in mu_values])
    likelihoods = np.exp(log_likelihoods - log_likelihoods.max())
    
    ax.plot(mu_values, likelihoods, 'b-', linewidth=2, label='L(μ)')
    ax.axvline(x=data.mean(), color=COLORS['true_mean'], linestyle='--', linewidth=2, 
               label=f'MLE = X̄ = {data.mean():.2f}')
    ax.axvline(x=true_mu, color=COLORS['pareto'], linestyle=':', linewidth=2,
               label=f'μ verdadera = {true_mu}')
    ax.fill_between(mu_values, 0, likelihoods, alpha=0.3)
    ax.set_xlabel('μ')
    ax.set_ylabel('L(μ) / max(L)')
    ax.set_title('Normal: estimando la media\nMLE = promedio muestral')
    ax.legend()
    
    plt.suptitle('Función de Verosimilitud y MLE', fontsize=14)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'likelihood_example.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: likelihood_example.png")


# =============================================================================
# 6. RESUMEN FINAL
# =============================================================================

def plot_resumen_mediocristran_extremistan():
    """
    ESTILO TALEB: Mediocristán vs Extremistán
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    n = 1000
    
    # Mediocristán: Normal (alturas)
    ax = axes[0, 0]
    heights = np.random.normal(170, 10, n)  # cm
    ax.hist(heights, bins=40, density=True, alpha=0.7, color=COLORS['normal'], edgecolor='white')
    ax.axvline(x=heights.mean(), color=COLORS['true_mean'], linewidth=2, linestyle='--')
    ax.set_xlabel('Altura (cm)')
    ax.set_ylabel('Densidad')
    ax.set_title('MEDIOCRISTÁN: Alturas humanas\nμ ≈ mediana, no hay outliers extremos')
    ax.annotate(f'Media = {heights.mean():.1f}\nMediana = {np.median(heights):.1f}\nMax = {heights.max():.1f}',
               xy=(0.95, 0.95), xycoords='axes fraction', ha='right', va='top',
               bbox=dict(facecolor='lightgreen', alpha=0.8))
    
    # Extremistán: Pareto (riqueza)
    ax = axes[0, 1]
    wealth = stats.pareto.rvs(1.5, size=n) * 50000  # $ (escala)
    wealth_plot = wealth[wealth < np.percentile(wealth, 95)]  # Limitar para ver
    ax.hist(wealth_plot, bins=40, density=True, alpha=0.7, color=COLORS['pareto'], edgecolor='white')
    ax.axvline(x=wealth.mean(), color=COLORS['true_mean'], linewidth=2, linestyle='--', label='Media')
    ax.axvline(x=np.median(wealth), color='purple', linewidth=2, linestyle=':', label='Mediana')
    ax.set_xlabel('Riqueza ($)')
    ax.set_ylabel('Densidad')
    ax.set_title('EXTREMISTÁN: Distribución de riqueza\nμ >> mediana, outliers dominan')
    ax.legend()
    ax.annotate(f'Media = ${wealth.mean():,.0f}\nMediana = ${np.median(wealth):,.0f}\n'
               f'Max = ${wealth.max():,.0f}',
               xy=(0.95, 0.95), xycoords='axes fraction', ha='right', va='top',
               bbox=dict(facecolor='lightyellow', alpha=0.8))
    
    # Convergencia del promedio: Mediocristán
    ax = axes[1, 0]
    n_max = 5000
    ns = np.arange(1, n_max + 1)
    for _ in range(20):
        data = np.random.normal(170, 10, n_max)
        running_mean = np.cumsum(data) / ns
        ax.plot(ns, running_mean, alpha=0.3, color=COLORS['normal'])
    ax.axhline(y=170, color=COLORS['true_mean'], linewidth=2, linestyle='--')
    ax.axhspan(169, 171, alpha=0.2, color=COLORS['true_mean'])
    ax.set_xlabel('n')
    ax.set_ylabel('Promedio acumulado')
    ax.set_title('Mediocristán: El promedio CONVERGE')
    ax.set_xscale('log')
    ax.set_ylim(165, 175)
    
    # Convergencia del promedio: Extremistán
    ax = axes[1, 1]
    for _ in range(20):
        data = stats.pareto.rvs(1.5, size=n_max) * 50000
        running_mean = np.cumsum(data) / ns
        ax.plot(ns, running_mean, alpha=0.3, color=COLORS['pareto'])
    true_mean_pareto = 1.5 / 0.5 * 50000  # = 150000
    ax.axhline(y=true_mean_pareto, color=COLORS['true_mean'], linewidth=2, linestyle='--')
    ax.set_xlabel('n')
    ax.set_ylabel('Promedio acumulado')
    ax.set_title('Extremistán: El promedio es INESTABLE')
    ax.set_xscale('log')
    
    plt.suptitle('Mediocristán vs Extremistán (Taleb)\n'
                '¿Puedes confiar en el promedio?', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'mediocristán_extremistan.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Generada: mediocristán_extremistan.png")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Genera todas las visualizaciones del laboratorio.
    """
    print("="*60)
    print("LABORATORIO DE PROBABILIDAD")
    print("Generando visualizaciones estilo Taleb...")
    print("="*60)
    print()
    
    print("[1/12] Distribuciones de probabilidad...")
    plot_distribuciones_comparacion()
    
    print("[2/12] LGN: Convergencia...")
    plot_lgn_convergencia()
    
    print("[3/12] TLC: Demostración...")
    plot_tlc_demo()
    
    print("[4/12] TLC vs Fat tails...")
    plot_tlc_vs_fattail()
    
    print("[5/12] Convergencia en fat tails...")
    plot_convergencia_fattail()
    
    print("[6/12] Cauchy: No convergencia...")
    plot_cauchy_no_convergencia()
    
    print("[7/12] Kappa de Taleb...")
    plot_kappa_taleb()
    
    print("[8/12] Extremos importan (Lorenz)...")
    plot_extremos_importan()
    
    print("[9/12] Una observación cambia todo...")
    plot_una_observacion_cambia_todo()
    
    print("[10/12] Diagnósticos de fat tails...")
    plot_fattail_diagnostics()
    
    print("[11/12] Likelihood example...")
    plot_likelihood_example()
    
    print("[12/12] Mediocristán vs Extremistán...")
    plot_resumen_mediocristran_extremistan()
    
    print()
    print("="*60)
    print(f"✓ Todas las imágenes generadas en: {IMAGES_DIR}/")
    print("="*60)
    print()
    print("Imágenes generadas:")
    for img in sorted(IMAGES_DIR.glob("*.png")):
        print(f"  - {img.name}")


if __name__ == "__main__":
    main()
