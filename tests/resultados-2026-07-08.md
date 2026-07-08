# Resultados de tests — 2026-07-08

## RED (baseline, skill sin modificar)

### escenario-migracion-servicios — 3/7 cubierto, 3 parciales, 1 fallo total

| Ítem esperado | Resultado |
|---|---|
| Mes 1 empieza con inventario GSC/GA4 + benchmark | ✅ Cubierto (el agente lo derivó de la única línea de discovery + criterio propio) |
| Matriz keep/improve/consolidate/kill | 🟡 Parcial: "migrar/consolidar/retirar" por URL, **sin criterios de datos** (umbrales de clics/backlinks/conversiones), sin categoría "improve" |
| Mapa 301 1:1 | ✅ Cubierto, con buen predicado de cierre |
| Quick wins M1-M2 (striking distance 5-15) | ❌ **Fallo total** — el brief decía "muchas en posición 5-15" y el agente nunca lo usó |
| Crawl diff staging vs producción | ❌ Ausente (pre-launch valida redirects/schema, pero sin diff old vs new) |
| Ventana de monitoreo post-migración estructurada | 🟡 Parcial: "diario semana 1" + retención a 4-6 semanas, sin cadencia 4-8 semanas ni criterios de alerta/rollback |
| Expectativa declarada de fluctuación | 🟡 Implícita en el KPI de retención, no declarada al cliente |

**Lección RED:** un agente fuerte improvisa ~40% del playbook de migración con conocimiento propio — eso es varianza, no cobertura. El skill debe hacerlo determinista. Nota positiva: adaptó país/idioma a Perú (`es-PE`) pese al hardcoding `EC` del ejemplo del grafo — el hardcoding es riesgo de varianza, no fallo determinista.

### escenario-ecommerce — 7/9 cubierto, 2 no ejercitados

| Ítem esperado | Resultado |
|---|---|
| Dimensiones = categorías/producto/guías | ✅ "Categoría-first", descartó matriz y ubicaciones con razón |
| Reglas de facetas | ✅ noindex por defecto + promoción a colección curada con demanda+copy |
| `Product`+`Offer`, `AggregateRating` solo real | ✅ Incluso añadió paridad schema↔feed |
| Merchant Center integrado | ✅ |
| Conversión purchase, no WhatsApp | ✅ Eventos GA4 e-commerce completos |
| País `es-MX`/MXN, nada de EC | ✅ Auto-adaptado pese al hardcoding del ejemplo |
| Capa local omitida con razón | ✅ |
| Roadmap año 1 forma catálogo | 🟡 No ejercitado a fondo (el prompt solo pide Mes 1; el M1 sí tiene forma correcta) |
| Crawl budget explícito | 🟡 Cubierto funcionalmente vía "gobernanza de indexación", sin nombrar logs/crawl budget |

**Lección RED:** el mecanismo del esqueleto (restricción dominante → dimensiones → núcleo schema) generaliza bien con un agente competente. **Decisión de diseño derivada:** NO apéndices por vertical — basta una tabla compacta de parametrización (`00-parametrizacion-vertical.md`) que fije lo que hoy queda a la improvisación (facetas, eventos por modelo de conversión, forma del roadmap, país), reduciendo varianza entre corridas/modelos.

---

## GREEN (tras crear `00-parametrizacion-vertical.md` + `13-migracion-sitio-existente.md` + des-hardcoding)

Prompts idénticos a RED; agentes frescos.

| Escenario | Resultado | Notas |
|---|---|---|
| migracion-servicios | ✅ **7/7** (RED: 3/7) | Matriz keep/improve/consolidate/kill completa; quick wins striking distance **sobre el sitio viejo** con transferencia por 301; crawl diff como bloqueante; alerta >20%/2 semanas → auditar técnico antes de contenido; fluctuación declarada por escrito. Citó "WhatsApp solo si discovery lo confirma — no se asume" |
| ecommerce | ✅ **9/9** (RED: 7/9) | Facetas con las 3 condiciones de promoción; Consent Mode v2 + LFPDPPP (fila nueva de 07); crawl budget + gates de indexación por lote explícitos; aplicó M0 de migración al detectar tráfico previo |
| saas | ✅ **7/7** (nuevo) | Usó la "fila SaaS de la parametrización" por nombre; comparativas BOFU primero; `SoftwareApplication` con offers EUR; `trial_signup`/`demo_request`; GDPR; cadencia acotada al equipo de 3 |
| local-multisede | ✅ **8/8** (nuevo) | `Restaurant` por sede + `parentOrganization`; reclamar GBP Chía día 1 (verificación lenta); menú HTML + 301 del PDF; reviews por sede; alcance trimestral respetado; UTM en enlaces de cada GBP; es-CO |

**Conclusión:** la generalización por tabla de parametrización + playbook de migración funciona en los 4 rubros. Pendiente de futuras pasadas (ver análisis de huecos en la carpeta del proyecto): SERP reality check (H2), columnas de keyword research (H4), umbrales en gates (F5), KPIs de tráfico AI (H5), runbook de caídas (H8), F1-F4, H6-H7, H9-H12. Correr estos 4 escenarios de nuevo tras cada pasada.

---

## Pasada 2 (tras aplicar los pasos 3-7 del análisis: H2, H4, F5, H5, H8, F1-F4, H6-H7, H9-H12 y menores)

Prompts idénticos; agentes frescos. **4/4 sin regresiones y con los elementos nuevos presentes:**

| Escenario | Elementos nuevos observados |
|---|---|
| migracion-servicios | SERP reality check pre-arquitectura · comparativas BOFU "obligatorio en B2B" · gates con umbral→acción (M3 congelar, M6 ≥50% hubs, M12 kill criteria) · UTM en GBP · segmento GA4 referrals AI · release combinado tratado como anti-patrón con benchmark por sección |
| ecommerce | SERP reality check aplicado (detectó marketplaces dominando el SERP MX → pivote a long-tail/BOFU) · gates con umbrales · branded search como proxy · Bing/IndexNow "prioridad M1" · comparativas · sin sobrepromesa de llms.txt |
| saas | Matiz de medición declarado al cliente ("clics de AI Overviews no segmentables") · mix 40-50/20-30/30 con expectativa impresiones↑/clics↓ en el spec · activo citable `/datos` en Q2 · `ProfilePage` + `dateModified` real · anti-osificación aplicada al calendario normativo |
| local-multisede | SERP reality check con implicación de agregadores ("optimizar presencia EN ellos") · UTM por sede "sin esto el Tier 2.5 queda ciego" · `ProfilePage` del chef · gate M3 con umbral de congelamiento, acotado al alcance trimestral |

**Estado:** los 7 fallas y 12 huecos del análisis 2026-07-08 están aplicados (F1-F7, H1-H12, G1-G7 + menores). El skill queda como referencia general multi-rubro. Estos 4 escenarios son la suite de regresión para cualquier edición futura.
