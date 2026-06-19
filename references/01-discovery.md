# 01 · Discovery — cuestionario de intake

El discovery es el primer artefacto. Sin los datos del **Nivel 1**, no se puede empezar el spec. Filosofía: no todas las preguntas aplican a todo negocio — salta las irrelevantes y **registra por qué** las saltaste.

Output: `docs/superpowers/discovery/YYYY-MM-DD-{cliente}-discovery.md`.

---

## Nivel 1 — Fundacionales (BLOQUEANTES)

| Pregunta | Por qué importa |
|---|---|
| Nombre legal + marca comercial | NAP, schema, GBP |
| Año de fundación, país, ciudad sede, tamaño de equipo | Organization schema, E-E-A-T |
| Modelo de negocio en una frase | Define todo el enfoque |
| Dominio: ¿confirmado / disponible / WHOIS / quién tiene acceso? | Bloqueante técnico |
| **Estado del sitio**: greenfield / básico (rehacer URLs libre) / con tráfico (requiere migración con 301) | Cambia el plan de Fase 1 por completo |
| Idioma: único / bilingüe / selectivo | Hreflang, arquitectura |
| **Modelo de conversión**: compra / lead / WhatsApp / llamada / booking + ciclo de venta | CTAs, tracking, atribución |
| Alcance del entregable (ver escala abajo) + plazo | Tamaño del spec |

**Escala de alcance** (elegir uno):
1. Arquitectura mínima (URLs + schema + technical baseline).
2. Arquitectura + contenido de lanzamiento (mes 1).
3. Estrategia trimestral (3 meses).
4. **Estrategia integral 12 meses** (lo que cubren AioTech e Inspira).

---

## Nivel 2 — Estratégicas (definen la arquitectura)

- **Audiencia primaria**: B2B (enterprise / mid / SMB) · B2C (premium / mass) · B2G · mixto. Pedir **% de revenue** por segmento + buyer personas.
- **Cobertura geográfica**: ciudad / región / país / multinacional. **Crítico**: por cada ubicación, ¿oficina física o solo service area? → decide schema/GBP y si hay arquitectura de ubicaciones.
- **Servicios/productos**: por cada uno → audiencia, ticket, margen, flagship vs complementario, estacionalidad, **sub-servicios (= spokes)**.
- **Sectores/industrias atendidas** (si aplica → dimensión de arquitectura).
- **Modelo de precios y USP** (diferenciador real, no marketing).

---

## Nivel 3 — Operativas (afinan implementación)

- Stack tecnológico actual / preferido. Quién mantiene post-launch.
- Hosting actual.
- Identidad visual / branding (logo, colores hex, tipografía).
- **Equipo / personas para E-E-A-T**: nombres, cargos, credenciales verificables, fotos, LinkedIn.
- Casos de éxito / portfolio / testimonios disponibles.
- Ofertas y CTAs.
- Operaciones que afectan el sitio: horario, tiempo de respuesta, canales de contacto.

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
