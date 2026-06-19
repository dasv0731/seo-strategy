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
- **Imágenes**: WebP + AVIF fallback; hero ≤ 150KB; `width`/`height` explícitos; lazy load excepto el LCP.
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
Viewport correcto · tap targets ≥ 48×48px · texto ≥ 16px · botón flotante (WhatsApp) sin tapar contenido ni generar CLS.

## IndexNow
Activar + validar `{base}/{key}.txt` accesible. Auto-ping en publish/update/delete a Bing, Yandex, Naver, Seznam.

## Setup de medición
| Herramienta | Setup |
|---|---|
| Google Search Console | Property domain + verificación DNS TXT + submit sitemap_index |
| Bing Webmaster | Importar de GSC + registrar IndexNow key |
| GA4 | Enhanced measurement ON + eventos custom: `whatsapp_click`, `form_submit`, `phone_click`, `case_view`, `booking_click` |
| Cloudflare Web Analytics | Backup privacy-friendly |
| GTM | Container único, defer 2s |

## Mantenimiento (cron)
| Frecuencia | Tarea |
|---|---|
| Diario | Backup |
| Semanal | Updates menores; security; GBP Insights |
| Quincenal | Auditar 404s en GSC + redirects |
| Mensual | Crawl completo (Screaming Frog); PSI/CWV; schema; NAP citations |
| Trimestral | Lighthouse + Sitebulb; pen-test básico; review del stack de herramientas |
