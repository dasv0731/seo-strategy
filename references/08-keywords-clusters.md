# 09 · Keyword research y mapa por cluster — CONSUMIR

**NO corras el estudio de keywords aquí.** arquitectura-seo ya lo hizo:
`Clientes\<slug>\arquitectura\resultados\mapa-keywords.csv` (keyword, cluster_id, es_principal,
volumen, dificultad, cpc, tendencia, intencion, fuente). Si te descubres inventando volúmenes o
listas de keywords, **DETENTE**.

**Recipe:** referencia `mapa-keywords.csv` como fuente de verdad; embebe un resumen derivado (un
cluster por servicio flagship/secundario/sector/ubicación + tabla de total de páginas indexables
año 1, leída del árbol); añade la lectura estratégica (qué clusters son la apuesta del año 1 según
la restricción dominante). El análisis continuo (quick wins, canibalización) es de seo-analisis-gsc.

**Si falta `mapa-keywords.csv`:** DETENERSE y derivar a correr arquitectura-seo. No reconstruyas el estudio tú.

---

## Resumen derivado por cluster (leído de `mapa-keywords.csv`)
No re-tabules keywords a mano. Agrupa `mapa-keywords.csv` por `cluster_id` — un cluster por servicio flagship, secundario, sector y ubicación — y embebe en §9 del spec un resumen compacto marcado *"(derivado de mapa-keywords.csv; fuente de verdad ahí)"*:

| Cluster | Keyword principal (`es_principal`) | Página canónica | Vol. | Dificultad | SERP hoy | Prioridad |
|---|---|---|---|---|---|---|
| automatización | automatización industrial | hub | 200-500 | media | AI Overview + service pages | P1 |
| PLC | programación PLC Siemens | spoke PLC | 30-100 | baja | service pages nicho | P1 |
| ubicación Quito | empresa automatización Quito | `/ubicaciones/quito` | 30-100 | baja | local pack + directorios | P2 |
| permisos (info) | permisos ARCERNNR | blog | — | baja | guías, sin AI Overview | P3 |

- `Vol.`, `Dificultad`, `intencion` y `tendencia` **se leen de las columnas del CSV**, no se estiman aquí.
- **SERP hoy** (features presentes + qué page-type rankea) y **Prioridad** son la **capa estratégica** que master añade sobre el CSV: valor de negocio (flagship/margen/intent) × esfuerzo (dificultad + contenido necesario). P1 se produce primero; una keyword de volumen alto con SERP hostil puede ser P3. La lectura del SERP **caduca** (principio 10) — re-revisar en los gates; con datos en vivo vía el SERP reality check de `03` / `orquestador-seo`.
- Cada cluster de servicio define su **pillar de blog** + N posts cluster (cola larga). Las queries informacionales → blog, enlazando al hub comercial (separación de intent en `03`).

## Qué clusters son la apuesta del año 1 (capa estratégica — se conserva)
Leyendo el resumen contra la **restricción dominante (§0.1)**, master decide qué clusters concentran la inversión de contenido del año 1 y cuáles esperan a fase 2. Esta priorización es lo que arquitectura-seo NO aporta: el CSV trae los números; el juicio de dónde apostar lo pone el spec.

## Disciplina anti-thin (clave en YMYL y negocios pequeños)
**Abrir un spoke solo cuando haya volumen Y contenido único** que lo justifique. En negocios pequeños, empezar con hubs y dejar spokes para fase 2. La **validación continua** (¿el cluster ganó tracción?, quick wins, canibalización real) es de **seo-analisis-gsc** con data GSC trimestral antes de expandir — no se simula aquí.

## Total de páginas indexables (año 1) — leído del árbol
El conteo por tipo se **deriva del árbol** (`arquitectura.csv`, ver `03`), no se inventa. Embébelo como parte del resumen derivado para dimensionar el esfuerzo de contenido:

| Tipo | AioTech (matriz) | Inspira (especialidad) |
|---|---|---|
| Core estáticas | 5 | 9 |
| Hubs de servicio/área | 5 | 6 |
| Spokes | 19 | 0-6 (fase 2) |
| Sectores | 4 | — |
| Ubicaciones / modalidad | 7 | 2 |
| Casos | 8-15 | — |
| Pillar pages | 5 | 4-5 |
| Cluster posts | 30-40 | 20-30 |
| **Total año 1** | **~80-95** | **~45-60** |

El inventario debe ser **sostenible con los recursos reales** de producción de contenido (ver `09-content-roadmap.md`).
