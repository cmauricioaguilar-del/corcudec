# CORCUDEC — Análisis Salarial

Análisis de dotación y bandas salariales de la **Corporación Cultural Universidad de Concepción (CORCUDEC)** y su **Orquesta Sinfónica Universidad de Concepción (OSUC)**.

## Datos

- **Fuente:** Imagen de Remuneraciones Julio 2026
- **Dotación:** 74 trabajadores activos
- **Áreas:** Orquesta (48), Administración (25), Dirección Musical (1)

## Estructura

```
CORCUDEC/
├── data/
│   └── dotacion_julio2026.csv   # Datos remuneracionales julio 2026
├── src/
│   ├── analisis.py              # Cálculos y estadísticas
│   ├── visualizaciones.py       # Gráficas matplotlib/seaborn
│   └── reporte.py               # Generador HTML (Jinja2)
├── output/                      # Reportes generados
├── main.py                      # Punto de entrada
└── requirements.txt
```

## Uso

```bash
pip install -r requirements.txt
python main.py
# → output/reporte_salarial_corcudec.html
```

## Componentes salariales

| Componente | Descripción |
|---|---|
| `sueldo_base` | Sueldo base mensual |
| `quinquenio_5/10/15` | Quinquenio por tramos de 5 años (1.5% SB c/u) |
| `asig_responsabilidad` | Asignación de responsabilidad |
| `asig_especial` | Asignación especial |
| `asig_jerarquia` | Asignación de jerarquía (Asistente JF / JF) |
| `desgaste_instrumentos` | Asignación desgaste de instrumentos (músicos) |
| `total_haberes` | Suma total imponibles + no imponibles |
| `liquido` | Líquido a pagar tras descuentos |

## Convenios Colectivos

- **CC1:** Sindicato Trabajadores CORCUDEC 2025-2026 (23 trabajadores)
- **CC2:** Sindicato Músicos OSUC 2026-2027 (45 músicos)
