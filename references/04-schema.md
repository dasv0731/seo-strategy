# 05 · Schemas y datos estructurados — ANCLAJE + delegación

master decide el **anclaje estratégico** del grafo: la entidad raíz (`Organization` | `Person` |
`LocalBusiness` | `OnlineStore` | `SoftwareApplication`…) según el rubro (00-parametrizacion) y la
restricción dominante, y qué entidades E-E-A-T la respaldan (§7).

**NO generes el JSON-LD aquí.** La generación del grafo conectado por @id para todo el dominio la
hace **schema-graph** (`Clientes\<slug>\schema-graph\` → `SCHEMA-REPORT.md`, snippets por página).

**Recipe:** en §5 del spec, declara el anclaje + la tabla schema/dónde/propósito a alto nivel +
"validación y generación → schema-graph". Si existe `SCHEMA-REPORT.md`, referéncialo; si no, anota
"generación pendiente: schema-graph".

---

## El anclaje: qué entidad es la raíz (decisión de núcleo — se conserva)
El grafo es **una entidad coherente** referenciada por `@id` (Organization, LocalBusiness por ciudad, Person y Service como la misma entidad), no schemas sueltos. La decisión estratégica de master es **qué entidad la ancla**, según rubro (00-parametrizacion) y restricción dominante:
- **Negocio corporativo** (AioTech): núcleo `Organization`; el equipo (`Person[]`) lo respalda como founders/autores.
- **Negocio persona-céntrico** (Inspira, YMYL): núcleo `Person`; el motor SEO se configura como **Site type = Person**. `Person` se referencia como `author`/`provider`/`founder` en todo el contenido. Campos clave: `alumniOf`, `hasCredential`, `knowsAbout`, `memberOf`, `sameAs`, `worksFor`→Organization.
- **E-commerce**: núcleo `OnlineStore` (+ `Organization`). **SaaS**: `SoftwareApplication` (+ `Organization`). **Local puro / service-area**: `LocalBusiness` o el subtipo vertical como cara del negocio.

master fija la raíz + qué entidades E-E-A-T la respaldan (`Person`, `hasCredential`, `sameAs`, casos como prueba — ver §7). La **elección y validación del tipo exacto** contra el vocabulario oficial (p. ej. **no existe `Psychologist`** → `Person` con `jobTitle`/`hasOccupation` + `MedicalBusiness`/`ProfessionalService` para el negocio local; multi-type array cuando dudes) la resuelve **schema-graph**; aquí solo se declara la raíz estratégica.

## Tabla schema/dónde/propósito (alto nivel — el JSON-LD lo genera schema-graph)
Declara en §5 el mapa de alto nivel de qué schema vive dónde y para qué. **No escribas aquí el JSON-LD ni el wiring de `@id` por página** — el grafo serializado, el esqueleto del Home y los snippets por página son el entregable de schema-graph:

| Schema | Dónde | Propósito |
|---|---|---|
| `Organization` | Home (referenciado en todas) | Entidad raíz, sameAs, founders |
| `WebSite` | Home | SearchAction + sitelinks |
| `ProfessionalService` + tipo vertical (multi-type) | Home / contacto | LocalBusiness HQ |
| `LocalBusiness` por ciudad | cada `/ubicaciones/[ciudad]` con sede real | service area |
| `Service` | cada servicio | descripción + `provider` link |
| `OfferCatalog` + `Offer` | hubs de servicio | subservicios como ofertas |
| `WebPage` + `BreadcrumbList` | todas | navegación |
| `FAQPage` | servicios, sectores, Home, contacto, primera-sesión | estructura extractable para GEO/AI — el rich snippet FAQ solo aparece para sitios gubernamentales/salud de alta autoridad desde 2023; no prometerlo |
| `Article` / `TechArticle` / `BlogPosting` | blog | autoría + fechas (`author`→Person, `datePublished` + `dateModified`; en YMYL: fecha de revisión + revisor **visibles en la página**, no solo en el schema) |
| `ProfilePage` | páginas de bio del equipo | E-E-A-T persona-céntrico (`mainEntity`→Person) — soportado por Google desde 2024 |
| `Article` con `about`→Service | casos | caso como prueba E-E-A-T |
| `Person` | equipo / bios | autoría con `knowsAbout`, `hasCredential` |
| `ContactPoint` | anidado en Organization | WhatsApp + email + teléfono |
| `ImageObject` | imágenes con metadata | license + author |

## Regla crítica (innegociable — guardrail que master impone a schema-graph)
**NO incluir `Review` / `AggregateRating` hasta que existan reseñas verificables reales.** Markup falso = violación de guidelines de Google, especialmente grave en YMYL. Lo mismo aplica a credenciales: nunca `hasCredential` no verificable. master registra esta restricción en §5 como límite duro que schema-graph debe respetar al generar el grafo.

## Validación y generación → schema-graph
El grafo conectado por `@id`, el esqueleto del Home, los snippets por página y su **validación** (Google Rich Results Test, Schema Markup Validator, validador del motor SEO, y la revisión manual de que los `@id` enlazan) son trabajo de **schema-graph**, que entrega `SCHEMA-REPORT.md`. Si ya existe, referéncialo desde §5; si no, anota *"generación pendiente: schema-graph"*. No dupliques aquí ni la generación ni el checklist de validación.
