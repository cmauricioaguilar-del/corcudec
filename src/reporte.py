from jinja2 import Template
from datetime import datetime

TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Análisis Salarial CORCUDEC — Julio 2026</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');
  :root {
    --navy: #1C3557; --gold: #B8892A; --cream: #F7F4EF;
    --text: #1a1a2e; --muted: #6b7280; --white: #ffffff;
    --green: #2E7D52; --red: #8B1A1A;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Source Sans 3', sans-serif; background: var(--cream); color: var(--text); line-height: 1.6; }
  header { background: var(--navy); color: var(--white); padding: 2.5rem 2rem 2rem; text-align: center; }
  header h1 { font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; font-weight: 600; letter-spacing: 0.02em; }
  header p { color: rgba(255,255,255,0.75); margin-top: 0.4rem; font-size: 1rem; }
  header .badge { display: inline-block; background: var(--gold); color: var(--white); font-size: 0.78rem; font-weight: 600; padding: 0.2rem 0.8rem; border-radius: 2rem; margin-top: 0.8rem; letter-spacing: 0.06em; }
  main { max-width: 1100px; margin: 0 auto; padding: 2rem 1.5rem 3rem; }
  section { margin-bottom: 2.5rem; }
  h2 { font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; color: var(--navy); border-bottom: 2px solid var(--gold); padding-bottom: 0.4rem; margin-bottom: 1.2rem; }
  .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; }
  .kpi { background: var(--white); border-left: 4px solid var(--navy); padding: 1rem 1.2rem; border-radius: 0 6px 6px 0; }
  .kpi.gold { border-left-color: var(--gold); }
  .kpi.green { border-left-color: var(--green); }
  .kpi label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); display: block; }
  .kpi .value { font-family: 'Cormorant Garamond', serif; font-size: 1.7rem; font-weight: 600; color: var(--navy); font-variant-numeric: tabular-nums; }
  .kpi .sub { font-size: 0.8rem; color: var(--muted); margin-top: 0.1rem; }
  .chart-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
  .chart-row.single { grid-template-columns: 1fr; }
  .chart-box { background: var(--white); border-radius: 8px; padding: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
  .chart-box img { width: 100%; height: auto; display: block; }
  table { width: 100%; border-collapse: collapse; font-size: 0.88rem; background: var(--white); border-radius: 8px; overflow: hidden; }
  thead tr { background: var(--navy); color: var(--white); }
  th { padding: 0.65rem 0.9rem; text-align: left; font-weight: 600; font-size: 0.8rem; letter-spacing: 0.04em; }
  td { padding: 0.55rem 0.9rem; border-bottom: 1px solid #f0ede8; }
  tr:last-child td { border-bottom: none; }
  tr:nth-child(even) { background: #fbf9f6; }
  .num { text-align: right; font-variant-numeric: tabular-nums; }
  .tag { display: inline-block; font-size: 0.72rem; padding: 0.15rem 0.5rem; border-radius: 1rem; font-weight: 600; }
  .tag-orch { background: #e8eef5; color: var(--navy); }
  .tag-admin { background: #e8f5ee; color: var(--green); }
  .tag-dir { background: #f5e8e8; color: var(--red); }
  .info-box { background: #fff8e8; border-left: 4px solid var(--gold); padding: 0.9rem 1.2rem; border-radius: 0 6px 6px 0; font-size: 0.9rem; }
  footer { text-align: center; padding: 1.5rem; font-size: 0.8rem; color: var(--muted); border-top: 1px solid #e5e1d8; margin-top: 1rem; }
  @media (max-width: 700px) { .chart-row { grid-template-columns: 1fr; } .kpi-grid { grid-template-columns: 1fr 1fr; } }
</style>
</head>
<body>
<header>
  <h1>Corporación Cultural Universidad de Concepción</h1>
  <p>Análisis de Dotación y Bandas Salariales · Orquesta Sinfónica Universidad de Concepción</p>
  <span class="badge">JULIO 2026 · {{ stats.total_empleados }} TRABAJADORES</span>
</header>
<main>
<section>
  <h2>Indicadores Generales</h2>
  <div class="kpi-grid">
    <div class="kpi"><label>Trabajadores activos</label><div class="value">{{ stats.total_empleados }}</div><div class="sub">Dotación julio 2026</div></div>
    <div class="kpi gold"><label>Sueldo base promedio</label><div class="value">{{ format_clp(stats.sueldo_base_promedio) }}</div><div class="sub">Mediana: {{ format_clp(stats.sueldo_base_mediana) }}</div></div>
    <div class="kpi gold"><label>Haberes promedio</label><div class="value">{{ format_clp(stats.haberes_promedio) }}</div><div class="sub">Incl. asignaciones e imponibles</div></div>
    <div class="kpi green"><label>Masa salarial SB</label><div class="value">{{ format_mclp(stats.masa_salarial_sb) }}</div><div class="sub">Sueldo base total mensual</div></div>
    <div class="kpi green"><label>Masa salarial haberes</label><div class="value">{{ format_mclp(stats.masa_salarial_haberes) }}</div><div class="sub">Total haberes mensual</div></div>
    <div class="kpi"><label>Dispersión salarial</label><div class="value">{{ format_clp(stats.sueldo_base_min) }}–{{ format_clp(stats.sueldo_base_max) }}</div><div class="sub">Mín.–Máx. sueldo base</div></div>
    <div class="kpi"><label>P25 – P75</label><div class="value">{{ format_clp(stats.p25) }}</div><div class="sub">P75: {{ format_clp(stats.p75) }}</div></div>
    <div class="kpi"><label>Mujeres / Hombres</label><div class="value">{{ genero.mujeres }} / {{ genero.hombres }}</div><div class="sub">{{ "%.0f"|format(genero.mujeres / stats.total_empleados * 100) }}% / {{ "%.0f"|format(genero.hombres / stats.total_empleados * 100) }}%</div></div>
  </div>
</section>
<section>
  <h2>Distribución Salarial</h2>
  <div class="chart-row">
    <div class="chart-box"><img src="data:image/png;base64,{{ graficas.distribucion }}" alt="Distribución salarios"></div>
    <div class="chart-box"><img src="data:image/png;base64,{{ graficas.por_departamento }}" alt="Por departamento"></div>
  </div>
</section>
<section>
  <h2>Escalafón por Nivel de Cargo</h2>
  <div class="chart-row single">
    <div class="chart-box"><img src="data:image/png;base64,{{ graficas.por_nivel }}" alt="Por nivel"></div>
  </div>
  <br>
  <table>
    <thead><tr><th>Nivel</th><th class="num">N°</th><th class="num">SB Promedio</th><th class="num">SB Mínimo</th><th class="num">SB Máximo</th><th class="num">Haberes Prom.</th></tr></thead>
    <tbody>
    {% for _, row in nivel_df.iterrows() %}
    <tr><td>{{ row.nivel }}</td><td class="num">{{ row.empleados }}</td><td class="num">{{ format_clp(row.sb_promedio) }}</td><td class="num">{{ format_clp(row.sb_min) }}</td><td class="num">{{ format_clp(row.sb_max) }}</td><td class="num">{{ format_clp(row.haberes_promedio) }}</td></tr>
    {% endfor %}
    </tbody>
  </table>
</section>
<section>
  <h2>Bandas Salariales</h2>
  <div class="chart-row">
    <div class="chart-box"><img src="data:image/png;base64,{{ graficas.bandas }}" alt="Bandas salariales"></div>
    <div class="chart-box"><img src="data:image/png;base64,{{ graficas.componentes }}" alt="Componentes haberes"></div>
  </div>
</section>
<section>
  <h2>Equidad de Género</h2>
  <div class="chart-row">
    <div class="chart-box"><img src="data:image/png;base64,{{ graficas.genero }}" alt="Equidad género"></div>
    <div style="display:flex;flex-direction:column;gap:1rem;justify-content:center;">
      <div class="kpi"><label>SB promedio hombres</label><div class="value">{{ format_clp(genero.sb_promedio_hombres) }}</div></div>
      <div class="kpi"><label>SB promedio mujeres</label><div class="value">{{ format_clp(genero.sb_promedio_mujeres) }}</div></div>
      <div class="kpi {% if genero.brecha_porcentual|abs < 5 %}green{% else %}gold{% endif %}"><label>Brecha salarial (H–M)</label><div class="value">{{ "%.1f"|format(genero.brecha_porcentual) }}%</div><div class="sub">{% if not genero.diferencia_significativa %}No significativa estadísticamente{% else %}Diferencia significativa (p={{ "%.3f"|format(genero.p_value) }}){% endif %}</div></div>
    </div>
  </div>
</section>
<section>
  <h2>Top 10 Remuneraciones (Total Haberes)</h2>
  <table>
    <thead><tr><th>#</th><th>Cargo</th><th>Área</th><th>Nivel</th><th class="num">Sueldo Base</th><th class="num">Total Haberes</th><th class="num">Líquido</th></tr></thead>
    <tbody>
    {% for _, row in top_df.iterrows() %}
    <tr><td>{{ loop.index }}</td><td>{{ row.cargo }}</td><td><span class="tag {% if row.departamento == 'Orquesta' %}tag-orch{% elif row.departamento == 'Administración' %}tag-admin{% else %}tag-dir{% endif %}">{{ row.departamento }}</span></td><td>{{ row.nivel }}</td><td class="num">{{ format_clp(row.sueldo_base) }}</td><td class="num">{{ format_clp(row.total_haberes) }}</td><td class="num">{{ format_clp(row.liquido) }}</td></tr>
    {% endfor %}
    </tbody>
  </table>
</section>
<section>
  <h2>Por Área</h2>
  <table>
    <thead><tr><th>Área</th><th class="num">N°</th><th class="num">SB Promedio</th><th class="num">SB Mediana</th><th class="num">Haberes Prom.</th><th class="num">Masa SB</th></tr></thead>
    <tbody>
    {% for _, row in dept_df.iterrows() %}
    <tr><td><span class="tag {% if row.departamento == 'Orquesta' %}tag-orch{% elif row.departamento == 'Administración' %}tag-admin{% else %}tag-dir{% endif %}">{{ row.departamento }}</span></td><td class="num">{{ row.empleados }}</td><td class="num">{{ format_clp(row.sb_promedio) }}</td><td class="num">{{ format_clp(row.sb_mediana) }}</td><td class="num">{{ format_clp(row.haberes_promedio) }}</td><td class="num">{{ format_mclp(row.masa_sb) }}</td></tr>
    {% endfor %}
    </tbody>
  </table>
</section>
<div class="info-box"><strong>Fuente:</strong> Imagen de Remuneraciones Julio 2026 · CORCUDEC.<br>Incluye 74 trabajadores activos (1 funcionario con licencia excluido). Datos en pesos chilenos (CLP) corrientes. Generado: {{ fecha_generacion }}.</div>
</main>
<footer>Corporación Cultural Universidad de Concepción &nbsp;|&nbsp; Análisis Salarial Interno &nbsp;|&nbsp; {{ fecha_generacion }}</footer>
</body>
</html>
"""


def generar_reporte(stats, genero, nivel_df, dept_df, top_df, graficas, ruta_salida):
    def format_clp(v):
        if v is None or (isinstance(v, float) and v != v):
            return '$0'
        return f'${int(v):,}'.replace(',', '.')

    def format_mclp(v):
        return f'${v/1_000_000:.1f}M'

    tpl = Template(TEMPLATE_HTML)
    html = tpl.render(
        stats=stats, genero=genero, nivel_df=nivel_df, dept_df=dept_df, top_df=top_df,
        graficas=graficas, format_clp=format_clp, format_mclp=format_mclp,
        fecha_generacion=__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M'),
    )
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    return ruta_salida
