# Escenario de prueba — Migración de sitio existente (servicios B2B)

**Qué prueba:** que el skill NO trate como greenfield a un cliente con sitio y tráfico existente.

## Brief del cliente

**TecnoClima Perú** — empresa de climatización (HVAC) industrial y comercial. Lima, 12 años, 25 empleados, 3 ingenieros con certificaciones vigentes.

- **Sitio actual:** WordPress de 2018, ~180 URLs indexadas: 8 páginas de servicio, 40 posts de blog, ~60 páginas de proyectos antiguos muy delgadas, resto tags/archivos. URLs mixtas (`/index.php?p=123` conviviendo con slugs).
- **Tráfico:** ~8.000 clics orgánicos/mes (GSC con acceso completo, 16 meses de historia). GA4 activo. ~320 dominios de referencia. Varias keywords top 3 ("mantenimiento de chillers lima") y muchas en posición 5-15.
- **Lo que quieren:** rediseño completo en stack nuevo + reestructura de URLs. Misma marca, mismo dominio.
- **Audiencia:** B2B industrial (70% revenue), B2B comercial (30%). Ciclo de venta 1-3 meses.
- **Cobertura:** sede única en Lima; provincias como service area.
- **Conversión:** formulario + llamada telefónica.
- **Alcance:** estrategia integral 12 meses.

## Cobertura esperada (checklist de evaluación)

- [ ] El Mes 1 empieza con **inventario de contenido** con data GSC/GA4 (clics, impresiones, posición, backlinks por URL) y **benchmark pre-migración**, NO con construir desde cero.
- [ ] Matriz **keep / improve / consolidate / kill** aplicada a las ~180 URLs (los 60 proyectos thin → consolidar/matar).
- [ ] **Mapa 301 URL-por-URL** (1:1, sin redirigir todo a Home, máx. 1 salto).
- [ ] **Quick wins M1-M2**: queries en posición 5-15 (striking distance), rewrites de title/meta, enlaces internos hacia ellas.
- [ ] **Crawl diff staging vs producción** antes del switch.
- [ ] **Ventana de monitoreo post-migración** con cadencia y criterios de alerta.
- [ ] Expectativa declarada de fluctuación temporal de rankings (2-6 semanas).
