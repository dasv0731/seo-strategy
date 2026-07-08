# 07 · Technical SEO foundation

Stack-agnóstico: los **targets y reglas** valen para cualquier CMS o framework. Lo que importa es el resultado medible, no la herramienta que lo produce.

## Hosting / CDN
Hosting de alto rendimiento **cerca de la audiencia** + CDN con optimización de plataforma. Latencia objetivo a la audiencia ≤ ~80-100ms. SSL Full (strict).

## CWV targets
| Métrica | Mobile | Desktop |
|---|---|---|
| LCP | ≤ 2.0s | ≤ 1.8s |
| INP | ≤ 150ms | ≤ 100ms |
| CLS | ≤ 0.05 | ≤ 0.05 |
| TTFB | ≤ 600ms | ≤ 400ms |
| FCP | ≤ 1.5s | ≤ 1.2s |

## Optimizaciones obligatorias
- **Imágenes**: WebP + AVIF fallback; hero ≤ 150KB; `width`/`height` explícitos; lazy load excepto el LCP; **alt text descriptivo obligatorio** (natural, sin stuffing) + nombre de archivo con keyword (`mantenimiento-chillers-lima.webp`, no `IMG_1234.jpg`).
- **Fonts**: 1 familia máx., self-hosted, `font-display: swap` + preload (no CDN de Google Fonts).
- **JS**: defer/async todo lo no crítico; widget de chat con defer; GTM diferido 2-3s; sin librerías pesadas.
- **CSS**: critical CSS inline en `<head>`, resto async.
- **HTML**: minify, gzip/brotli, HTTP/2 o HTTP/3.
- **DB / backend**: limpieza periódica de datos transitorios y consultas no usadas.

## Criterios para elegir herramientas (cualquier stack)
No importa el CMS/framework; sí que el stack cumpla estas funciones sin sacrificar CWV:
- **SEO/meta + schema**: motor que permita inyectar JSON-LD custom por content-type.
- **Caché/CDN**: una sola capa de caché (no dos solapadas) + CDN con optimización de borde.
- **Imágenes**: pipeline WebP/AVIF automático.
- **Forms + anti-spam**, **redirects 301**, **IndexNow**, **backups**, **security**.

**Evitar (en cualquier plataforma):** constructores/extensiones que inflan el DOM y matan INP/LCP, dos sistemas de caché a la vez, librerías JS pesadas no usadas, y motores SEO que generan schema pobre o no extensible.

## Sitemap
Index + un sitemap por content-type + posts + imágenes:
```
/sitemap_index.xml
  ├── sitemap-pages.xml
  ├── sitemap-{cpt}.xml  (uno por content-type)
  ├── sitemap-posts.xml
  └── sitemap-images.xml
```
`lastmod` **solo si es fidedigno** (fecha real de cambio de contenido, no del deploy): Google lo usa cuando es confiable y lo ignora para siempre si detecta que miente.

## Headers de seguridad
```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; [extender]
```
HSTS preload tras 6 meses estables.

## Mobile-first
Viewport correcto · tap targets ≥ 48×48px · texto ≥ 16px · botón flotante del canal principal de conversión (WhatsApp / llamada / reserva) sin tapar contenido ni generar CLS.

## IndexNow
Activar + validar `{base}/{key}.txt` accesible. Auto-ping en publish/update/delete a Bing, Yandex, Naver, Seznam.

## Escala (solo si el inventario indexable proyectado > ~1.000 URLs)
E-commerce, programático, publishers: **análisis de logs** (qué rastrea Googlebot realmente) · crawl budget (eliminar cadenas de redirects, 404 masivos, facetas rastreables infinitas) · reglas de facetas/paginación explícitas · escalar contenido **por lotes con gate de indexación** (verificar % indexado del lote anterior antes de abrir el siguiente — principio 9). En sitios < ~1.000 URLs, omitir: el crawl budget no es la restricción.

## Setup de medición
| Herramienta | Setup |
|---|---|
| Google Search Console | Property domain + verificación DNS TXT + submit sitemap_index |
| Bing Webmaster | Importar de GSC + registrar IndexNow key |
| GA4 | Enhanced measurement ON + eventos custom **según el modelo de conversión del discovery** — lead: `form_submit`, `phone_click`, `whatsapp_click` · booking: `booking_click` · e-commerce: `view_item`, `add_to_cart`, `purchase` · SaaS: `trial_signup`, `demo_request` (+ `case_view` si hay casos) |
| Cloudflare Web Analytics | Backup privacy-friendly |
| GTM | Container único, defer 2s |
| Consentimiento | Banner + **Google Consent Mode v2** — obligatorio con audiencia UE, recomendado donde aplique ley local (LGPD, LFPDPPP, LOPDP…). Diferir GTM no exime del consentimiento; el defer distorsiona la atribución de sesiones cortas — documentarlo en el spec |

## Mantenimiento (cron)
| Frecuencia | Tarea |
|---|---|
| Diario | Backup |
| Semanal | Updates menores; security; GBP Insights |
| Quincenal | Auditar 404s en GSC + redirects |
| Mensual | Crawl completo (Screaming Frog); PSI/CWV; schema; NAP citations |
| Trimestral | Lighthouse + Sitebulb; pen-test básico; review del stack de herramientas |
