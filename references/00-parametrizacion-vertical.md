# 00 · Parametrización por rubro

**Cuándo leer:** después del discovery y ANTES de decidir arquitectura. El esqueleto §0-§14 es el mismo para todo rubro; lo que cambia son los **parámetros**. `case-studies.md` muestra el mecanismo con dos rubros; esta tabla lo extiende a los demás. Ubica el negocio en una fila y úsala para instanciar §0.1, §2-§5, §10 y §12.

| Rubro | Restricción dominante típica | Dimensiones de arquitectura | Núcleo schema | Content-types clave | Conversión (eventos) | Forma del año 1 |
|---|---|---|---|---|---|---|
| **Servicios B2B/B2C** (AioTech) | Normativa demostrable / ciclo de venta largo | servicios × sectores × ubicaciones | `Organization` | hubs, spokes, casos, blog | lead: `form_submit`, `phone_click`, `whatsapp_click` | foundation → expansión local/sectorial → autoridad → optimización (`09`) |
| **Persona-céntrico / YMYL** (Inspira) | E-E-A-T / YMYL | especialidades (hub por problemática) | `Person` | hubs de especialidad, blog firmado | `booking_click`, `whatsapp_click` | igual que servicios, cadencia baja y todo firmado |
| **Local multi-sede** (restaurantes, clínicas, retail) | Proximidad + reviews por sede | sedes × servicios/carta | `LocalBusiness`/vertical **por sede** | página por sede, servicios/menú en HTML (nunca solo PDF), blog local ligero | `booking_click`, `phone_click`, direcciones GBP | GBP+NAP por sede → páginas de sede → reviews → contenido local |
| **E-commerce** | Gobernanza de catálogo e indexación a escala | categorías → subcategorías → producto (+ guías) | `Organization`/`OnlineStore` + `Product`/`Offer` por ficha | colecciones con copy único, fichas, guías de compra, comparativas | GA4 e-commerce estándar: `view_item`, `add_to_cart`, `purchase` | técnica + facetas → colecciones top → guías/soporte → autoridad + facetas curadas |
| **SaaS** | PLG/ciclo de prueba + incumbentes con más autoridad | features × casos de uso × integraciones × comparativas | `Organization` + `SoftwareApplication` (offers de planes) | features, use-cases, integraciones, **vs/alternativas (BOFU primero)**, pricing, glosario | `trial_signup`, `demo_request` | comparativas BOFU → features/use-cases → topical authority → integraciones |
| **Publisher / afiliados** | E-E-A-T de autores + frescura a escala editorial | topics/secciones × formatos | `Organization`/`NewsMediaOrganization` + `Person` autores | artículos, reviews con experiencia real de producto, evergreen actualizable | pageviews, clic afiliado, suscripción | taxonomía → autoridad de autores → actualización sistemática |
| **Marketplace / directorio / programático** | Render + crawl budget + thin a escala (principio 9) | entidad × modificador (data-driven) | `ItemList` + entidad por página | plantillas con datos únicos por página | según modelo | validar render+indexación en muestra → escalar por lotes con gates de indexación |

**Si el rubro no está en la tabla:** deriva la fila con el mecanismo de `case-studies.md` (restricción dominante → dimensiones → núcleo schema → conversión) y regístrala en el spec.

## Reglas transversales de parametrización

1. **País e idioma.** Los ejemplos del skill usan Ecuador (`EC`, `es-EC`, SENESCYT/MSP, RUC/SUPERCÍAS, LOPDP, Doctoralia). Son **ejemplos, no defaults**: sustituir siempre por los equivalentes del país del cliente — ISO del país, `es-XX`, registro profesional local (colegiatura, cédula profesional…), registros mercantiles locales, ley de protección de datos (GDPR, LFPDPPP, LGPD, LOPDP…) y directorios sectoriales de ese mercado.
2. **Conversión.** El modelo elegido en discovery propaga a TODO: CTA flotante (WhatsApp / llamada / reserva / carrito), eventos GA4, mensajes prellenados, hidden fields y KPIs Tier 1. **No asumir WhatsApp** — es el ejemplo de los case studies, no la regla.
3. **Escala.** Si el inventario indexable proyectado supera ~1.000 URLs (e-commerce, programático, publisher), añadir a §8: análisis de logs / crawl budget, reglas de facetas y paginación, y gates de indexación por lote antes de escalar (ver `07-technical-seo.md`).
4. **Sitio existente.** Si hay tráfico previo, `references/13-migracion-sitio-existente.md` modifica la Fase 1 — aplica a cualquier rubro.

## Mini-regla e-commerce: facetas
Facetas (`?color=`, `/sofas-grises`) → **noindex por defecto**. Se promueve una combinación a colección indexable solo con las tres condiciones: demanda demostrada (keyword con volumen) + copy único + inventario suficiente. Canonical de facetas → su colección. **Paridad estricta `Product` schema ↔ feed de Merchant Center** (precio/disponibilidad desalineados = desaprobaciones).
