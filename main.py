import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(__file__))

def _sha256(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

from src.analisis import (
    cargar_datos, estadisticas_generales, analisis_por_departamento,
    analisis_por_nivel, analisis_equidad_genero, bandas_salariales,
    analisis_quinquenios, top_salarios, distribucion_componentes,
)
from src.visualizaciones import (
    grafica_distribucion_salarios, grafica_salario_por_departamento,
    grafica_salario_por_nivel, grafica_equidad_genero,
    grafica_bandas_salariales, grafica_componentes_haberes,
)
from src.reporte import generar_reporte

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'dotacion_julio2026.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
OUTPUT_HTML = os.path.join(OUTPUT_DIR, 'reporte_salarial_corcudec.html')


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Cargando datos CORCUDEC...")
    df = cargar_datos(DATA_PATH)
    print(f"  → {len(df)} trabajadores activos (Julio 2026)")

    print("Calculando estadísticas...")
    stats = estadisticas_generales(df)
    genero = analisis_equidad_genero(df)
    nivel_df = analisis_por_nivel(df)
    dept_df = analisis_por_departamento(df)
    top_df = top_salarios(df, n=10)

    print("Generando gráficas...")
    graficas = {
        'distribucion': grafica_distribucion_salarios(df),
        'por_departamento': grafica_salario_por_departamento(df),
        'por_nivel': grafica_salario_por_nivel(df),
        'genero': grafica_equidad_genero(df),
        'bandas': grafica_bandas_salariales(df),
        'componentes': grafica_componentes_haberes(df),
    }

    print("Generando reporte HTML...")
    ruta = generar_reporte(
        stats, genero, nivel_df, dept_df, top_df, graficas, OUTPUT_HTML,
        df=df,
        auth_user_hash=_sha256('admin'),
        auth_pass_hash=_sha256('Corcudec2026'),
    )
    print(f"\n✓ Reporte generado: {ruta}")

    print("\n=== RESUMEN ===")
    print(f"  Trabajadores:        {stats['total_empleados']}")
    print(f"  SB promedio:         ${stats['sueldo_base_promedio']:,.0f}")
    print(f"  SB mediana:          ${stats['sueldo_base_mediana']:,.0f}")
    print(f"  Haberes promedio:    ${stats['haberes_promedio']:,.0f}")
    print(f"  Masa salarial SB:    ${stats['masa_salarial_sb']:,.0f}")
    print(f"  Masa haberes:        ${stats['masa_salarial_haberes']:,.0f}")
    print(f"  Brecha género:       {genero['brecha_porcentual']:.1f}%")


if __name__ == '__main__':
    main()
