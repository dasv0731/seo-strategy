# 12 · Las ~15 fases de un plan de implementación

El plan deriva del spec y es **operativo**: ejecutable tarea-por-tarea con checkboxes `- [ ]`, pensado para agentes (`superpowers:subagent-driven-development` o `executing-plans`). Uno por mes/trimestre.

Output: `docs/superpowers/plans/YYYY-MM-DD-{cliente}-seo-mesN-plan.md`

## Header del plan
`Goal` · `Architecture` (resumen del spec) · `Tech Stack` (con costos) · `File Structure` (archivos físicos / config en BD / servicios externos).

## Estructura jerárquica
**Fase N → Tarea N.M → Paso 1,2,3…** Cada tarea termina con un **paso de validación + commit**. Los pasos incluyen comandos exactos, snippets y criterios de "hecho".

## Fase 0 — Pre-requisitos (BLOQUEANTE)
Datos del cliente antes de tocar nada técnico: crear **checklist de datos privada**, marcar datos críticos por fase, confirmar dominio (whois), **validar credenciales reales** (YMYL), confirmar compromisos operativos sostenibles del copy.

**Sitio existente con tráfico:** insertar las fases M0-M2 de `references/13-migracion-sitio-existente.md` (inventario+benchmark, matriz keep/kill, mapa 301) antes de la Fase 1. El **inventario keep/improve/consolidate/kill + `mapeo-301.csv` los produce arquitectura-seo (modo migración)** — estas fases los **consumen**, no los regeneran. Pre-launch (13) añade el crawl diff staging vs producción y Launch/Post-launch (14-15) usan su ventana de monitoreo.

## Las 15 fases (genéricas, reordenables según stack)
1. **Infraestructura** — hosting, DNS/CDN, SSL, config base, .htaccess/redirects.
2. **Hardening + módulos core** — security, backups, redirects, cleanup de bloat.
3. **Stack SEO** — motor SEO + custom fields + registro de content-types (**según el árbol de `arquitectura.csv`**, ya producido por arquitectura-seo) + field groups + sitemap.
4. **Schemas custom** — el módulo **inyecta** el grafo JSON-LD que **ya produjo schema-graph** (snippets por content-type con `@id` resuelto); **no se diseña ni valida el schema en esta fase**.
5. **Builder + templates + componentes** — plantillas por content-type + bloques de internal linking reutilizables (**según `enlazado.csv`**, ya producido por arquitectura-seo).
6. **Performance** — caché, imágenes (WebP/AVIF), fonts/critical CSS.
7. **Forms + conversión** — anti-spam, prefill contextual, WhatsApp/booking.
8. **Tracking + Analytics** — GA4, GTM, GSC, Bing, CRM, eventos de conversión.
9. **Foundation files** — robots.txt, llms.txt, sitemap live.
10. **Páginas del hito** — copy (**redacción → content-engine**; **estructura de secciones → diseño-secciones**) + montaje + menús + legales (privacidad/términos).
11. **GBP setup** completo.
12. **NAP citations** top 5.
13. **Pre-launch** — validación de schema, performance, mobile, links/404, forms, robots/sitemap, checklist.
14. **Launch** — submit sitemap + IndexNow, anunciar, solicitar indexación en GSC, monitoreo.
15. **Post-launch monitoring** — semana 1: monitoreo diario + iteraciones.

Apéndice del plan: datos a confirmar + resumen ejecutivo.

## Self-Review (cierre del plan) — OBLIGATORIO
Tabla que mapea **cada sección §1-§14 del spec → la(s) fase(s) que la cubren**. Garantiza trazabilidad spec↔plan y que nada del spec quedó sin implementar.

## Definition of Done del hito
Checklist de cierre: producción con HTTPS/sin-www/headers · páginas core publicadas, indexables, con schema válido · grafo JSON-LD sin errores · GBP en verificación + NAP consistente · GSC+Bing+GA4 + sitemap + eventos de conversión · robots.txt + llms.txt · CWV en target mobile · (YMYL: disclaimers + protección de datos presentes) · content-types + templates listos para el siguiente mes.

## Validación final de lanzamiento
PSI mobile · tap targets/texto · indexabilidad (sin noindex accidental, "discourage search engines" desmarcado) · schema de todas las páginas · enlaces internos/404 (páginas aún no creadas → "próximamente", **nunca enlazar a 404**) · conversión end-to-end · solicitar indexación en GSC.
