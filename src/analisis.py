import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime


def cargar_datos(ruta):
    df = pd.read_csv(ruta)
    df['sexo'] = df['sexo'].str.strip().str.upper()
    df['quinquenios_total'] = df['quinquenio_5'] + df['quinquenio_10'] + df['quinquenio_15']
    df['quinquenios_anos'] = (
        (df['quinquenio_5'] > 0).astype(int) * 5 +
        (df['quinquenio_10'] > 0).astype(int) * 5 +
        (df['quinquenio_15'] > 0).astype(int) * 5
    )
    df['mes_referencia'] = 'Julio 2026'
    return df


def estadisticas_generales(df):
    sb = df['sueldo_base']
    hab = df['total_haberes']
    liq = df['liquido']
    return {
        'total_empleados': len(df),
        'sueldo_base_promedio': sb.mean(),
        'sueldo_base_mediana': sb.median(),
        'sueldo_base_min': sb.min(),
        'sueldo_base_max': sb.max(),
        'sueldo_base_std': sb.std(),
        'haberes_promedio': hab.mean(),
        'haberes_mediana': hab.median(),
        'liquido_promedio': liq.mean(),
        'p25': sb.quantile(0.25),
        'p75': sb.quantile(0.75),
        'masa_salarial_sb': sb.sum(),
        'masa_salarial_haberes': hab.sum(),
    }


def analisis_por_departamento(df):
    return (
        df.groupby('departamento')
        .agg(
            empleados=('sueldo_base', 'count'),
            sb_promedio=('sueldo_base', 'mean'),
            sb_mediana=('sueldo_base', 'median'),
            sb_min=('sueldo_base', 'min'),
            sb_max=('sueldo_base', 'max'),
            haberes_promedio=('total_haberes', 'mean'),
            masa_sb=('sueldo_base', 'sum'),
        )
        .reset_index()
        .sort_values('sb_promedio', ascending=False)
    )


def analisis_por_nivel(df):
    orden = ['Director', 'Concertino', 'Asistente Concertino', 'Jefatura',
             'Jefe de Fila', 'Asistente de Fila', 'Tutti', 'Administrativo']
    result = (
        df.groupby('nivel')
        .agg(
            empleados=('sueldo_base', 'count'),
            sb_promedio=('sueldo_base', 'mean'),
            sb_mediana=('sueldo_base', 'median'),
            sb_min=('sueldo_base', 'min'),
            sb_max=('sueldo_base', 'max'),
            haberes_promedio=('total_haberes', 'mean'),
        )
        .reset_index()
    )
    result['orden'] = result['nivel'].apply(
        lambda x: orden.index(x) if x in orden else len(orden)
    )
    return result.sort_values('orden').drop(columns='orden')


def analisis_equidad_genero(df):
    m = df[df['sexo'] == 'M']['sueldo_base']
    f = df[df['sexo'] == 'F']['sueldo_base']
    stat, pvalue = stats.mannwhitneyu(m, f, alternative='two-sided')
    brecha_pct = ((m.mean() - f.mean()) / f.mean()) * 100
    return {
        'hombres': len(m),
        'mujeres': len(f),
        'sb_promedio_hombres': m.mean(),
        'sb_promedio_mujeres': f.mean(),
        'brecha_porcentual': brecha_pct,
        'p_value': pvalue,
        'diferencia_significativa': pvalue < 0.05,
    }


def bandas_salariales(df):
    return (
        df.groupby('nivel')['sueldo_base']
        .quantile([0.25, 0.50, 0.75])
        .unstack()
        .rename(columns={0.25: 'p25', 0.50: 'mediana', 0.75: 'p75'})
        .reset_index()
    )


def analisis_quinquenios(df):
    con_q = df[df['quinquenios_total'] > 0]
    return {
        'con_quinquenio': len(con_q),
        'sin_quinquenio': len(df) - len(con_q),
        'quinquenio_promedio': con_q['quinquenios_total'].mean() if len(con_q) > 0 else 0,
        'anos_servicio_promedio': con_q['quinquenios_anos'].mean() if len(con_q) > 0 else 0,
        'por_departamento': df.groupby('departamento').agg(
            con_q=('quinquenios_total', lambda x: (x > 0).sum()),
            q_promedio=('quinquenios_total', 'mean'),
        ).reset_index(),
    }


def top_salarios(df, n=10):
    return (
        df.nlargest(n, 'total_haberes')
        [['id', 'cargo', 'departamento', 'nivel', 'sexo', 'sueldo_base', 'total_haberes', 'liquido']]
        .reset_index(drop=True)
    )


def distribucion_componentes(df):
    total = df['total_haberes'].sum()
    return {
        'sueldo_base': df['sueldo_base'].sum(),
        'quinquenios': df['quinquenios_total'].sum(),
        'asig_responsabilidad': df['asig_responsabilidad'].sum(),
        'asig_especial': df['asig_especial'].sum(),
        'asig_jerarquia': df['asig_jerarquia'].sum(),
        'horas_extras': df['horas_extras'].sum(),
        'bono_invierno': df['bono_invierno'].sum(),
        'desgaste_instrumentos': df['desgaste_instrumentos'].sum(),
        'asig_movilizacion': df['asig_movilizacion'].sum(),
        'total_haberes': total,
    }
