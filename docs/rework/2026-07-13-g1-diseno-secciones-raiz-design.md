---
title: G1 — Migrar diseño-secciones a la raíz canónica Clientes\<slug>\
date: 2026-07-13
status: draft
owner: dasv0731
phase: design-spec
---

# G1 — diseño-secciones a `Clientes\<slug>\`

## Objetivo

Migrar `diseño-secciones` de la raíz vieja `~/seo-clientes/<slug>/` (modelo del orquestador
pre-ecosistema) a la raíz canónica **`C:\Users\Marke\Documents\Respaldo SEO\Clientes\<slug>\`**,
apuntándola a los artefactos reales del ecosistema. Alcance quirúrgico: solo rutas y nombres de
artefactos; la metodología (diagnóstico, tiers de evidencia, matriz por tipo de página) queda intacta.

## Decisión de alcance

- G1 = **solo diseño-secciones**. La migración de la raíz de orquestador-seo se absorbe en **G4**,
  porque su raíz es inseparable de su modelo de alta (PROJECT.md vs `contexto`, conexiones.md vs
  `.json`, repo por cliente) que diverge del ecosistema real y hay que reconciliarlo entero.
- Nota para G4 (no en alcance aquí): el orquestador **se queda como skill** (no agente) —
  orquestar = invocar/secuenciar otras skills/subagentes, capacidad del loop principal, no de un
  subagente. Su rework en G4 es de contenido (routing + modelo de cliente), no de tipo.

## Cambios

**Raíz:** `~/seo-clientes/<slug>/` → `C:\Users\Marke\Documents\Respaldo SEO\Clientes\<slug>\`
(hardcodeada como base-cliente / extraccion / interlinking / arquitectura-seo — consistencia con
las hermanas doc-driven).

**Remapeo de lo que LEE:**
| Antes (`~/seo-clientes/<slug>/`) | Ahora (`Clientes\<slug>\`) |
|---|---|
| `PROJECT.md` (negocio + vertical + tono) | `base\contexto-<slug>.md` (negocio) + spec `docs\superpowers\specs\*-seo-design.md` (§0.1 restricción dominante, §1 vertical/tono) si existe |
| `discovery/` | `docs\superpowers\discovery\` |
| `keywords/` | `keywords\` (igual) |
| `data/seo.db` | `data\seo.db` (igual) |
| crawl `page_source/*.html` | `data\page_source\` (de extraccion, igual) |

**ESCRIBE:** `secciones/<slug-pagina>/{01-informe-disenador, 02-informe-redactor, 03-informe-final}`
→ bajo `Clientes\<slug>\secciones\<slug-pagina>\`.

**Degradación (se conserva la actual, solo cambian rutas/nombres):** si falta el spec → cae al
`contexto`/discovery para vertical/tono; si falta `contexto` → intake mínimo y preguntar dónde guardar.

## Archivos a tocar (doc-driven, sin código con paths de cliente)

`SKILL.md`, `references/redaccion.md`, `templates/informe-redactor.md`, y cualquier otra referencia
que mencione `~/seo-clientes` o `PROJECT.md` (grep exhaustivo al implementar). NO tocar la
metodología (references de diagnóstico, tipos de página, elementos-layout, accesibilidad).

## Verificación

1. `grep -rn "seo-clientes\|PROJECT.md" diseno-secciones/` (excluyendo historial) → 0 como fuente
   de cliente (salvo notas de compatibilidad si se dejan).
2. Test de escenario: un subagente neutral produce las secciones de una página para un
   cliente-fixture en `Clientes\<slug>\` y confirma que (a) resuelve la raíz canónica, (b) lee
   `contexto`/spec/keywords, (c) escribe en `Clientes\<slug>\secciones\<slug-pagina>\`.

## Fuera de alcance
- Root/rework del orquestador (→ G4). Reconciliar PROJECT.md → contexto en el orquestador (→ G4).
