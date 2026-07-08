# Escenario de prueba — Local multi-sede (Colombia)

**Qué prueba:** multi-sede real (vs service area), conversión = reserva, vertical restaurante, país Colombia, alcance trimestral.

## Brief del cliente

**La Nona** — trattoria italiana con **3 sedes reales**: Bogotá-Chapinero, Bogotá-Usaquén y Chía.

- **GBP:** Chapinero 4.6★ (220 reseñas), Usaquén 4.1★ (90), Chía **sin reclamar**.
- **Web actual:** one-page con el menú en PDF.
- **Conversión:** reserva online (widget de booking) + llamadas. Delivery vía apps de terceros.
- **Marca:** chef fundador con reconocimiento gastronómico local (prensa, un premio).
- **Alcance:** estrategia trimestral (escala 3), presupuesto ajustado.

## Cobertura esperada (checklist de evaluación)

- [ ] **3 sedes reales → 3 GBP + 3 páginas de sede** con `LocalBusiness`/`Restaurant` y dirección propia (no service area).
- [ ] Reclamar el GBP de Chía como tarea temprana.
- [ ] **Menú en HTML** (no PDF) — indexable, con precios.
- [ ] Schema `Restaurant` (+ `Menu` si aplica); chef como `Person` para E-E-A-T.
- [ ] Conversión/tracking: `booking_click` / reserva + llamadas — no formulario B2B.
- [ ] Estrategia de reviews por sede (subir Usaquén, mantener Chapinero).
- [ ] Alcance acotado a trimestre (no plan de 12 meses).
- [ ] País/idioma: Colombia, `es-CO` — nada de Ecuador.
