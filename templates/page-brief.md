# Plantilla — Brief de página con copy (para §14 del spec)

> **Delegación.** Este brief = lista de páginas del árbol (`arquitectura.csv`) + notas estratégicas. La ESTRUCTURA de secciones la produce `diseño-secciones`; el COPY informacional largo, `content-engine`. No re-diseñes secciones ni redactes el cuerpo aquí.

## Convenciones globales (definir una vez, aplican a todas)
| Elemento | Especificación |
|---|---|
| Header | Logo + menú + CTA primario |
| Footer | NAP + hubs (servicios/sectores/ubicaciones) + legales + redes |
| CTA flotante | Canal principal del discovery (WhatsApp / llamada / reserva / carrito) — defer, sin tapar contenido, sin CLS |
| Breadcrumbs | Todas excepto Home + `BreadcrumbList` |
| CTA secundario | Mid-page |
| Mobile-first | Tap ≥48px, texto ≥16px |
| Imágenes | ALT descriptivo + archivo nombrado con keyword + WebP |
| Tono | [definir: técnico / cálido / ...] |

## Brief por página
```
URL: /...
TITLE (≤60 car): ...
META DESCRIPTION (≤155 car): ...
H1: ...
KEYWORD PRINCIPAL: ...   SECUNDARIAS: [3-5]
INTENT: ...
SCHEMA: [lista]
LONGITUD: [N palabras]

--- COPY POR SECCIÓN ---
HERO: titular + subhead empático/técnico + CTA
TL;DR (40-60 palabras, GEO-citable): ...
[Bloque 1: ¿Para quién es? / Problema]
[Bloque 2: Qué ofrecemos / Cómo trabajamos — sin promesas]
[Bloque 3: Señales / aplicaciones / sub-servicios (spokes)]
[Bloque 4: Prueba — casos / credenciales / marcas]
[Modalidad / cobertura]
FAQ (4-6, pregunta H3 + respuesta directa 1ª oración):
CTA FINAL: [según modelo de conversión: WhatsApp + form | agenda | carrito | trial] + mensaje prellenado si aplica
[YMYL: Disclaimer + Crisis Box]
[Bloque de autoría → Person]

DATOS A CONFIRMAR antes de publicar:
- // CONFIRMAR ...
```
