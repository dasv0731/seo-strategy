# 05 · Local SEO y Google Business Profile

*(Omitir o reducir mucho si el negocio no tiene componente local.)*

## Principio rector
**Una sola oficina física → un GBP completo.** Las demás ciudades son **service area, NO sedes**. Falsear ubicaciones múltiples en GBP = **suspensión permanente**.

- Sede real → GBP completo + página `/ubicaciones/[ciudad]` con `LocalBusiness` schema y dirección física.
- Otras ciudades → solo página SEO con `Service + areaServed`, sin pretender oficina.
- Negocio 100% online / 1 sede (Inspira) → capa local "ligera": GBP de la sede + 1-2 páginas de modalidad (`/psicologa-quito`, `/terapia-online`). No justifica matriz de ciudades.

## Configuración GBP
| Campo | Regla |
|---|---|
| Nombre | Exacto, **sin variantes** (idéntico al NAP) |
| Categoría primaria | La más específica del oficio |
| Categorías secundarias | Hasta 9, relevantes |
| Service area | Ciudad(es) + país si hay atención online |
| Teléfono | Fijo + WhatsApp Business |
| Sitio | URL canónica **con UTM** (`?utm_source=gbp&utm_medium=organic`) — sin esto el tráfico de GBP se reporta como directo y el Tier 2.5 queda ciego |
| Horario | Por día |
| Atributos | "Atiende emergencias", "Presupuestos sin costo", "Atención online", "Requiere cita"… |
| Servicios | Lista de servicios/áreas + spokes |

**Operativa:** posts ≥ 1/semana enlazando a una URL del sitio (imagen branded 1200×900). Q&A pre-poblado 8-15 preguntas **desde la cuenta de la empresa**.

## Estructura de página por ciudad (8 bloques)
1. Hero localizado + breadcrumb + CTA.
2. Intro **200-300 palabras únicas** por ciudad (evita thin/duplicado).
3. "Servicios disponibles en [Ciudad]" — cards localizadas.
4. "Casos en [Ciudad]" — 2-3 cards (o fallback si no hay).
5. "Sectores que atendemos en [Ciudad]" — cards.
6. Mapa **estático** de cobertura (no Google Maps embed — ahorra quota y CWV).
7. FAQ específico de la ciudad (4-6 preguntas).
8. CTA final.

Hub sectorial especial (p.ej. `/ubicaciones/oriente` en AioTech) → estructura ampliada con sub-zonas y enlace prominente al `/sectores/[sector]` relacionado.

## NAP consistency (auditoría obligatoria Mes 1)
Fijar un **NAP canónico** (Nombre, Address, Phone) idéntico en: GBP · web (footer + contacto) · schema `LocalBusiness` · Bing Places (auto-import de GBP) · Apple Maps · directorios locales/sectoriales · LinkedIn · Facebook · Instagram · cámaras/asociaciones · OpenStreetMap · (salud: Doctoralia).

## Estrategia de reviews
- Solicitud **post-proyecto/post-sesión** con link directo `g.page/r/[id]/review` + plantilla breve con beneficio para el cliente.
- Metas escalonadas: ~5 (M1-M3) → 15 (M6) → 30+ (año 1). *(Inspira más conservador: 5/15/25-30.)*
- Responder **TODAS ≤ 48h**. Negativas: respuesta pública corta + canal privado.
- Reviews 4★+ → render en Home / equipo.
- **Nunca presionar ni incentivar.** En YMYL/salud: responder **sin revelar que la persona es paciente** (confidencialidad).
