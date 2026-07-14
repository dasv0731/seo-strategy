# 00b · Flujo de dos fases y contratos de consumo

seo-master-plan **consume** artefactos de otras skills; no los regenera. Corre en dos momentos,
con arquitectura-seo en medio.

## Las dos fases

**FRAMING** (antes de arquitectura-seo):
- Lee `Clientes\<slug>\base\contexto-<slug>.md` (base-cliente). Si falta → entrevista de discovery
  (fallback) y sugiere base-cliente. No bloquea.
- Razona §0 panorama · §0.1 restricción dominante · §1 decisiones estratégicas · §2 elección de
  enfoque de arquitectura. NO escribe el spec: deja este razonamiento en el discovery doc +
  `enfoque.md`.
- Escribe el handoff `Clientes\<slug>\arquitectura\data\enfoque.md` (formato abajo) y
  `Clientes\<slug>\docs\superpowers\discovery\<fecha>-<slug>-discovery.md`.

**arquitectura-seo** corre (consume `enfoque.md`) → `arquitectura\resultados\arquitectura.csv`,
`enlazado.csv`, `mapa-keywords.csv` + `sitio.yaml`.

**ENSAMBLAJE** (después):
- Lee (requerido) `arquitectura\resultados\arquitectura.csv`, `enlazado.csv`, `mapa-keywords.csv`.
- Lee (opcional, Escenario A) el bundle de diagnóstico.
- Escribe el spec §0–§14 completo en `Clientes\<slug>\docs\superpowers\specs\<fecha>-<slug>-seo-design.md`
  y los planes en `...\plans\`.

## Formato de `enfoque.md` (lo consume arquitectura-seo Fase 0)

```
# Enfoque — <cliente>

**Qué priorizar:** <líneas/servicios a potenciar, derivado de la restricción dominante>
**Dimensiones de arquitectura:** <servicios | sectores | ubicaciones | especialidades ...>
**País/idioma:** <location_code / language_code, confirmado contra conexiones.json>
**Modelo de conversión:** <compra | lead | whatsapp | llamada | booking>
**Competidores conocidos:** <lista o "ninguno declarado">
```

## Contrato de inputs que consumo

| Artefacto | De | Sección que lo consume | Requerido |
|---|---|---|---|
| `base\contexto-<slug>.md` | base-cliente | §0, §7 (framing) | no (fallback entrevista) |
| `arquitectura\resultados\arquitectura.csv` | arquitectura-seo | §3 | **sí** (duro) |
| `arquitectura\resultados\enlazado.csv` | arquitectura-seo | §4 | sí |
| `arquitectura\resultados\mapa-keywords.csv` | arquitectura-seo | §9 | sí |
| bundle diagnóstico (hallazgos, interlinking, geo, cwv, linkbuilding, SCHEMA-REPORT, mapeo-301) | pipeline | §13, baseline | no (Escenario A) |

## Reglas de degradación

- Falta `arquitectura.csv` al ensamblar → **DETENERSE** y derivar a correr arquitectura-seo. No
  generar el árbol.
- Falta `contexto-<slug>.md` en framing → entrevista propia (fallback), sugiere base-cliente.
- Falta el bundle de diagnóstico (Escenario A) → ensamblar con lo que haya y marcar huecos como
  checklist de datos privada en §13. No fabricar.
- Falta salida de schema-graph → §5 se queda en anclaje estratégico + "generación pendiente: schema-graph".

## Rama de escenarios (por `estado del sitio` del discovery)

- `greenfield` | `básico` → **Escenario B**: arquitectura-seo modo greenfield (sin inventario/301);
  spec sabor foundation (§13 N/A); planes = fases de build.
- `con-tráfico` → **Escenario A**: fase de diagnóstico previa (master la CONSUME, no la corre);
  arquitectura-seo modo migración (inventario + `mapeo-301.csv`); spec sabor migración (§13 activo,
  KPI retención); planes con M0-M2 antes del build.

master **consume, no orquesta**: en el Escenario A lee los outputs del diagnóstico si existen; no
invoca las skills. El runtime que las encadena es orquestador-seo.
