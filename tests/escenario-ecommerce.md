# Escenario de prueba — E-commerce puro (México)

**Qué prueba:** que el skill parametrice dimensiones de catálogo (no servicios/sectores), schema de producto, facetas, conversión = compra, y país ≠ Ecuador.

## Brief del cliente

**Kuna Home** — tienda online de muebles y decoración de marca propia. CDMX, envíos a todo México, **sin tiendas físicas**.

- **Plataforma:** Shopify. **1.200 SKUs**, ~60 categorías/subcategorías. **Navegación facetada** por material, color, precio y estilo.
- **Sitio:** 8 meses de vida, ~600 clics orgánicos/mes. Venden sobre todo por Meta Ads y un marketplace externo.
- **Google Merchant Center activo** (campañas de Shopping).
- **Conversión:** compra online (checkout). Ticket promedio $2.400 MXN. Tienen chat pero el objetivo es `purchase`.
- **Marca:** 2 diseñadores fundadores con apariciones en prensa de diseño.
- **Alcance:** estrategia integral 12 meses.

## Cobertura esperada (checklist de evaluación)

- [ ] Dimensiones de arquitectura = **categorías / subcategorías / producto** (+ guías de compra), NO servicios×sectores×ubicaciones.
- [ ] **Reglas de facetas**: noindex por defecto; indexar solo combinaciones con demanda + copy único.
- [ ] Schema: **`Product` + `Offer`** (precio, disponibilidad, GTIN/SKU); `AggregateRating` solo con reseñas reales; `Organization` como núcleo.
- [ ] **Merchant Center / Shopping** integrado a la estrategia (feed ↔ SEO).
- [ ] Roadmap año 1 con forma de catálogo (técnica+catálogo → categorías → contenido de soporte → autoridad), no FOUNDATION→LOCAL+SECTOR.
- [ ] Conversión/tracking: eventos e-commerce (`purchase`, `add_to_cart`), NO `whatsapp_click` como principal.
- [ ] Schema/país: `addressCountry: MX`, `es-MX` — nada de `EC`.
- [ ] Sin capa local/GBP (no hay sede física) — sección omitida con razón registrada.
- [ ] Mención de crawl budget / control de indexación si el inventario crece.
