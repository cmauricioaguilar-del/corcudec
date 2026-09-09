import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import base64
from io import BytesIO

PALETTE_ORQ = '#1C3557'
PALETTE_ADMIN = '#2E7D52'
PALETTE_DIR = '#8B1A1A'
PALETTE_ACC = '#B8892A'

DEPT_COLORS = {
    'Orquesta': PALETTE_ORQ,
    'Administración': PALETTE_ADMIN,
    'Dirección Musical': PALETTE_DIR,
}

NIVEL_ORDER = ['Director', 'Concertino', 'Asistente Concertino', 'Jefatura',
               'Jefe de Fila', 'Asistente de Fila', 'Tutti', 'Administrativo']


def _fmt_clp(x, pos=None):
    return f'${x/1_000_000:.1f}M' if x >= 1_000_000 else f'${x/1000:.0f}K'


def _save_fig(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=130)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_b64


def grafica_distribucion_salarios(df):
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.hist(df['sueldo_base'] / 1_000_000, bins=18, color=PALETTE_ORQ, alpha=0.82, edgecolor='white')
    mediana = df['sueldo_base'].median() / 1_000_000
    media = df['sueldo_base'].mean() / 1_000_000
    ax.axvline(mediana, color=PALETTE_ACC, linewidth=2, linestyle='--', label=f'Mediana ${mediana:.2f}M')
    ax.axvline(media, color=PALETTE_DIR, linewidth=2, linestyle=':', label=f'Promedio ${media:.2f}M')
    ax.set_xlabel('Sueldo Base (millones CLP)', fontsize=11)
    ax.set_ylabel('N° Trabajadores', fontsize=11)
    ax.set_title('Distribución de Sueldos Base — Julio 2026', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.spines[['top', 'right']].set_visible(False)
    return _save_fig(fig)


def grafica_salario_por_departamento(df):
    grp = df.groupby('departamento')['sueldo_base'].mean().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 3.5))
    colors = [DEPT_COLORS.get(d, PALETTE_ORQ) for d in grp.index]
    bars = ax.barh(grp.index, grp.values / 1_000_000, color=colors, height=0.5)
    for bar, val in zip(bars, grp.values):
        ax.text(val / 1_000_000 + 0.05, bar.get_y() + bar.get_height() / 2,
                f'${val/1_000_000:.2f}M', va='center', fontsize=10, fontweight='bold')
    ax.set_xlabel('Sueldo Base Promedio (millones CLP)', fontsize=10)
    ax.set_title('Sueldo Base Promedio por Área', fontsize=12, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_xlim(0, grp.max() / 1_000_000 * 1.35)
    return _save_fig(fig)


def grafica_salario_por_nivel(df):
    orden_valido = [n for n in NIVEL_ORDER if n in df['nivel'].unique()]
    medias = df.groupby('nivel')['sueldo_base'].mean()
    medias = medias.reindex(orden_valido)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    colors = [PALETTE_DIR if n == 'Director' else PALETTE_ACC if n in ('Concertino', 'Asistente Concertino')
              else PALETTE_ORQ if n in ('Jefe de Fila', 'Asistente de Fila', 'Tutti')
              else PALETTE_ADMIN for n in medias.index]
    bars = ax.bar(range(len(medias)), medias.values / 1_000_000, color=colors, width=0.65)
    for bar, val in zip(bars, medias.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f'${val/1_000_000:.2f}M', ha='center', fontsize=8.5, fontweight='bold')
    ax.set_xticks(range(len(medias)))
    ax.set_xticklabels(medias.index, rotation=30, ha='right', fontsize=9)
    ax.set_ylabel('Sueldo Base Promedio (millones CLP)', fontsize=10)
    ax.set_title('Escalafón Salarial por Nivel', fontsize=12, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    return _save_fig(fig)


def grafica_equidad_genero(df):
    genero_data = df.groupby('sexo')['sueldo_base'].mean()
    etiquetas = {'M': 'Hombres', 'F': 'Mujeres'}
    labels = [etiquetas.get(k, k) for k in genero_data.index]
    colors = [PALETTE_ORQ, '#C0392B']
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].bar(labels, genero_data.values / 1_000_000, color=colors, width=0.45)
    for i, (lbl, val) in enumerate(zip(labels, genero_data.values)):
        axes[0].text(i, val / 1_000_000 + 0.03, f'${val/1_000_000:.2f}M',
                     ha='center', fontweight='bold', fontsize=11)
    axes[0].set_ylabel('Sueldo Base Promedio (M CLP)', fontsize=10)
    axes[0].set_title('Promedio por Género', fontsize=11, fontweight='bold')
    axes[0].spines[['top', 'right']].set_visible(False)
    conteo = df['sexo'].value_counts()
    c_labels = [etiquetas.get(k, k) for k in conteo.index]
    axes[1].pie(conteo.values, labels=c_labels, colors=colors, autopct='%1.0f%%',
                startangle=90, textprops={'fontsize': 11})
    axes[1].set_title('Distribución por Género', fontsize=11, fontweight='bold')
    fig.tight_layout()
    return _save_fig(fig)


def grafica_bandas_salariales(df):
    orden_valido = [n for n in NIVEL_ORDER if n in df['nivel'].unique()]
    bandas = df.groupby('nivel')['sueldo_base'].quantile([0.25, 0.50, 0.75]).unstack()
    bandas = bandas.reindex(orden_valido)
    fig, ax = plt.subplots(figsize=(11, 5))
    x = range(len(bandas))
    ax.bar(x, (bandas[0.75] - bandas[0.25]) / 1_000_000,
           bottom=bandas[0.25] / 1_000_000, color=PALETTE_ORQ, alpha=0.35, width=0.55, label='P25–P75')
    ax.scatter(x, bandas[0.50] / 1_000_000, color=PALETTE_ACC, zorder=5, s=80, label='Mediana')
    ax.plot(x, bandas[0.50] / 1_000_000, color=PALETTE_ACC, linewidth=1.5, alpha=0.6)
    ax.set_xticks(list(x))
    ax.set_xticklabels(bandas.index, rotation=30, ha='right', fontsize=9)
    ax.set_ylabel('Sueldo Base (millones CLP)', fontsize=10)
    ax.set_title('Bandas Salariales por Nivel de Cargo', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.spines[['top', 'right']].set_visible(False)
    return _save_fig(fig)


def grafica_componentes_haberes(df):
    componentes = {
        'Sueldo Base': df['sueldo_base'].sum(),
        'Quinquenios': df['quinquenios_total'].sum(),
        'Asig. Responsabilidad': df['asig_responsabilidad'].sum(),
        'Asig. Especial': df['asig_especial'].sum(),
        'Asig. Jerarquía': df['asig_jerarquia'].sum(),
        'Desgaste Inst.': df['desgaste_instrumentos'].sum(),
        'Bono Invierno': df['bono_invierno'].sum(),
        'Otros': df['asig_movilizacion'].sum() + df['asig_jjtt'].sum() + df['horas_extras'].sum(),
    }
    componentes = {k: v for k, v in componentes.items() if v > 0}
    total = sum(componentes.values())
    labels = list(componentes.keys())
    sizes = [v / total * 100 for v in componentes.values()]
    palette = [PALETTE_ORQ, PALETTE_ACC, PALETTE_DIR, PALETTE_ADMIN,
               '#5B7DB1', '#D4A853', '#6B8E6B', '#999999']
    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, colors=palette[:len(labels)],
        autopct=lambda p: f'{p:.1f}%' if p > 3 else '',
        startangle=140, pctdistance=0.75,
    )
    ax.legend(wedges, [f'{l} (${componentes[l]/1_000_000:.1f}M)' for l in labels],
              loc='lower right', fontsize=8.5, framealpha=0.9)
    ax.set_title('Composición de la Masa Salarial\nTotal Haberes — Julio 2026', fontsize=12, fontweight='bold')
    return _save_fig(fig)
