# seo-master-plan

Skill de Claude Code que codifica una **metodología SEO integral a 12 meses**, 100% enfocada en SEO y **agnóstica al stack** (cualquier CMS o framework).

Destilado de dos planes SEO reales:
- **B2B industrial** — arquitectura matriz cruzada (servicios × sectores × ubicaciones), marca `Organization`.
- **YMYL salud (persona)** — arquitectura especialidad-first, marca `Person`.

## Qué hace

Guía el pipeline completo de una estrategia SEO:

```
Discovery → Design Spec (§0–§14) → Planes por mes/trimestre → Contenido → KPIs
```

con 7 principios transversales (el #1: identificar la *restricción dominante* antes de la arquitectura).

## Estructura

```
SKILL.md            Punto de entrada: pipeline, principios, índice, anti-patrones
references/         13 referencias temáticas (discovery, spec, arquitectura, schema,
                    local/GBP, GEO/E-E-A-T, technical, keywords, contenido, KPIs,
                    link building, fases de plan, case-studies comparativo)
templates/          4 plantillas (content-brief, page-brief, competitive-audit, team-bio)
```

## Instalación

Clónalo dentro de tu carpeta de skills de Claude Code:

```bash
git clone https://github.com/dasv0731/seo-strategy.git ~/.claude/skills/seo-master-plan
```

En Windows (PowerShell):

```powershell
git clone https://github.com/dasv0731/seo-strategy.git "$env:USERPROFILE\.claude\skills\seo-master-plan"
```

El skill se activa al iniciar un proyecto SEO o ante frases como *"plan SEO"*, *"estrategia SEO"*, *"arquitectura SEO"*.

## Se integra con

- [`claude-seo`](https://github.com/AgriciDaniel/claude-seo) — motor de datos/análisis en vivo (auditorías, DataForSEO, GSC, schema, técnico, local, GEO).
- [`orquestador-seo`](https://github.com/dasv0731/orquestador-seo) — orquestador que combina este skill estratégico con `claude-seo`.
