# 06 · GEO, AI Overviews, llms.txt y E-E-A-T

GEO (Generative Engine Optimization) es **ciudadano de primera clase**, no apéndice. Las AI Overviews ya capturan tráfico — el contenido se diseña para ser citable desde el día 1.

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
User-agent: Bytespider
Allow: /

User-agent: *
Disallow: /admin/
Disallow: /staging/
Disallow: /?s=

Sitemap: {base}/sitemap_index.xml
```
*(Si la marca NO quiere alimentar training data, omitir `Google-Extended`, `Applebot-Extended`, `CCBot`, `GPTBot`. Decisión del cliente.)*

## llms.txt (raíz del sitio)
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
| **Expertise** | Títulos, registro profesional (SENESCYT/MSP/colegio), certificaciones con `ImageObject`; enfoque explicado; `hasCredential` |
| **Authoritativeness** | Membresías y asociaciones, marcas representadas, casos verificables, backlinks de industria, perfil Doctoralia/sectorial |
| **Trustworthiness** | Dirección física visible, registros legales (RUC/SUPERCÍAS), NAP consistente, schema completo, equipo con LinkedIn público, política de privacidad y términos |

**Ancla en personas reales.** Nunca credenciales no verificables.

## Brand mentions off-site
LinkedIn long-form mensual del experto · guest posts en revistas sectoriales · notas de prensa (con permiso del cliente) · speaking en eventos/webinars · Q&A en foros técnicos (Reddit r/PLC, Stack Exchange…) · entidad en **Wikidata**.

## Optimización por plataforma AI
| Plataforma | Vector dominante |
|---|---|
| Google AI Overviews | Schema + autoridad + topical depth + freshness |
| ChatGPT (modelo) | Frecuencia de menciones en training data → LinkedIn + guest posts + foros |
| ChatGPT Search / OAI-SearchBot | Como Google: schema, citability, backlinks |
| Perplexity | Citaciones de fuentes confiables; premia stat claims sourceadas + FAQ extractable |
| Bing Copilot | SEO Bing + Bing Webmaster + IndexNow |
| Claude | Common Crawl + Anthropic web |

## Ética / seguridad del contenido (YMYL — obligatorio)
En páginas de salud/legal/finanzas:
- **Disclaimer visible** (informativo, no sustituye atención profesional/urgencia).
- **Crisis Box** (líneas de emergencia y salud mental) en contenido sensible.
- **Frases prohibidas**: "cura", "garantía", "100%", diagnóstico a distancia, credenciales no verificables.
- Validar antes de instruir; lenguaje claro; CTA sin presión.
