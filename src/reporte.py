import json
from jinja2 import Template
from datetime import datetime

TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Análisis Salarial CORCUDEC — Julio 2026</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');
  :root {
    --navy: #1C3557; --gold: #B8892A; --cream: #F7F4EF;
    --text: #1a1a2e; --muted: #6b7280; --white: #ffffff;
    --green: #2E7D52; --red: #8B1A1A;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Source Sans 3', sans-serif; background: var(--cream); color: var(--text); line-height: 1.6; }
  header {
    background: var(--navy);
    border-top: 5px solid var(--gold);
    border-bottom: 5px solid var(--gold);
    display: flex;
    align-items: stretch;
    min-height: 155px;
  }
  .hdr-left {
    flex: 1;
    padding: 1.8rem 2rem 1.8rem 2.2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .hdr-left h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--white);
    line-height: 1.25;
    letter-spacing: 0.01em;
  }
  .hdr-divider {
    width: 1px;
    background: rgba(255,255,255,0.12);
    margin: 0;
  }
  .hdr-sub {
    color: rgba(255,255,255,0.55);
    font-size: 0.88rem;
    margin-top: 0.25rem;
  }
  .hdr-sub2 {
    color: rgba(255,255,255,0.55);
    font-size: 0.88rem;
    margin-top: 0.12rem;
  }
  .hdr-rule {
    width: 100%;
    max-width: 380px;
    height: 1px;
    background: var(--gold);
    opacity: 0.5;
    margin: 0.55rem 0;
  }
  .badge {
    display: inline-block;
    background: var(--gold);
    color: var(--white);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.22rem 0.9rem;
    border-radius: 2rem;
    letter-spacing: 0.06em;
    margin-top: 0.3rem;
    align-self: flex-start;
  }
  .hdr-right {
    width: 300px;
    flex-shrink: 0;
    padding: 1rem 1.3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
  }
  .lidera-card {
    background: #F7F4EF;
    border-radius: 10px;
    box-shadow: 2px 3px 14px rgba(0,0,0,0.22);
    width: 100%;
    padding: 1.1rem 1rem 0.9rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0;
  }
  .lidera-by {
    font-size: 0.65rem;
    color: rgba(0,0,0,0.28);
    font-style: italic;
    margin-bottom: 0.45rem;
    letter-spacing: 0.02em;
  }
  .lidera-wordmark {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: #4a4a4a;
    letter-spacing: 0.06em;
    line-height: 1;
    margin-top: 0.3rem;
  }
  .lidera-gold-rule {
    width: 110px;
    height: 1.5px;
    background: var(--gold);
    opacity: 0.65;
    margin: 0.55rem 0 0.4rem;
  }
  .lidera-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: #3a3a3a;
    letter-spacing: 0.01em;
  }
  .lidera-tagline {
    font-size: 0.62rem;
    color: #999;
    font-style: italic;
    margin-top: 0.18rem;
    text-align: center;
  }
  @media (max-width: 700px) {
    header { flex-direction: column; }
    .hdr-right { width: 100%; border-top: 1px solid rgba(255,255,255,0.12); }
    .hdr-divider { display: none; }
  }
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
  .chart-box canvas { width: 100% !important; }
  .chart-hint { font-size: 0.72rem; color: var(--muted); text-align: center; margin-top: 0.5rem; }
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
  tr.drillable { cursor: pointer; transition: background 0.15s; }
  tr.drillable:hover td { background: #eef3f8 !important; }
  tr.drillable td:first-child::after { content: ' ↗'; font-size: 0.68rem; color: var(--muted); }
  /* Login */
  #loginOverlay { position: fixed; inset: 0; background: var(--navy); z-index: 200; display: flex; align-items: center; justify-content: center; }
  #loginOverlay.hidden { display: none; }
  .login-box { background: var(--white); border-radius: 12px; padding: 2.5rem 2.8rem; width: 100%; max-width: 380px; box-shadow: 0 12px 50px rgba(0,0,0,0.35); text-align: center; }
  .login-box .logo { font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; font-weight: 600; color: var(--navy); margin-bottom: 0.2rem; }
  .login-box .sub { font-size: 0.82rem; color: var(--muted); margin-bottom: 1.8rem; }
  .login-box .gold-bar { width: 2.5rem; height: 3px; background: var(--gold); margin: 0.5rem auto 1.6rem; border-radius: 2px; }
  .login-field { width: 100%; border: 1.5px solid #e0dcd6; border-radius: 6px; padding: 0.65rem 0.9rem; font-size: 0.95rem; font-family: inherit; color: var(--text); background: #fafaf8; margin-bottom: 0.8rem; outline: none; transition: border-color 0.15s; }
  .login-field:focus { border-color: var(--navy); }
  .login-btn { width: 100%; background: var(--navy); color: var(--white); border: none; border-radius: 6px; padding: 0.7rem; font-size: 0.95rem; font-weight: 600; cursor: pointer; letter-spacing: 0.04em; transition: background 0.15s; margin-top: 0.4rem; }
  .login-btn:hover { background: #243f63; }
  .login-error { color: var(--red); font-size: 0.82rem; margin-top: 0.6rem; min-height: 1.2em; }
  .login-lidera { border-top: 1px solid #e8e4de; margin-top: 1.4rem; padding-top: 1rem; display: flex; flex-direction: column; align-items: center; gap: 0.2rem; }
  .login-lidera-by { font-size: 0.62rem; color: #aaa; font-style: italic; }
  .login-lidera-inner { display: flex; align-items: center; gap: 0.45rem; margin-top: 0.3rem; }
  .login-lidera-word { font-family: 'Source Sans 3', sans-serif; font-size: 1.25rem; font-weight: 700; color: #4a4a4a; letter-spacing: 0.07em; }
  .login-lidera-name { font-size: 0.72rem; color: #888; margin-top: 0.15rem; }
  #reportContent { display: none; }
  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.45); z-index: 100; display: none; align-items: flex-start; justify-content: center; padding: 2rem 1rem; overflow-y: auto; }
  .modal-overlay.open { display: flex; }
  .modal { background: var(--white); border-radius: 10px; width: 100%; max-width: 900px; box-shadow: 0 8px 40px rgba(0,0,0,0.18); animation: fadeUp 0.2s ease; }
  @keyframes fadeUp { from { opacity:0; transform: translateY(12px); } to { opacity:1; transform: translateY(0); } }
  .modal-header { background: var(--navy); color: var(--white); padding: 1.1rem 1.4rem; border-radius: 10px 10px 0 0; display: flex; align-items: center; justify-content: space-between; }
  .modal-header h3 { font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; font-weight: 600; }
  .modal-header .badge-count { background: var(--gold); font-size: 0.75rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 1rem; letter-spacing: 0.04em; }
  .modal-close { background: none; border: none; color: rgba(255,255,255,0.8); font-size: 1.4rem; cursor: pointer; line-height: 1; padding: 0 0.2rem; }
  .modal-close:hover { color: var(--white); }
  .modal-body { padding: 1.2rem 1.4rem 1.4rem; overflow-x: auto; }
  .modal-body table { font-size: 0.84rem; }
  .modal-stats { display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap; }
  .modal-stat { flex: 1; min-width: 130px; background: var(--cream); border-radius: 6px; padding: 0.6rem 0.9rem; }
  .modal-stat label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.07em; color: var(--muted); display: block; }
  .modal-stat .val { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; font-weight: 600; color: var(--navy); }
  @media (max-width: 700px) {
    .chart-row { grid-template-columns: 1fr; }
    .kpi-grid { grid-template-columns: 1fr 1fr; }
    .modal-overlay { padding: 0; align-items: flex-end; }
    .modal { border-radius: 12px 12px 0 0; }
  }
</style>
</head>
<body>

<!-- Login overlay -->
<div id="loginOverlay">
  <div class="login-box">
    <div class="logo">CORCUDEC</div>
    <div class="gold-bar"></div>
    <div class="sub">Análisis Salarial Interno · Julio 2026</div>
    <input id="loginUser" class="login-field" type="text" placeholder="Usuario" autocomplete="username">
    <input id="loginPass" class="login-field" type="password" placeholder="Contraseña" autocomplete="current-password">
    <button class="login-btn" id="loginBtn">Acceder</button>
    <div class="login-error" id="loginError"></div>
    <div class="login-lidera">
      <div class="login-lidera-by">Análisis desarrollado por</div>
      <div class="login-lidera-inner">
        <svg width="36" height="42" viewBox="0 0 68 72" fill="none" xmlns="http://www.w3.org/2000/svg">
          <ellipse cx="14" cy="8"  rx="7" ry="8"  fill="#D4623B"/>
          <ellipse cx="14" cy="19" rx="3.5" ry="3" fill="#D4623B"/>
          <ellipse cx="14" cy="28" rx="7" ry="8"  fill="#D4623B"/>
          <ellipse cx="14" cy="39" rx="3.5" ry="3" fill="#D4623B"/>
          <ellipse cx="14" cy="48" rx="7" ry="8"  fill="#D4623B"/>
          <ellipse cx="14" cy="59" rx="3.5" ry="3" fill="#D4623B"/>
          <ellipse cx="14" cy="68" rx="7" ry="4"  fill="#D4623B"/>
          <ellipse cx="34" cy="8"  rx="7" ry="8"  fill="#7B3A8E"/>
          <ellipse cx="34" cy="19" rx="3.5" ry="3" fill="#7B3A8E"/>
          <ellipse cx="34" cy="28" rx="7" ry="8"  fill="#7B3A8E"/>
          <ellipse cx="34" cy="39" rx="3.5" ry="3" fill="#7B3A8E"/>
          <ellipse cx="34" cy="48" rx="7" ry="8"  fill="#7B3A8E"/>
          <ellipse cx="34" cy="59" rx="3.5" ry="3" fill="#7B3A8E"/>
          <ellipse cx="34" cy="68" rx="7" ry="4"  fill="#7B3A8E"/>
          <ellipse cx="54" cy="8"  rx="7" ry="8"  fill="#259990"/>
          <ellipse cx="54" cy="19" rx="3.5" ry="3" fill="#259990"/>
          <ellipse cx="54" cy="28" rx="7" ry="8"  fill="#259990"/>
          <ellipse cx="54" cy="39" rx="3.5" ry="3" fill="#259990"/>
          <ellipse cx="54" cy="48" rx="7" ry="8"  fill="#259990"/>
          <ellipse cx="54" cy="59" rx="3.5" ry="3" fill="#259990"/>
          <ellipse cx="54" cy="68" rx="7" ry="4"  fill="#259990"/>
        </svg>
        <span class="login-lidera-word">LIDERA</span>
      </div>
      <div class="login-lidera-name">Consultora Lidera</div>
    </div>
  </div>
</div>

<div id="reportContent">
<header>
  <div class="hdr-left">
    <h1>Corporación Cultural<br>Universidad de Concepción</h1>
    <div class="hdr-rule"></div>
    <div class="hdr-sub">Orquesta Sinfónica Universidad de Concepción</div>
    <div class="hdr-sub2">Análisis de Dotación y Bandas Salariales · Julio 2026</div>
    <span class="badge">JULIO 2026 · {{ stats.total_empleados }} TRABAJADORES ACTIVOS</span>
  </div>
  <div class="hdr-divider"></div>
  <div class="hdr-right">
    <div class="lidera-card">
      <div class="lidera-by">Análisis desarrollado por</div>
      <!-- Bead columns SVG (centered) -->
      <svg width="68" height="72" viewBox="0 0 68 72" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- Orange column (left) -->
        <ellipse cx="14" cy="8"  rx="7" ry="8"  fill="#D4623B"/>
        <ellipse cx="14" cy="19" rx="3.5" ry="3" fill="#D4623B"/>
        <ellipse cx="14" cy="28" rx="7" ry="8"  fill="#D4623B"/>
        <ellipse cx="14" cy="39" rx="3.5" ry="3" fill="#D4623B"/>
        <ellipse cx="14" cy="48" rx="7" ry="8"  fill="#D4623B"/>
        <ellipse cx="14" cy="59" rx="3.5" ry="3" fill="#D4623B"/>
        <ellipse cx="14" cy="68" rx="7" ry="4"  fill="#D4623B"/>
        <!-- Purple column (center) -->
        <ellipse cx="34" cy="8"  rx="7" ry="8"  fill="#7B3A8E"/>
        <ellipse cx="34" cy="19" rx="3.5" ry="3" fill="#7B3A8E"/>
        <ellipse cx="34" cy="28" rx="7" ry="8"  fill="#7B3A8E"/>
        <ellipse cx="34" cy="39" rx="3.5" ry="3" fill="#7B3A8E"/>
        <ellipse cx="34" cy="48" rx="7" ry="8"  fill="#7B3A8E"/>
        <ellipse cx="34" cy="59" rx="3.5" ry="3" fill="#7B3A8E"/>
        <ellipse cx="34" cy="68" rx="7" ry="4"  fill="#7B3A8E"/>
        <!-- Teal column (right) -->
        <ellipse cx="54" cy="8"  rx="7" ry="8"  fill="#259990"/>
        <ellipse cx="54" cy="19" rx="3.5" ry="3" fill="#259990"/>
        <ellipse cx="54" cy="28" rx="7" ry="8"  fill="#259990"/>
        <ellipse cx="54" cy="39" rx="3.5" ry="3" fill="#259990"/>
        <ellipse cx="54" cy="48" rx="7" ry="8"  fill="#259990"/>
        <ellipse cx="54" cy="59" rx="3.5" ry="3" fill="#259990"/>
        <ellipse cx="54" cy="68" rx="7" ry="4"  fill="#259990"/>
      </svg>
      <div class="lidera-wordmark">LIDERA</div>
      <div class="lidera-gold-rule"></div>
      <div class="lidera-name">Consultora Lidera</div>
      <div class="lidera-tagline">Consultoría en Gestión de Personas y Organizaciones</div>
    </div>
  </div>
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
    <div class="chart-box">
      <canvas id="chartDept" height="140"></canvas>
      <p class="chart-hint">↑ Haz clic en una barra para ver los trabajadores del área</p>
    </div>
  </div>
</section>

<section>
  <h2>Escalafón por Nivel de Cargo</h2>
  <div class="chart-row single">
    <div class="chart-box">
      <canvas id="chartNivel" height="90"></canvas>
      <p class="chart-hint">↑ Haz clic en una barra para ver los trabajadores del nivel</p>
    </div>
  </div>
  <br>
  <table>
    <thead><tr>
      <th>Nivel</th><th class="num">N°</th><th class="num">SB Promedio</th>
      <th class="num">SB Mínimo</th><th class="num">SB Máximo</th><th class="num">Haberes Prom.</th>
    </tr></thead>
    <tbody>
    {% for _, row in nivel_df.iterrows() %}
    <tr class="drillable" data-drill="nivel" data-value="{{ row.nivel }}">
      <td>{{ row.nivel }}</td>
      <td class="num">{{ row.empleados }}</td>
      <td class="num">{{ format_clp(row.sb_promedio) }}</td>
      <td class="num">{{ format_clp(row.sb_min) }}</td>
      <td class="num">{{ format_clp(row.sb_max) }}</td>
      <td class="num">{{ format_clp(row.haberes_promedio) }}</td>
    </tr>
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
    <div class="chart-box" style="grid-column: span 1"><img src="data:image/png;base64,{{ graficas.genero }}" alt="Equidad género"></div>
    <div style="display: flex; flex-direction: column; gap: 1rem; justify-content: center;">
      <div class="kpi"><label>SB promedio hombres</label><div class="value">{{ format_clp(genero.sb_promedio_hombres) }}</div></div>
      <div class="kpi"><label>SB promedio mujeres</label><div class="value">{{ format_clp(genero.sb_promedio_mujeres) }}</div></div>
      <div class="kpi {% if genero.brecha_porcentual|abs < 5 %}green{% else %}gold{% endif %}">
        <label>Brecha salarial (H–M)</label>
        <div class="value">{{ "%.1f"|format(genero.brecha_porcentual) }}%</div>
        <div class="sub">{% if not genero.diferencia_significativa %}No significativa estadísticamente{% else %}Diferencia significativa (p={{ "%.3f"|format(genero.p_value) }}){% endif %}</div>
      </div>
    </div>
  </div>
</section>

<section>
  <h2>Top 10 Remuneraciones (Total Haberes)</h2>
  <table>
    <thead><tr>
      <th>#</th><th>Cargo</th><th>Área</th><th>Nivel</th>
      <th class="num">Sueldo Base</th><th class="num">Total Haberes</th><th class="num">Líquido</th>
    </tr></thead>
    <tbody>
    {% for _, row in top_df.iterrows() %}
    <tr>
      <td>{{ loop.index }}</td>
      <td>{{ row.cargo }}</td>
      <td><span class="tag {% if row.departamento == 'Orquesta' %}tag-orch{% elif row.departamento == 'Administración' %}tag-admin{% else %}tag-dir{% endif %}">{{ row.departamento }}</span></td>
      <td>{{ row.nivel }}</td>
      <td class="num">{{ format_clp(row.sueldo_base) }}</td>
      <td class="num">{{ format_clp(row.total_haberes) }}</td>
      <td class="num">{{ format_clp(row.liquido) }}</td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</section>

<section>
  <h2>Por Área</h2>
  <table>
    <thead><tr>
      <th>Área</th><th class="num">N°</th><th class="num">SB Promedio</th>
      <th class="num">SB Mediana</th><th class="num">Haberes Prom.</th><th class="num">Masa SB</th>
    </tr></thead>
    <tbody>
    {% for _, row in dept_df.iterrows() %}
    <tr class="drillable" data-drill="departamento" data-value="{{ row.departamento }}">
      <td><span class="tag {% if row.departamento == 'Orquesta' %}tag-orch{% elif row.departamento == 'Administración' %}tag-admin{% else %}tag-dir{% endif %}">{{ row.departamento }}</span></td>
      <td class="num">{{ row.empleados }}</td>
      <td class="num">{{ format_clp(row.sb_promedio) }}</td>
      <td class="num">{{ format_clp(row.sb_mediana) }}</td>
      <td class="num">{{ format_clp(row.haberes_promedio) }}</td>
      <td class="num">{{ format_mclp(row.masa_sb) }}</td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</section>

<div class="info-box">
  <strong>Fuente:</strong> Imagen de Remuneraciones Julio 2026 · CORCUDEC.<br>
  Incluye 74 trabajadores activos (1 funcionario con licencia excluido). Datos en pesos chilenos (CLP) corrientes.
  Generado: {{ fecha_generacion }}.
</div>

</main>
<footer>Corporación Cultural Universidad de Concepción &nbsp;|&nbsp; Análisis Salarial Interno &nbsp;|&nbsp; {{ fecha_generacion }}</footer>
</div><!-- /reportContent -->

<!-- Modal drill-down -->
<div class="modal-overlay" id="modalOverlay">
  <div class="modal">
    <div class="modal-header">
      <h3 id="modalTitle">Detalle</h3>
      <div style="display:flex;align-items:center;gap:0.8rem">
        <span class="badge-count" id="modalCount"></span>
        <button class="modal-close" id="modalClose" aria-label="Cerrar">×</button>
      </div>
    </div>
    <div class="modal-body">
      <div class="modal-stats" id="modalStats"></div>
      <div style="overflow-x:auto">
        <table id="modalTable">
          <thead id="modalThead"></thead>
          <tbody id="modalTbody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script>
// ── Auth ─────────────────────────────────────────────────
const AUTH_USER_HASH = "{{ auth_user_hash }}";
const AUTH_PASS_HASH = "{{ auth_pass_hash }}";

async function sha256(str) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

function showReport() {
  document.getElementById('loginOverlay').classList.add('hidden');
  document.getElementById('reportContent').style.display = 'block';
}

(async () => {
  if (sessionStorage.getItem('corcudec_auth') === '1') { showReport(); return; }
})();

document.getElementById('loginBtn').addEventListener('click', async () => {
  const user = document.getElementById('loginUser').value.trim();
  const pass = document.getElementById('loginPass').value;
  const err  = document.getElementById('loginError');
  err.textContent = '';
  if (!user || !pass) { err.textContent = 'Ingresa usuario y contraseña.'; return; }
  const [uh, ph] = await Promise.all([sha256(user), sha256(pass)]);
  if (uh === AUTH_USER_HASH && ph === AUTH_PASS_HASH) {
    sessionStorage.setItem('corcudec_auth', '1');
    showReport();
  } else {
    err.textContent = 'Credenciales incorrectas.';
    document.getElementById('loginPass').value = '';
  }
});

['loginUser','loginPass'].forEach(id => {
  document.getElementById(id).addEventListener('keydown', e => {
    if (e.key === 'Enter') document.getElementById('loginBtn').click();
  });
});

// ── Data ──────────────────────────────────────────────────
const EMPLEADOS = {{ empleados_json }};

function fmtClp(v) {
  return '$' + Math.round(v).toLocaleString('es-CL');
}
function avg(arr) {
  return arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
}

// ── Dept chart ────────────────────────────────────────────
const DEPT_COLORS = {
  'Orquesta': '#1C3557',
  'Administración': '#2E7D52',
  'Dirección Musical': '#8B1A1A',
};
const deptGroups = {};
EMPLEADOS.forEach(e => {
  (deptGroups[e.departamento] = deptGroups[e.departamento] || []).push(e);
});
const deptLabels = Object.keys(deptGroups).sort(
  (a, b) => avg(deptGroups[a].map(e => e.sueldo_base)) - avg(deptGroups[b].map(e => e.sueldo_base))
);
new Chart(document.getElementById('chartDept'), {
  type: 'bar',
  data: {
    labels: deptLabels,
    datasets: [{
      data: deptLabels.map(d => avg(deptGroups[d].map(e => e.sueldo_base)) / 1e6),
      backgroundColor: deptLabels.map(d => (DEPT_COLORS[d] || '#1C3557') + 'cc'),
      borderColor: deptLabels.map(d => DEPT_COLORS[d] || '#1C3557'),
      borderWidth: 1.5,
      borderRadius: 4,
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    onClick(e, els) { if (els.length) openDrill('departamento', deptLabels[els[0].index]); },
    onHover(e, els) { e.native.target.style.cursor = els.length ? 'pointer' : 'default'; },
    plugins: {
      legend: { display: false },
      title: { display: true, text: 'Sueldo Base Promedio por Área', font: { size: 13, weight: 'bold' }, color: '#1a1a2e' },
      tooltip: { callbacks: { label: ctx => ' ' + fmtClp(ctx.raw * 1e6) + ' — clic para detalle' } }
    },
    scales: {
      x: { ticks: { callback: v => '$' + Number(v).toFixed(1) + 'M' }, grid: { color: '#f0ede8' } },
      y: { grid: { display: false } }
    }
  }
});

// ── Nivel chart ───────────────────────────────────────────
const NIVEL_ORDER = ['Director','Concertino','Asistente Concertino','Jefatura',
                     'Jefe de Fila','Asistente de Fila','Tutti','Administrativo'];
function nivelColor(n) {
  if (n === 'Director') return '#8B1A1A';
  if (n === 'Concertino' || n === 'Asistente Concertino') return '#B8892A';
  if (['Jefe de Fila','Asistente de Fila','Tutti'].includes(n)) return '#1C3557';
  return '#2E7D52';
}
const nivelGroups = {};
EMPLEADOS.forEach(e => {
  (nivelGroups[e.nivel] = nivelGroups[e.nivel] || []).push(e);
});
const nivelLabels = NIVEL_ORDER.filter(n => nivelGroups[n]);
new Chart(document.getElementById('chartNivel'), {
  type: 'bar',
  data: {
    labels: nivelLabels,
    datasets: [{
      data: nivelLabels.map(n => avg(nivelGroups[n].map(e => e.sueldo_base)) / 1e6),
      backgroundColor: nivelLabels.map(n => nivelColor(n) + 'cc'),
      borderColor: nivelLabels.map(n => nivelColor(n)),
      borderWidth: 1.5,
      borderRadius: 4,
    }]
  },
  options: {
    responsive: true,
    onClick(e, els) { if (els.length) openDrill('nivel', nivelLabels[els[0].index]); },
    onHover(e, els) { e.native.target.style.cursor = els.length ? 'pointer' : 'default'; },
    plugins: {
      legend: { display: false },
      title: { display: true, text: 'Escalafón Salarial por Nivel', font: { size: 13, weight: 'bold' }, color: '#1a1a2e' },
      tooltip: { callbacks: { label: ctx => ' ' + fmtClp(ctx.raw * 1e6) + ' — clic para detalle' } }
    },
    scales: {
      y: { ticks: { callback: v => '$' + Number(v).toFixed(1) + 'M' }, grid: { color: '#f0ede8' } },
      x: { grid: { display: false } }
    }
  }
});

// ── Modal ─────────────────────────────────────────────────
const overlay = document.getElementById('modalOverlay');

function openDrill(campo, valor) {
  const rows = EMPLEADOS.filter(e => e[campo] === valor);
  const sbs = rows.map(e => e.sueldo_base);
  const habs = rows.map(e => e.total_haberes);

  document.getElementById('modalTitle').textContent = valor;
  document.getElementById('modalCount').textContent = rows.length + ' trabajadores';

  document.getElementById('modalStats').innerHTML = `
    <div class="modal-stat"><label>SB Promedio</label><div class="val">${fmtClp(avg(sbs))}</div></div>
    <div class="modal-stat"><label>SB Mínimo</label><div class="val">${fmtClp(Math.min(...sbs))}</div></div>
    <div class="modal-stat"><label>SB Máximo</label><div class="val">${fmtClp(Math.max(...sbs))}</div></div>
    <div class="modal-stat"><label>Haberes Prom.</label><div class="val">${fmtClp(avg(habs))}</div></div>
  `;

  const extraHeader = campo === 'departamento' ? 'Nivel' : 'Área';
  document.getElementById('modalThead').innerHTML = `<tr>
    <th>#</th><th>Cargo</th><th>${extraHeader}</th><th>Sexo</th>
    <th class="num">Sueldo Base</th><th class="num">Total Haberes</th><th class="num">Líquido</th>
  </tr>`;

  const sorted = [...rows].sort((a, b) => b.sueldo_base - a.sueldo_base);
  document.getElementById('modalTbody').innerHTML = sorted.map((e, i) => {
    const extra = campo === 'departamento' ? e.nivel : e.departamento;
    return `<tr>
      <td>${i + 1}</td>
      <td>${e.cargo}</td>
      <td>${extra}</td>
      <td>${e.sexo === 'M' ? 'H' : 'M'}</td>
      <td class="num">${fmtClp(e.sueldo_base)}</td>
      <td class="num">${fmtClp(e.total_haberes)}</td>
      <td class="num">${fmtClp(e.liquido)}</td>
    </tr>`;
  }).join('');

  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeDrill() {
  overlay.classList.remove('open');
  document.body.style.overflow = '';
}

document.getElementById('modalClose').addEventListener('click', closeDrill);
overlay.addEventListener('click', e => { if (e.target === overlay) closeDrill(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDrill(); });

document.querySelectorAll('tr.drillable').forEach(tr => {
  tr.addEventListener('click', () => openDrill(tr.dataset.drill, tr.dataset.value));
});
</script>
</body>
</html>
"""


def generar_reporte(stats, genero, nivel_df, dept_df, top_df, graficas, ruta_salida, df=None,
                    auth_user_hash='', auth_pass_hash=''):
    def format_clp(v):
        if v is None or (isinstance(v, float) and v != v):
            return '$0'
        return f'${int(v):,}'.replace(',', '.')

    def format_mclp(v):
        return f'${v/1_000_000:.1f}M'

    cols = ['cargo', 'departamento', 'nivel', 'sexo', 'sueldo_base', 'total_haberes', 'liquido']
    if df is not None:
        records = df[cols].to_dict('records')
        for r in records:
            for k in ('sueldo_base', 'total_haberes', 'liquido'):
                r[k] = int(r[k]) if r[k] == r[k] else 0
    else:
        records = []
    empleados_json = json.dumps(records, ensure_ascii=False)

    tpl = Template(TEMPLATE_HTML)
    html = tpl.render(
        stats=stats,
        genero=genero,
        nivel_df=nivel_df,
        dept_df=dept_df,
        top_df=top_df,
        graficas=graficas,
        format_clp=format_clp,
        format_mclp=format_mclp,
        empleados_json=empleados_json,
        auth_user_hash=auth_user_hash,
        auth_pass_hash=auth_pass_hash,
        fecha_generacion=__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M'),
    )
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    return ruta_salida
