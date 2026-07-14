# 01 · Discovery — framing del engagement

El discovery es la fase **FRAMING** de seo-master-plan (ver `references/00b-flujo-y-contratos.md`): razona el panorama y las decisiones estratégicas **antes** de arquitectura-seo, y produce el handoff `enfoque.md` + el discovery doc. **No escribe el spec** — eso es el ENSAMBLAJE posterior.

Filosofía: no todas las preguntas aplican a todo negocio — salta las irrelevantes y **registra por qué** las saltaste.

> **Factual vs estratégico.** El intake FACTUAL (nombre legal, fundación, productos/servicios, personas/credenciales, casos, certificaciones) **no se re-pregunta**: se lee de `base\contexto-<slug>.md` (skill base-cliente) — solo se confirma y se rellenan huecos. Las preguntas **ESTRATÉGICAS** (alcance, modelo de conversión, render mode, estado del sitio, decision gates) sí son intake directo del framing. Si falta `contexto-<slug>.md`, se entrevista como fallback y se sugiere correr base-cliente (no bloquea).

Output: dos artefactos (ver **Salida del framing** al final) — el discovery doc y `enfoque.md`.

---

## Nivel 1 — Fundacionales (BLOQUEANTES)

> Los datos FACTUALES de abajo (nombre legal, fundación) **NO se re-preguntan**: se leen de `base\contexto-<slug>.md` (base-cliente). Solo confirmar/rellenar huecos. Las preguntas marcadas **ESTRATÉGICAS** son intake directo del framing.

| Pregunta | Por qué importa |
|---|---|
| Nombre legal + marca comercial · *de base\contexto-\<slug\>.md* | NAP, schema, GBP |
| Año de fundación, país, ciudad sede, tamaño de equipo · *de base\contexto-\<slug\>.md* | Organization schema, E-E-A-T |
| Modelo de negocio en una frase · *de base-cliente; confirmar* | Define todo el enfoque |
| **ESTRATÉGICA** — Dominio: ¿confirmado / disponible / WHOIS / quién tiene acceso? | Bloqueante técnico |
| **ESTRATÉGICA** — **Estado del sitio**: greenfield / básico (rehacer URLs libre) / con tráfico (requiere migración con 301 → `references/13-migracion-sitio-existente.md`). *Este campo ramifica todo el escenario (ver más abajo y `references/00b-flujo-y-contratos.md`): greenfield/básico → Escenario B (foundation); con-tráfico → Escenario A (migración, con diagnóstico previo que master CONSUME).* | Cambia el plan de Fase 1 por completo |
| **ESTRATÉGICA** — Render mode: SSR / SSG / CSR / híbrido | Indexabilidad, crawl budget |
| Idioma: único / bilingüe / selectivo | Hreflang, arquitectura |
| **ESTRATÉGICA** — **Modelo de conversión**: compra / lead / WhatsApp / llamada / booking + ciclo de venta | CTAs, tracking, atribución; va a `enfoque.md` |
| **ESTRATÉGICA** — Alcance del entregable (ver escala abajo) + plazo | Tamaño del spec |

**Escala de alcance** (elegir uno):
1. Arquitectura mínima (URLs + schema + technical baseline).
2. Arquitectura + contenido de lanzamiento (mes 1).
3. Estrategia trimestral (3 meses).
4. **Estrategia integral 12 meses** (lo que cubren AioTech e Inspira).

---

## Nivel 2 — Estratégicas (definen la arquitectura)

- **Audiencia primaria**: B2B (enterprise / mid / SMB) · B2C (premium / mass) · B2G · mixto. Pedir **% de revenue** por segmento + buyer personas.
- **Cobertura geográfica**: ciudad / región / país / multinacional. **Crítico**: por cada ubicación, ¿oficina física o solo service area? → decide schema/GBP y si hay arquitectura de ubicaciones.
- **Servicios/productos**: el catálogo (nombres, descripciones, sub-servicios) **se lee de `base\contexto-<slug>.md`, no se re-pregunta**. El framing solo añade el juicio estratégico por cada uno → audiencia, ticket, margen, flagship vs complementario, estacionalidad, **sub-servicios (= spokes)**.
- **Sectores/industrias atendidas** (si aplica → dimensión de arquitectura). *Los sectores factuales de base-cliente; aquí se decide si son dimensión de arquitectura.*
- **Modelo de precios y USP** (diferenciador real, no marketing).

---

## Nivel 3 — Operativas (afinan implementación)

> Los datos FACTUALES de abajo (branding, personas/credenciales, casos, certificaciones, contacto/horario) **NO se re-preguntan**: se leen de `base\contexto-<slug>.md` (base-cliente). Solo confirmar/rellenar huecos.

- **ESTRATÉGICA** — Stack tecnológico actual / preferido. Quién mantiene post-launch.
- **ESTRATÉGICA** — Hosting actual.
- Identidad visual / branding (logo, colores hex, tipografía). · *de base\contexto-\<slug\>.md*
- **Equipo / personas para E-E-A-T**: nombres, cargos, credenciales verificables, fotos, LinkedIn. · *de base\contexto-\<slug\>.md*
- Casos de éxito / portfolio / testimonios disponibles. · *de base\contexto-\<slug\>.md*
- Certificaciones y acreditaciones. · *de base\contexto-\<slug\>.md*
- **ESTRATÉGICA** — Ofertas y CTAs.
- Operaciones que afectan el sitio: horario, tiempo de respuesta, canales de contacto. · *de base\contexto-\<slug\>.md*

---

## Nivel 4 — Continuas (durante la implementación)

- **Competencia**: directos / indirectos / aspiracional.
- Marketing existente, tracking/analytics actuales, activos de contenido existentes.
- Backlinks / autoridad actual.
- **Legal/regulatorio** (clave en YMYL: salud, finanzas, legal — disclaimers, protección de datos).
- Presupuesto / plazos.
- **Definition of success + decision gates** (qué se evalúa a M3/M6/M9).

---

## Apéndice A — Datos por tipo de schema

Pedir solo los del schema que aplique:
- **Organization / LocalBusiness**: nombre, dirección exacta, GPS, teléfono, horario por día, áreas servidas, redes (sameAs).
- **Person** (negocios persona-céntricos): nombre, título exacto, universidad, año de titulación, **número de registro profesional**, posgrados, áreas de expertise (`knowsAbout`), foto 800×800.
- **Product**: SKU, precio, disponibilidad, marca, GTIN.
- **Service**: descripción, tipo, área servida, audiencia.
- **Event / Article**: fechas, autor, ubicación.

## Apéndice B — Preguntas extra por tipo de negocio

- **E-commerce**: catálogo, plataforma, feed de Shopping, inventario.
- **SaaS**: modelo PLG/SLG, prueba gratis, integraciones, comparativas vs competidores.
- **Local / brick-and-mortar**: # ubicaciones, GBP existentes, reviews actuales.
- **Healthcare / legal / finanzas (YMYL)**: credenciales verificables, disclaimers obligatorios, líneas de crisis, protección de datos.
- **Agencias / freelancers**: portfolio, autoría personal.

---

## Checklist final (10 ítems antes de empezar el spec)

- [ ] Modelo de negocio claro en una frase
- [ ] Dominio confirmado y con acceso
- [ ] Estado del sitio definido (greenfield/básico/migración)
- [ ] Audiencia primaria + % revenue
- [ ] Cobertura geográfica + física vs service-area por ubicación
- [ ] Servicios/productos con flagship vs complementario
- [ ] Modelo de conversión + ciclo de venta
- [ ] **Restricción dominante identificada** (la fuerza que gobierna todo → §0.1 del spec)
- [ ] Personas para E-E-A-T con datos verificables
- [ ] Alcance del entregable + plazo + decision gates

### Modos de discovery (tiempo estimado)
| Modo | Cuándo | Tiempo |
|---|---|---|
| Sesión única | Cliente disponible, negocio simple | 60-90 min |
| Intake form | Cliente ocupado, datos conocidos | async + 30 min repaso |
| Workshop multi-sesión | Negocio complejo, varios stakeholders | 2-3 sesiones |

---

## Salida del framing (qué produce el discovery)

El discovery es la fase FRAMING. Produce dos artefactos (NO el spec):
1. `Clientes\<slug>\docs\superpowers\discovery\<fecha>-<slug>-discovery.md` — el discovery narrado.
2. `Clientes\<slug>\arquitectura\data\enfoque.md` — el handoff a arquitectura-seo (formato en
   `references/00b-flujo-y-contratos.md`), derivado de la restricción dominante (§0.1) y del enfoque
   de arquitectura elegido (§2).

Tras escribir `enfoque.md`, se corre arquitectura-seo. El spec §0–§14 se ensambla DESPUÉS.

### Ramificación por `estado del sitio`

El campo **estado del sitio** (Nivel 1) ramifica todo el escenario (detalle en `references/00b-flujo-y-contratos.md`):

- `greenfield` | `básico` → **Escenario B (foundation)**: arquitectura-seo en modo greenfield (sin
  inventario/301); spec sabor foundation (§13 N/A); planes = fases de build.
- `con-tráfico` → **Escenario A (migración)**: fase de diagnóstico previa que master **CONSUME, no
  corre**; arquitectura-seo en modo migración (inventario + `mapeo-301.csv`); spec sabor migración
  (§13 activo, KPI de retención); planes con M0-M2 antes del build.
