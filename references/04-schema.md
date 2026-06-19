# 04 · Schema y datos estructurados

## Estrategia: un grafo, no schemas sueltos
Un **grafo JSON-LD** con `@id` referenciado entre nodos para que el motor entienda que `Organization`, `LocalBusiness` por ciudad, `Person` y `Service` son **la misma entidad coherente**. El motor/módulo SEO genera la base; los content-types custom se inyectan vía hook/filtro del motor o como bloque de código en cada plantilla.

## Tabla schema por página

| Schema | Dónde | Propósito |
|---|---|---|
| `Organization` | Home (referenciado en todas) | Entidad raíz, sameAs, founders |
| `WebSite` | Home | SearchAction + sitelinks |
| `ProfessionalService` + tipo vertical (multi-type) | Home / contacto | LocalBusiness HQ |
| `LocalBusiness` por ciudad | cada `/ubicaciones/[ciudad]` con sede real | service area |
| `Service` | cada servicio | descripción + `provider` link |
| `OfferCatalog` + `Offer` | hubs de servicio | subservicios como ofertas |
| `WebPage` + `BreadcrumbList` | todas | navegación |
| `FAQPage` | servicios, sectores, Home, contacto, primera-sesión | rich snippet FAQ |
| `Article` / `TechArticle` / `BlogPosting` | blog | autoría + fecha (`author`→Person) |
| `Article` con `about`→Service | casos | caso como prueba E-E-A-T |
| `Person` | equipo / bios | autoría con `knowsAbout`, `hasCredential` |
| `ContactPoint` | anidado en Organization | WhatsApp + email + teléfono |
| `ImageObject` | imágenes con metadata | license + author |

## Person vs Organization (decisión de núcleo)
- **Negocio corporativo** (AioTech): núcleo `Organization`; el equipo (`Person[]`) lo respalda como founders/autores.
- **Negocio persona-céntrico** (Inspira): núcleo `Person`; el motor SEO se configura como **Site type = Person**. `Person` se referencia como `author`/`provider`/`founder` en todo el contenido. Campos clave: `alumniOf`, `hasCredential`, `knowsAbout`, `memberOf`, `sameAs`, `worksFor`→Organization.

### Notas de tipos que no existen
- **No existe `Psychologist` en Schema.org** → usar `Person` (con `jobTitle`/`hasOccupation`) + `MedicalBusiness`/`ProfessionalService` para el negocio local.
- Cuando dudes del tipo correcto, usa el más cercano + multi-type array (`["MedicalBusiness","ProfessionalService"]`).

## Esqueleto del grafo en Home (patrón)
```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "{base}/#organization",
      "name": "...", "url": "{base}/", "logo": {"@type":"ImageObject","url":"..."},
      "founder": [{"@id": "{base}/equipo#persona"}],
      "sameAs": ["LinkedIn","Facebook","Instagram"],
      "contactPoint": [{"@type":"ContactPoint","telephone":"+...","areaServed":"EC","availableLanguage":"es"}] },
    { "@type": "WebSite", "@id": "{base}/#website",
      "url": "{base}/", "publisher": {"@id": "{base}/#organization"}, "inLanguage": "es-EC" },
    { "@type": ["ProfessionalService","{tipo-vertical}"], "@id": "{base}/#localbusiness",
      "name": "...", "telephone": "+...", "priceRange": "$$-$$$",
      "address": {"@type":"PostalAddress","addressLocality":"...","addressRegion":"...","addressCountry":"EC"},
      "areaServed": [{"@type":"City","name":"..."}],
      "hasOfferCatalog": {"@type":"OfferCatalog","itemListElement":[
        {"@type":"Offer","itemOffered":{"@type":"Service","@id":"{base}/servicios/...#service"}}
      ]} }
  ]
}
```

## Regla crítica (innegociable)
**NO incluir `Review` / `AggregateRating` hasta que existan reseñas verificables reales.** Markup falso = violación de guidelines de Google, especialmente grave en YMYL. Lo mismo aplica a credenciales: nunca `hasCredential` no verificable.

## Validación obligatoria antes de cada deploy (4 pasos)
1. Google Rich Results Test — https://search.google.com/test/rich-results
2. Schema Markup Validator — https://validator.schema.org/
3. Validador del motor SEO (si lo ofrece).
4. Manual: revisar el grafo serializado (jq / JSON formatter) — confirmar que los `@id` enlazan.
