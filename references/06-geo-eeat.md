# 06 · GEO, AI Overviews, llms.txt y E-E-A-T

> **Última revisión de crawlers/plataformas: 2026-07.** Este es el archivo que más rápido caduca del skill: revisar la allowlist y la tabla de plataformas en cada decision gate (principio 10) y actualizar esta fecha al hacerlo.

GEO (Generative Engine Optimization) es **ciudadano de primera clase**, no apéndice. Las AI Overviews ya capturan tráfico — el contenido se diseña para ser citable desde el día 1. Jerarquía de palancas por evidencia: **citability + E-E-A-T + schema** (evidencia fuerte) > Bing/IndexNow (barata y accionable) > llms.txt (apuesta especulativa).

## robots.txt — allowlist de crawlers AI
```
User-agent: Googlebot
Allow: /

User-agent: GPTBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: CCBot
Allow: /

User-agent: *
Disallow: /admin/
Disallow: /staging/
Disallow: /?s=

Sitemap: {base}/sitemap_index.xml
```
*(Si la marca NO quiere alimentar training data, omitir `Google-Extended`, `Applebot-Extended`, `CCBot`, `GPTBot`. Decisión del cliente. `Bytespider` (ByteDance/TikTok) queda **fuera del default**: agresivo, suele ignorar robots.txt y no devuelve tráfico de búsqueda — añadirlo solo si el cliente quiere presencia en ese ecosistema.)*

## llms.txt (apuesta especulativa de bajo costo — opcional)
Google confirmó públicamente que **no lo usa** y ninguna plataforma AI mayor ha confirmado consumirlo. Son 10 minutos y cero riesgo: se hace, pero **no desplaza a las palancas con evidencia** (citability, E-E-A-T, schema) ni se le prometen resultados al cliente.
Formato markdown: H1 marca + blockquote descriptivo (2-4 líneas) + secciones de links con **una descripción de una línea por enlace**.
```markdown
# {Marca}

> {Descripción de 2-4 líneas: qué hace, dónde, especialidades.}

## Servicios / Áreas
- [Nombre](url): descripción de una línea.

## Cobertura / Modalidad
- [Ciudad/Online](url)

## Empresa / Profesional
- [Equipo / Sobre](url)

## Optional
- [Blog](url)
```
`llms-full.txt` (contenido extendido) opcional fase 2. Check mensual de que devuelve 200 OK.

## Citability passage-level (reglas de contenido)
Obligatorias en cada página de servicio/sector/blog clínico:
- **TL;DR primer párrafo (40-60 palabras)**: definición + 1 dato clave + audiencia.
- Patrón **definición → elaboración**: `X es Y. Funciona así: ...`.
- **FAQ con pregunta en H3 + respuesta directa en la primera oración**.
- **Stat claims con fuente citada**: "Según {norma/fuente}, ...".
- **Tablas comparativas** extractables.
- **Listas numeradas** para how-to.
- **Auto-suficiencia por párrafo** (extractable sin contexto).
- Glosario técnico (fase posterior).

## E-E-A-T — los 4 pilares mapeados a acciones
| Pilar | Implementación concreta |
|---|---|
| **Experience** | Bios con años de campo/práctica; casos con fecha, ubicación, problema real; fotos reales en proyectos/consultorio |
| **Expertise** | Títulos, registro profesional del país (p.ej. SENESCYT/MSP en EC, cédula profesional en MX, colegiado en ES), certificaciones con `ImageObject`; enfoque explicado; `hasCredential` |
| **Authoritativeness** | Membresías y asociaciones, marcas representadas, casos verificables, backlinks de industria, perfil en el directorio sectorial del mercado (p.ej. Doctoralia en salud) |
| **Trustworthiness** | Dirección física visible, registros legales del país (p.ej. RUC/SUPERCÍAS en EC), NAP consistente, schema completo, equipo con LinkedIn público, política de privacidad y términos |

**Ancla en personas reales.** Nunca credenciales no verificables.

## Activos citables con datos originales (imán #1 de links Y de citas AI)
Una página `/datos/` (o `/estadisticas-[sector]/`) con 10-20 stats propias o curadas del sector, **actualizada anualmente** con changelog visible: es el activo que más backlinks naturales atrae y el que Perplexity/AI Overviews citan con más frecuencia. Fuentes: datos operativos propios anonimizados, mini-encuestas a clientes, agregación de fuentes oficiales con análisis propio. Formato: cada stat = cifra + fuente + fecha. Planificarla en Q2 como táctica nombrada, no como extra del link building.

## Brand mentions off-site
LinkedIn long-form mensual del experto · guest posts en revistas sectoriales · notas de prensa (con permiso del cliente) · speaking en eventos/webinars · Q&A en foros técnicos (Reddit r/PLC, Stack Exchange…) · entidad en **Wikidata**.

## Optimización por plataforma AI
| Plataforma | Vector dominante |
|---|---|
| Google AI Overviews | Schema + autoridad + topical depth + freshness |
| ChatGPT (modelo) | Frecuencia de menciones en training data → LinkedIn + guest posts + foros |
| ChatGPT Search / OAI-SearchBot | Crawl propio (OAI-SearchBot) + grounding parcial vía Bing → schema, citability, backlinks **y** Bing Webmaster + IndexNow |
| Perplexity | Citaciones de fuentes confiables; premia stat claims sourceadas + FAQ extractable |
| Bing Copilot | SEO Bing + Bing Webmaster + IndexNow |
| Claude | Common Crawl + Anthropic web |

**Palanca barata que suele olvidarse:** Bing Webmaster + IndexNow (setup en `07`) alimentan Copilot y parte del grounding de ChatGPT Search — activar en M1 como acción prioritaria, no como extra.

## Ética / seguridad del contenido (YMYL — obligatorio)
En páginas de salud/legal/finanzas:
- **Disclaimer visible** (informativo, no sustituye atención profesional/urgencia).
- **Crisis Box** (líneas de emergencia y salud mental) en contenido sensible.
- **Frases prohibidas**: "cura", "garantía", "100%", diagnóstico a distancia, credenciales no verificables.
- Validar antes de instruir; lenguaje claro; CTA sin presión.
