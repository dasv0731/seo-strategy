# Núcleo estratégico de seo-master-plan — lo que NO cubren tus skills/flujos

> Materia prima para el rework. Extraído fielmente de las references de la skill actual,
> dejando FUERA todo lo que ya hacen base-cliente, diseño-secciones, schema-graph,
> interlinking, content-engine, extraccion/seo-vitals, el pipeline de datos
> (seo-setup/seo-sync/seo-analisis/seo-cambios/seo-dashboard) y orquestador-seo.
>
> Regla de corte: se queda la **estrategia y el diseño** (qué y por qué); sale la
> **ejecución y la medición** (cómo se produce y cómo se mide) que ya tiene dueño.

---

## MAPA DE DELEGACIÓN (qué sale y a dónde)

| Sección spec (§0–§14) | Qué queda en master-plan | Qué se delega y a quién |
|---|---|---|
| §0 Panorama | Síntesis estratégica del negocio | Datos de empresa ← **base-cliente** (`contexto-<cliente>.md`) |
| §0.1 Restricción dominante | **Todo** (núcleo) | — |
| §1 Decisiones estratégicas | Alcance, conversión, stack, scope, estado del sitio | Nombre legal/fundación/productos ← **base-cliente** |
| §2 Enfoque de arquitectura | Solo la *decisión de enfoque* condicionada por restricción dominante | Diseño del árbol + SERP reality check ← **arquitectura-seo** |
| §3 URLs y content-types | — | Árbol de URLs ← **arquitectura-seo** |
| §4 Clusters e internal linking | — | Diseño ← **arquitectura-seo** (Fase 7); auditoría del enlazado ← **interlinking** |
| §5 Schemas | Solo qué entidades/anclaje pide la estrategia | Generación/validación JSON-LD ← **schema-graph** |
| §6 Local / GBP | Solo la *línea estratégica* (prioridad/presupuesto) | Ejecución (GBP, NAP, city pages, reviews) ← **local/GBP (nueva)** |
| §7 GEO / AI / E-E-A-T | *Diseño* (anclaje E-E-A-T, reglas de citability) | Auditoría/monitoreo (allowlist, llms.txt, citability, menciones AI) ← **geo-audit (nueva)** |
| §8 Technical | **Requisitos/targets** (render mode, CWV target, IndexNow) | Crawl y medición ← **extraccion / seo-vitals** |
| §9 Keywords y clusters | — | Estudio + clustering ← **arquitectura-seo** (Fases 1-3); quick wins continuos ← **seo-analisis-gsc** |
| §10 Plan de contenido | **Roadmap/cadencia/roles** | Producción de la pieza ← **content-engine** |
| §11 Competitivo + link building | Solo la *línea estratégica* de off-site | Análisis competidor ← **competidores (nueva)**; análisis+adquisición de links ← **off-site (nueva)** |
| §12 KPIs / dashboard / tooling | **Diseño** (jerarquía, gates, runbook, atribución) | Medición y reporte ← pipeline de datos |
| §13 Roadmap / riesgos / supuestos | **Todo** | — |
| §14 Briefs de página (copy) | Solo la lista de páginas del hito | Estructura de secciones + copy ← **diseño-secciones / content-engine** |
| (Fases del plan) | **Todo** (esqueleto de ~15 fases) | Ejecución ← superpowers:executing-plans |
| (Migración) | **Estrategia** (retención, ventanas, riesgo) | Árbol/301/inventario ← **arquitectura-seo** |

---

## A · PARAMETRIZACIÓN POR VERTICAL (§00)  [núcleo, se queda entero]

El esqueleto §0–§14 es el mismo para todo rubro; cambian los **parámetros**. Ubicar el
negocio en una fila e instanciar §0.1, §2-§5, §10, §12.

| Rubro | Restricción dominante típica | Dimensiones de arquitectura | Núcleo schema | Content-types clave | Conversión (eventos) | Forma del año 1 |
|---|---|---|---|---|---|---|
| Servicios B2B/B2C | Normativa demostrable / venta larga | servicios × sectores × ubicaciones | `Organization` | hubs, spokes, casos, blog | `form_submit`, `phone_click`, `whatsapp_click` | foundation → expansión local/sectorial → autoridad → optimización |
| Persona-céntrico / YMYL | E-E-A-T / YMYL | especialidades (hub por problemática) | `Person` | hubs de especialidad, blog firmado | `booking_click`, `whatsapp_click` | igual que servicios, cadencia baja y todo firmado |
| Local multi-sede | Proximidad + reviews por sede | sedes × servicios/carta | `LocalBusiness`/vertical por sede | página por sede, servicios/menú en HTML, blog local | `booking_click`, `phone_click`, GBP | GBP+NAP por sede → páginas de sede → reviews → contenido local |
| E-commerce | Gobernanza de catálogo e indexación a escala | categorías → subcategorías → producto (+ guías) | `Organization`/`OnlineStore` + `Product`/`Offer` | colecciones con copy único, fichas, guías, comparativas | `view_item`, `add_to_cart`, `purchase` | técnica + facetas → colecciones top → guías/soporte → autoridad |
| SaaS | PLG/ciclo de prueba + incumbentes | features × casos × integraciones × comparativas | `Organization` + `SoftwareApplication` | features, use-cases, integraciones, vs/alternativas (BOFU), pricing, glosario | `trial_signup`, `demo_request` | comparativas BOFU → features/use-cases → topical authority → integraciones |
| Publisher / afiliados | E-E-A-T autores + frescura a escala | topics/secciones × formatos | `NewsMediaOrganization` + `Person` autores | artículos, reviews con experiencia real, evergreen | pageviews, clic afiliado, suscripción | taxonomía → autoridad de autores → actualización sistemática |
| Marketplace / directorio / programático | Render + crawl budget + thin a escala | entidad × modificador (data-driven) | `ItemList` + entidad por página | plantillas con datos únicos por página | según modelo | validar render+indexación en muestra → escalar por lotes con gates |

**Si el rubro no está:** derivar la fila con el mecanismo (restricción dominante →
dimensiones → núcleo schema → conversión) y registrarla en el spec.

**Reglas transversales de parametrización:**
1. **País e idioma.** Los ejemplos usan Ecuador (EC, es-EC, SENESCYT/MSP, RUC/SUPERCÍAS,
   LOPDP, Doctoralia): son ejemplos, no defaults. Sustituir por equivalentes del país del
   cliente (ISO país, es-XX, registro profesional local, registros mercantiles, ley de
   datos GDPR/LFPDPPP/LGPD/LOPDP, directorios sectoriales del mercado).
2. **Conversión.** El modelo elegido en discovery propaga a TODO (CTA flotante, eventos
   GA4, mensajes prellenados, hidden fields, KPIs Tier 1). No asumir WhatsApp.
3. **Escala.** Si el inventario indexable proyectado supera ~1.000 URLs, añadir a §8:
   logs/crawl budget, reglas de facetas y paginación, gates de indexación por lote.
4. **Sitio existente.** Si hay tráfico previo, la migración (§13) modifica la Fase 1.

**Mini-regla e-commerce (facetas):** `?color=`, `/sofas-grises` → noindex por defecto. Se
promueve a colección indexable solo con: demanda demostrada (volumen) + copy único +
inventario suficiente. Canonical de facetas → su colección. Paridad estricta `Product`
schema ↔ feed de Merchant Center.

---

## B · DISCOVERY ESTRATÉGICO (§01)  [solo las capas NO-factuales; lo factual es base-cliente]

Filosofía: no todas las preguntas aplican; saltar irrelevantes y registrar por qué.
Sin datos del Nivel 1 no se empieza el spec.

**Se queda (estratégico):**
- **Alcance del entregable** (elegir uno): 1) arquitectura mínima · 2) arquitectura +
  contenido de lanzamiento (mes 1) · 3) estrategia trimestral · 4) estrategia integral 12m.
- **Estado del sitio**: greenfield / básico (rehacer URLs libre) / con tráfico (→ migración §13).
- **Modelo de conversión**: compra / lead / WhatsApp / llamada / booking + ciclo de venta.
- **Modo de renderizado** (¿el contenido crítico se ve sin ejecutar JS?): decide indexabilidad y CWV.
- **Nivel 2 estratégico**: % revenue por segmento de audiencia + buyer personas; cobertura
  geográfica (oficina física vs service area por ubicación); flagship vs secundario,
  estacionalidad, sub-servicios (= spokes); sectores atendidos (= dimensión de arquitectura);
  modelo de precios + USP real.
- **Nivel 4 continuo**: competencia (directos/indirectos/aspiracional); legal/regulatorio
  (clave YMYL); definition of success + decision gates (qué se evalúa a M3/M6/M9).

**Sale a base-cliente (factual):** nombre legal + marca, año/país/ciudad/tamaño equipo,
servicios/productos con detalle, equipo/personas con credenciales, casos/testimonios,
certificaciones, identidad visual, operaciones (horario, canales). El discovery los
**consume** desde `contexto-<cliente>.md`, no los vuelve a preguntar.

---

## C · RESTRICCIÓN DOMINANTE + PRINCIPIOS TRANSVERSALES  [núcleo]

**§0.1 — Restricción dominante (la sección más importante).** Identificar la fuerza que
gobierna TODAS las decisiones y explicar cómo condiciona arquitectura, schema, contenido,
conversión y off-site. Ej.: Inspira → YMYL/E-E-A-T salud; AioTech → cumplimiento normativo
+ ciclo B2B largo; e-commerce → catálogo/inventario; SaaS → product-led + ciclo de prueba.
Sin esto, el plan es plantilla muerta.

**Principios transversales (hacerlos explícitos en cada spec):**
1. Restricción dominante primero (§0.1).
2. Honestidad estructural: nunca `Review`/`AggregateRating` falso ni credenciales no
   verificables; datos pendientes como `XXXX`/`// CONFIRMAR` + checklist de datos privada.
3. GEO/AI como ciudadano de primera clase (integrado al contenido desde día 1).
4. E-E-A-T anclado en personas reales (bios, credenciales con `ImageObject`, `Person`).
5. Validar antes de avanzar: decision gates M3/M6/M9; validación de schema pre-deploy;
   anti-canibalización por intención + medición trimestral GSC.
6. Spec primero (estratégico/estable), planes ejecutables después (operativos).
7. Separar informacional (blog) de transaccional (hubs); el blog enlaza a su hub y no lo diluye.
8. Un predicado de cierre por fase (un criterio "Hecho" inspeccionable, no lista difusa).
9. Modo de renderizado = costura transversal: indexabilidad y rendimiento lo heredan a la
   vez; decidirlo en discovery. Letal en arquitecturas a escala (verificar render antes de escalar).
10. Criterios con fecha de caducidad (anti-osificación): todo juicio SERP-dependiente lleva
    condición de re-revisión; en cada gate revisar ≥1 criterio y preguntar "¿sigue vigente?".

**Anti-patrones:** saltarse discovery/restricción dominante → plan genérico · copiar la
matriz cruzada de AioTech a un negocio pequeño → thin/canibalización/penalización · markup
falso o credenciales inventadas → violación de guidelines · GEO como apéndice · spec sin
planes ejecutables / sin Self-Review · abrir spokes sin volumen/contenido único.

---

## D · ESQUELETO DEL DESIGN SPEC (§02)  [núcleo — el orden conceptual se conserva]

Frontmatter: `title / date / status:draft / owner / phase:design-spec`.
Output: `docs/superpowers/specs/YYYY-MM-DD-{cliente}-seo-design.md`.

Secciones (numeración flexible; omitir las que no apliquen y registrar por qué):
§0 Panorama · §0.1 Restricción dominante · §1 Decisiones estratégicas (tabla decisión|valor)
· §2 Enfoque de arquitectura · §3 URLs y content-types · §4 Clusters e internal linking
· §5 Schemas · §6 Local/GBP · §7 GEO/AI/E-E-A-T · §8 Technical · §9 Keywords y clusters
· §10 Plan de contenido 12m · §11 Competitivo y link building · §12 KPIs/dashboard/tooling
· §13 Roadmap/riesgos/supuestos · §14 Briefs de página. Apéndices A (páginas fuera del hito)
y B (glosario).

Orden conceptual (se mantiene): panorama → restricción → decisiones → arquitectura → schema
→ local → GEO → técnico → keywords → contenido → competencia → KPIs → roadmap → briefs.

**Spec self-review (antes de pasar a planes):** 1) placeholders → `// CONFIRMAR` + checklist
· 2) consistencia interna (¿secciones que se contradicen?) · 3) scope (¿enfocado para un set
de planes?) · 4) ambigüedad (elegir una interpretación y hacerla explícita).

---

## E · ENFOQUE DE ARQUITECTURA (§2/§3)  [MIGRA → arquitectura-seo; master-plan solo elige el *enfoque* condicionado por la restricción dominante. Este contenido = materia prima para construir arquitectura-seo]

**Elegir enfoque (documentar elegido + descartados + trade-off):**
| Enfoque | Cuándo | Riesgo |
|---|---|---|
| Servicio-first `/servicios/[slug]` hub→spokes | mono-audiencia, pocos servicios | limitado si hay sectores/ubicaciones fuertes |
| Sector-first `/sectores/[slug]` | la industria guía la decisión | diluye keywords de servicio |
| Matriz cruzada (servicios×sectores×ubicaciones+casos) | audiencia mixta + multi-ubicación + 12m + recursos 2-3× contenido | canibalización sin disciplina de canónicas |
| Especialidad-first (hub por problemática, `Person`) | profesional/equipo pequeño, YMYL, 1 sede | — (el seguro por defecto) |

Regla de oro: elegir por **tamaño y recursos reales**. Copiar la matriz a un negocio pequeño
→ thin + canibalización (grave en YMYL).

**SERP reality check (obligatorio ANTES de fijar el enfoque):** para las 5-10 keywords
flagship, ver qué TIPO de página domina el top 10 (service page / directorio-marketplace /
guía / comparativa / local pack / e-commerce). Si lo dominan directorios → una service page
no rankeará: cambiar la apuesta (long-tail, local, comparativas) o competir dentro de esos
agregadores. Registrar tipo dominante por keyword + implicación aceptada. Juicio que caduca
(re-revisar en cada gate). En vivo: vía orquestador-seo (seo-sxo, seo-dataforseo).

**Reglas de slug:** minúsculas · sin diacríticos · guión · sin stopwords · sin `.html` ·
trailing slash consistente por 301 · sin-www + HTTPS por 301.

**Content-types (universal, no por CMS):** cada dimensión = un content-type con hub overview
+ jerarquía `/[tipo]/[hub-slug]/[spoke-slug]`. Dimensiones canónicas: Servicios
(transaccional) · Sectores (por audiencia) · Ubicaciones (local) · Casos (E-E-A-T
transversal) · Blog (pillar+clusters) · Comparativas/alternativas (BOFU; obligatorio evaluar
en B2B y SaaS; el que mejor sobrevive a AI Overviews).

**Reglas canónicas:** canonical auto-referente por content-type · taxonomías de filtro →
noindex salvo copy curado único · paginación → canonical a sí misma (sin rel prev/next) ·
trailing slash consistente.

**Separación informacional ↔ transaccional:** las queries informacionales viven en el blog
(pillar+clusters) y enlazan obligatoriamente a su hub comercial; los hubs no se diluyen.

**Bilingüe/multi-región (solo si discovery Nivel 1):** subdirectorios `/en/` (default) >
subdominios > ccTLDs · hreflang recíproco + auto-referente + `x-default` · abrir un idioma
solo si habrá contenido completo y mantenido · auditoría → claude-seo:seo-hreflang.

---

## F · INTERNAL LINKING (§4)  [DISEÑO MIGRA → arquitectura-seo (Fase 7); la AUDITORÍA de lo construido = interlinking]

- Topología hub-and-spoke en capas: Home → hubs de cada dimensión → spokes; casos cruzan
  transversalmente.
- Toda página crítica ≤ 3 clics desde Home. Footer global expone hubs principales.
- Breadcrumbs en todas (excepto Home) con `BreadcrumbList` JSON-LD.

**Anti-canibalización (tabla por conflicto):**
| Conflicto | Página canónica | La otra enlaza con anchor |
|---|---|---|
| `[servicio] + [ciudad]` | `/ubicaciones/[ciudad]` | "cobertura en [ciudad]" |
| `[servicio] + [sector]` | `/sectores/[sector]` | "aplicaciones en [sector]" |
| `[servicio]` genérico | `/servicios/[slug]` (hub) | — |
| `[ciudad] + [servicio específico]` low-vol | `/servicios/[slug]` | mencionar ciudad sin H1 dedicado |
Resolución: por mayor intent local/sectorial + medición trimestral GSC (si la secundaria gana
impresiones por la query → redirigir canonical).

**Bloques reutilizables:** servicios/áreas relacionados · sectores/para quién · cobertura ·
casos similares · recursos del blog · CTA "hablemos/agenda" · bloque de autoría (`Person`) en
contenido clínico/técnico.

**Mix de anchor interno:** exact-match 10-15% · partial-match 40-50% · branded 15-20% ·
generic 10-15% · naked URL 5-10%.

> Nota de handoff: master-plan **declara** esta topología en `estrategia.yaml` (formato de
> interlinking); interlinking la **verifica** contra el crawl real.

---

## G · LOCAL SEO Y GBP (§6)  [EJECUCIÓN MIGRA → skill local/GBP (nueva); master-plan solo la línea estratégica. Materia prima para esa skill]

**Principio rector:** una sola oficina física → un GBP completo; las demás ciudades son
service area, NO sedes (falsear ubicaciones = suspensión permanente). 100% online/1 sede →
capa local ligera (GBP + 1-2 páginas de modalidad).

**Config GBP:** nombre exacto = NAP · categoría primaria la más específica · hasta 9
secundarias · service area (ciudades + país si hay online) · fijo + WhatsApp Business · URL
canónica **con UTM** (`?utm_source=gbp&utm_medium=organic`) · horario por día · atributos ·
lista de servicios+spokes. Operativa: posts ≥1/sem enlazando a URL del sitio (imagen 1200×900);
Q&A pre-poblado 8-15 desde la cuenta de la empresa.

**Página por ciudad (8 bloques):** hero localizado+breadcrumb+CTA · intro 200-300 palabras
únicas · servicios en [Ciudad] (cards) · casos en [Ciudad] · sectores en [Ciudad] · mapa
estático (no embed) · FAQ de la ciudad (4-6) · CTA final.

**NAP consistency (auditoría Mes 1):** NAP canónico idéntico en GBP · web (footer+contacto) ·
schema `LocalBusiness` · Bing Places · Apple Maps · directorios · LinkedIn/FB/IG · cámaras ·
OpenStreetMap · (salud: Doctoralia).

**Reviews:** solicitud post-proyecto con link directo `g.page/r/[id]/review` · metas ~5(M1-3)
→15(M6)→30+(año1) · responder TODAS ≤48h · 4★+ render en Home · nunca presionar/incentivar ·
YMYL: responder sin revelar que es paciente.

---

## H · GEO, AI OVERVIEWS, LLMS.TXT Y E-E-A-T (§7)  [DISEÑO se queda (anclaje E-E-A-T, citability en contenido); MONITOREO MIGRA → geo-audit (nueva). El archivo que más caduca]

Jerarquía de palancas por evidencia: **citability + E-E-A-T + schema** (fuerte) >
Bing/IndexNow (barata) > llms.txt (especulativa).

**robots.txt — allowlist de crawlers AI:** Googlebot, GPTBot, ChatGPT-User, OAI-SearchBot,
ClaudeBot, anthropic-ai, PerplexityBot, Google-Extended, Applebot-Extended, CCBot → Allow.
`Disallow: /admin/ /staging/ /?s=`. Si la marca NO quiere alimentar training data → omitir
Google-Extended/Applebot-Extended/CCBot/GPTBot. `Bytespider` fuera del default.

**llms.txt (opcional, 10 min, cero riesgo, no desplaza a las palancas con evidencia):** H1
marca + blockquote 2-4 líneas + secciones de links con descripción de una línea. `llms-full.txt`
fase 2. Check mensual 200 OK.

**Citability passage-level (obligatorio en servicio/sector/blog clínico):** TL;DR primer
párrafo 40-60 palabras (definición + dato clave + audiencia) · patrón definición→elaboración
· FAQ con pregunta en H3 + respuesta directa en 1ª oración · stat claims con fuente ·
tablas comparativas extractables · listas numeradas para how-to · auto-suficiencia por
párrafo · glosario técnico (fase posterior).

**E-E-A-T — 4 pilares → acciones:** Experience (bios con años, casos con fecha/lugar/problema,
fotos reales) · Expertise (títulos, registro profesional del país, certificaciones con
`ImageObject`, `hasCredential`) · Authoritativeness (membresías, marcas representadas, casos
verificables, backlinks de industria, directorio sectorial) · Trustworthiness (dirección
física, registros legales del país, NAP consistente, schema completo, LinkedIn público,
privacidad y términos). Anclar en personas reales; nunca credenciales no verificables.

**Activos citables con datos originales (imán #1 de links y citas AI):** página `/datos/` o
`/estadisticas-[sector]/` con 10-20 stats propias/curadas, actualizada anualmente con
changelog. Cada stat = cifra + fuente + fecha. Planificar en Q2 como táctica nombrada.

**Brand mentions off-site:** LinkedIn long-form mensual del experto · guest posts en revistas
sectoriales · notas de prensa (con permiso) · speaking · Q&A en foros técnicos · entidad en
Wikidata.

**Optimización por plataforma:** AI Overviews → schema+autoridad+topical depth+freshness ·
ChatGPT (modelo) → frecuencia de menciones (LinkedIn+guest+foros) · ChatGPT Search →
OAI-SearchBot + Bing (schema, citability, backlinks, Bing Webmaster+IndexNow) · Perplexity →
stat claims sourceadas + FAQ · Bing Copilot → SEO Bing + Webmaster + IndexNow · Claude →
Common Crawl + Anthropic web. **Palanca barata:** Bing Webmaster + IndexNow activar en M1.

**Ética/seguridad YMYL (obligatorio):** disclaimer visible · Crisis Box (líneas de
emergencia) · frases prohibidas ("cura", "garantía", "100%", diagnóstico a distancia,
credenciales no verificables) · validar antes de instruir; CTA sin presión.

---

## I · REQUISITOS TÉCNICOS (§8)  [solo targets/decisiones; el crawl y la medición son extraccion/seo-vitals]

Se queda como **requisito declarado en el spec** (no como ejecución):
- **Modo de renderizado** decidido en discovery y declarado explícito (SSR/estático/CSR/híbrido).
- **CWV targets:** passing 80%+ mobile (LCP/INP/CLS). Schema válido 100%. HTTPS 100%.
- **Foundation files:** robots.txt (allowlist AI de §7), llms.txt, sitemap live.
- **IndexNow + Bing Webmaster:** activar en M1 (palanca GEO barata).
- **Escala >~1.000 URLs:** logs/crawl budget, reglas de facetas/paginación, gates de
  indexación por lote antes de escalar.

> La medición real (CWV, crawl, issues) la hacen extraccion + seo-vitals; §8 solo fija el objetivo.

---

## J · KEYWORD RESEARCH Y CLUSTERS (§9)  [MIGRA → arquitectura-seo (Fases 1-3, es su corazón); quick wins continuos = seo-analisis-gsc]

- Metodología: un cluster por servicio flagship + secundarios + sectores + ubicaciones.
- Tabla de total de páginas indexables año 1 (para dimensionar scope y detectar riesgo de thin).
- Clustering por solapamiento de intención (no similitud textual).

> El análisis continuo (quick wins pos. 5-15, canibalización, marca vs no-marca) es de
> seo-analisis-gsc sobre seo.db. §9 hace el mapa inicial que alimenta el roadmap.

---

## K · PLAN DE CONTENIDO 12 MESES (§10)  [planificación; la producción es content-engine]

- Modelo de producción + roles + horas.
- Roadmap trimestral + cadencia + plantillas de longitud por tipo.
- Promoción cross-channel.

> La redacción de cada pieza (con fact-check/EEAT real) es de content-engine; la estructura
> de secciones de cada página es de diseño-secciones. §10 planifica QUÉ y CUÁNDO, no redacta.

---

## L · ANÁLISIS COMPETITIVO Y LINK BUILDING (§11)  [Análisis competidor MIGRA → competidores (nueva); link building MIGRA → off-site (nueva, 2 módulos: analiza+construye); master-plan solo la línea estratégica. Materia prima para ambas]

**Tipología por tier:** T1 multinacionales (no competir de frente; partnership/certificación)
· T2 firmas locales (competir gap por gap con profundidad+frescura+GEO) · T3 nicho (copy
técnico + casos verticales) · T4 freelancers (solo queries genéricas) · Aspiracional (benchmark).

**Auditoría competitiva (M1-2, 8-10 nombres T2-3):** dominio, DR, # páginas indexadas, top10
pages/keywords, tráfico estimado, schema, GBP+reviews, LCP, cobertura servicios/sectores/
ubicaciones, cadencia, backlinks (# ref domains + top10 + anchors), **gaps**.

**Link building 12m:** Foundation Q1-Q2 (directorios/citations, perfiles, asociaciones) ·
Content-driven Q2-Q3 (guest posts, pillars, datos originales) · Outreach Q3-Q4 (sitios que ya
enlazan a competidores; sobre piezas que ya performan en GSC) · PR (notas de prensa, speaking).

**Anchor externo saludable:** predominio branded + naked URL; exact-match <5-10%.

**Outreach:** email 3-4 líneas value-first, personalizado, seguir 1×/semana. Desconfiar de
links "garantizados" <$100 (granjas → disavow).

**Re-auditoría ligada a gates:** re-auditar T2-3 en cada gate (M3/M6/M9).

---

## M · KPIs, DECISION GATES Y RUNBOOK (§12)  [diseño; la medición es el pipeline de datos]

**Jerarquía 3 tiers:** T1 Business outcomes (leads, calificados, revenue atribuido) · T2 SEO
outcomes (tráfico orgánico, rankings, visibility GSC; T2.5 local: map pack, GBP, reviews) ·
T3 Leading indicators (contenido publicado, ref domains, salud técnica, GEO/AI). Cada KPI con
proyección Q1→Q4. Targets permanentes: CWV 80%+, schema 100%, HTTPS 100%.

**GEO/AI como KPI propio:** segmento GA4 de referrals AI (chatgpt/perplexity/gemini/copilot)
— OJO: los clics de AI Overviews llegan como Google orgánico y NO son segmentables. Búsqueda
branded en GSC como proxy de autoridad. Brand mentions en AI (check mensual). llms.txt 200 OK.

**Atribución (estructural, sin esto no hay T1):** UTMs en todo link · GA4 custom dimensions ·
hidden fields en forms · WhatsApp con UTM · CRM con pipeline.

**Decision gates (umbral → acción; un gate sin umbral es una reunión):**
- **M3** baseline (no exigir resultados). Umbrales técnicos: indexación = exactamente el árbol
  designado, CWV 80%+, schema 100%. Si falla → congelar contenido nuevo hasta resolver.
- **M6** ¿≥50% de hubs con impresiones crecientes (3m)? Sí → abrir spokes/facetas. No →
  congelar y auditar indexación/calidad/tipo-de-SERP. Canibalización → redirigir canonical.
- **M9** ¿ref domains y branded creciendo vs M6? Sí → duplicar lo que funciona (outreach sobre
  top). No → reasignar horas a promoción/refresh.
- **M12** cierre + plan año 2. Kill criteria honesto: cluster sin impresiones tras 9m con
  técnica sana → replantear la apuesta, no insistir.
En cada gate re-revisar ≥1 criterio SERP-dependiente (principio 10).

**Runbook ante caída (ANTES de optimizar nada; la causa casi siempre está arriba):**
1) Técnico (noindex/robots accidental, cobertura GSC, 404s, deploy reciente) · 2) Acción
manual/seguridad (GSC) · 3) Core update (si coincide → no tocar reactivamente) · 4) Cambio de
layout SERP (AI Overview/local pack: impresiones estables + clics abajo = pérdida de CTR) ·
5) Estacionalidad (YoY no MoM) · 6) Competencia. Regla: caída sin causa identificada NO se
"optimiza" reescribiendo — se diagnostica.

**Cadencia de reporting:** semanal 15min (anomalías) · mensual 1h (2 págs) · trimestral 1día
(ejecutivo 5-7 págs + gate) · anual (plan año 2).

> Tooling y dashboard reales, alertas y veredictos antes/después: pipeline de datos
> (seo-sync/seo-analisis/seo-cambios/seo-dashboard). §12 diseña la jerarquía y los umbrales.

---

## N · ROADMAP CONSOLIDADO, RIESGOS Y SUPUESTOS (§13)  [núcleo]

Recursos (hrs/semana) · presupuesto año 1 (usar costos orientativos de §11) · supuestos
críticos · riesgos + mitigaciones · out of scope · definition of success · decision gates.

---

## O · FASES DEL PLAN + MIGRACIÓN  [núcleo]

### Esqueleto de ~15 fases (genéricas, reordenables según stack)
Output: `docs/superpowers/plans/YYYY-MM-DD-{cliente}-seo-mesN-plan.md`. Header: Goal ·
Architecture · Tech Stack (con costos) · File Structure. Jerarquía Fase N → Tarea N.M → Paso;
cada tarea cierra con validación + commit.

**Fase 0 (BLOQUEANTE):** checklist de datos privada, datos críticos por fase, confirmar
dominio (whois), validar credenciales reales (YMYL), confirmar compromisos operativos.

1 Infraestructura · 2 Hardening + módulos core · 3 Stack SEO · 4 Schemas custom (JSON-LD por
content-type) · 5 Builder + templates + componentes (bloques de linking) · 6 Performance ·
7 Forms + conversión · 8 Tracking + Analytics · 9 Foundation files (robots/llms/sitemap) ·
10 Páginas del hito (copy+menús+legales) · 11 GBP setup · 12 NAP citations top 5 · 13
Pre-launch (validación schema/perf/mobile/links/forms/robots) · 14 Launch (sitemap+IndexNow+
solicitar indexación) · 15 Post-launch monitoring (semana 1 diario).

**Self-Review (OBLIGATORIO):** tabla que mapea cada §1-§14 del spec → fase(s) que la cubren.
**Definition of Done del hito:** producción HTTPS/sin-www/headers · core indexable con schema
válido · grafo JSON-LD sin errores · GBP en verificación + NAP · GSC+Bing+GA4+sitemap+eventos
· robots+llms · CWV target mobile · (YMYL: disclaimers+datos) · content-types listos.

### Migración / sitio existente (§13) — modifica la Fase 1
**Regla cero:** KPI de migración = **retención, no crecimiento** (≥90-95% de clics a semana
6-8). Declarar por escrito la fluctuación esperada (2-6 semanas de baile). No combinar en un
release cambio de dominio + reestructura URLs + rediseño + reescritura.

**Variante sin rediseño (retainer de optimización):** aplican solo M0 (inventario+benchmark),
matriz keep/improve/consolidate/kill y quick wins; omitir 301 masivo y crawl diff. KPI =
crecimiento vs benchmark.

**M0 — Inventario + benchmark (ANTES de diseñar la arquitectura):** inventario por URL con 12-16
meses (clics/impresiones/posición GSC, sesiones/conversiones GA4, backlinks por URL, crawl
completo). Benchmark congelado pre-migración (top 50-100 queries, tráfico por sección, #
indexadas, CWV) — bloqueante.

**Matriz keep/improve/consolidate/kill (por URL, con umbrales):** Keep (clics/conversiones/
backlinks → migrar 1:1) · Improve (impresiones sin clics, pos. 5-15 → migrar + rewrite) ·
Consolidate (varias thin del mismo tema → fusionar + 301) · Kill (0 clics + 0 backlinks + 0
valor 12m → 410, o 301 al padre si tiene backlink). Cada URL recibe una decisión.

**Quick wins M1-M2 (mejor ROI del año):** striking distance (pos. 5-15 → rewrite title/meta,
reforzar internos desde hubs, completar contra top 3); si la migración tarda >4-6 sem,
ejecutar sobre el sitio viejo (el equity se transfiere por los 301).

**Mapa 301:** 1:1 vieja→nueva, nunca todo a Home (soft-404), máx 1 salto; cubrir variantes
(parámetros, mayúsculas, trailing slash, http, www); kill con backlinks → 301 al padre; mapa
versionado ≥12 meses.

**Pre-switch (bloqueante):** crawl diff staging vs producción (URLs, titles, canonicals,
robots, schema, status); cualquier diferencia no explicada bloquea launch.

**Switch + monitoreo:** Día 0 (301 activos + verificación, submit sitemap nuevo manteniendo el
viejo 2-4 sem, IndexNow, indexación top en GSC) · Días 1-14 diario (404s, cobertura, redirects,
top queries) · Semanas 2-8 semanal (retención vs benchmark, top 50, ref domains). Alerta:
caída >20% sostenida 2+ semanas → auditar 301/indexación/render antes de tocar contenido.

---

## DECISIONES CONSOLIDADAS (2026-07-13)

master-plan se reenfoca a **espina estratégica + gobernanza + ensamblaje**. Todo lo operativo
se delega a skills dedicadas. **master-plan se construye AL FINAL** (es el integrador que
consume las salidas de las demás).

**Criterio skill-vs-módulo (afilado):** skill dedicada si cumple las 3 → (a) usa inputs propios
que master-plan no tiene · (b) produce su propio doc/entregable separable · (c) se invoca con
cadencia propia. Si solo pasa una vez al escribir la estrategia y no produce artefacto
separable → módulo en master-plan.

**Lo que le queda a master-plan (residual):** restricción dominante + parametrización por
vertical + 10 principios · discovery estratégico (scope/conversión/render mode/gates) · diseño
de KPIs/gates/runbook · estrategia de migración (retención/ventanas/riesgo, NO el 301) ·
roadmap de contenido (calendario/roles, NO la redacción) · goals técnicos (§8) · la *línea
estratégica* de local/off-site/GEO · el Design Spec §0–§14 + los planes por fase que ensamblan
todas las salidas.

---

## SKILLS A CREAR (lo que falta antes de rehacer master-plan)

| # | Skill nueva | Estado | Absorbe del núcleo | Depende de |
|---|---|---|---|---|
| 1 | **arquitectura-seo** | **Spec listo** (aprobado en diseño), sin construir | §2, §3, §4 diseño, §9, parte de migración (301/inventario) — secs. E, F, J | base-cliente, conexiones, keywords |
| 2 | **competidores** | Prevista en spec de arquitectura-seo, sin spec propio | parte de §11 (análisis competidor) — sec. L | extraccion (crawl) |
| 3 | **off-site / link building** | Idea, sin spec (1 skill, 2 módulos: analiza + construye) | resto de §11 — sec. L | competidores (gaps), (seo-backlinks) |
| 4 | **geo-audit** | **✅ Hecha** — v1 mergeada e instalada 2026-07-13 (spec+plan en `Nuevas skills\GEO Audit\docs\superpowers\`; v2 diseñada en spec §17) | monitoreo de §7 (allowlist, llms.txt, citability, menciones AI) — sec. H | crawl / respuestas AI |
| 5 | **local / GBP** | Idea, sin spec (solo si hay clientes locales) | ejecución de §6 — sec. G | — |
| 6 | **seo-master-plan (rework)** | Este núcleo extraído; **se hace AL FINAL** | — (integra a las 5 de arriba) | consume 1-5 |

**Orden de construcción sugerido (por dependencias):**
1. arquitectura-seo (spec listo, desbloquea el resto) → 2. competidores → 3. off-site →
4. ~~geo-audit~~ ✅ (hecha 2026-07-13, fuera de orden) → 5. local/GBP (condicional) →
6. rework de master-plan (integrador, al final). **Siguiente: construir arquitectura-seo.**

---

## PENDIENTES PARA EL BRAINSTORM (de master-plan, no resolver aún)
- ¿Handoffs como contratos de archivo? (`contexto-<cliente>.md` → discovery; árbol de
  arquitectura-seo → spec; `estrategia.yaml` para interlinking).
- ¿El Design Spec sigue siendo un solo doc §0–§14 o se parte apuntando a cada skill?
- ¿master-plan produce `estrategia.yaml` (lo que interlinking espera) como salida canónica?
- Off-site: decidido = 1 skill con 2 módulos; ¿su módulo "analiza" propio vs depender de la
  externa `claude-seo:seo-backlinks`?
- Frontera master-plan ↔ orquestador-seo: master-plan = artefacto (spec+planes); orquestador =
  runtime que invoca.
