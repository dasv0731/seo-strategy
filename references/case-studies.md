# Case studies — el mismo esqueleto, dos negocios

Esta es la pieza de mayor valor del skill: muestra cómo **el mismo esqueleto §0–§14 se parametriza** distinto según el negocio. No memorices los detalles; aprende el *mecanismo de adaptación*.

## Tabla comparativa

| Dimensión | **AioTech** | **Inspira Bienestar** |
|---|---|---|
| Negocio | Ingeniería eléctrica/automatización | Psicóloga individual (Andrea) |
| Audiencia | B2B industrial + comercial + B2C premium (mixta) | B2C en estado vulnerable |
| **Restricción dominante (§0.1)** | Cumplimiento normativo demostrable + ciclo B2B largo | **YMYL / E-E-A-T en salud mental** |
| Geografía | Nacional + foco sector petrolero (multi-ubicación) | 1 sede (Quito) + online nacional |
| **Arquitectura (§2)** | **Matriz cruzada** (servicios × sectores × ubicaciones + casos) | **Especialidad-first** hub-and-spoke por problemática |
| Núcleo de marca / schema (§5) | `Organization` + `ProfessionalService`/`Electrician` | **`Person`** (Andrea) + `MedicalBusiness`/`ProfessionalService`; Site type = Person |
| Capa local (§6) | 7 ubicaciones (1 sede real + 6 service area) + hub Oriente | Ligera: GBP + 2 páginas de modalidad |
| Conversión | WhatsApp + formulario corto (transaccional) | Agenda + WhatsApp + form (cálida, sin presión) |
| Cadencia de contenido (§10) | 4-6 piezas/mes | 2-3 piezas/mes (la experta firma todo) |
| Total páginas año 1 (§9) | ~80-95 | ~45-60 |
| Link building (§11) | Robusto: tiers, outreach, PR sectorial | Ligero: autoridad de persona, Doctoralia, podcasts |
| Off-site E-E-A-T | Membresías CIEEPI/CIP, marcas, casos | Colegio profesional, registro MSP, medios |
| Tono de contenido | Técnico, "cada decisión justificada con norma" | Cálido, validar antes de instruir, sin promesas |
| Riesgo principal | Canibalización entre dimensiones | Thin content + penalización YMYL |
| Extras YMYL | — | Disclaimers, Crisis Box, frases prohibidas, LOPDP |

## Lecciones de adaptación

1. **La arquitectura se elige por recursos, no por ambición.** AioTech tenía equipo y horizonte para sostener matriz cruzada (2-3× contenido). Inspira explícitamente **descartó** la matriz: una sola profesional no sostiene decenas de páginas únicas, y en YMYL las thin/duplicadas se penalizan más. Mismo esqueleto, decisión opuesta — y ambas correctas.

2. **El núcleo del grafo schema cambia con quién es la autoridad.** Corporativo → `Organization` con el equipo de respaldo. Persona-céntrico → `Person` como núcleo, referenciado como `author`/`provider` en todo el contenido.

3. **La restricción dominante (§0.1) propaga todo.** En Inspira, "YMYL" no es una nota: gobierna arquitectura (simple), schema (Person + sin Review falso), contenido (disclaimers), conversión (sin presión) y off-site (credenciales verificables). Identificarla bien al inicio evita inconsistencias en todo el spec.

4. **La capa local escala con el negocio.** Multi-ubicación con sede real → páginas por ciudad + GBP. Sede única → capa ligera. **Nunca** falsear ubicaciones.

5. **La cadencia se ajusta a quién produce.** Si la experta firma todo (E-E-A-T), la cadencia baja pero sube la calidad/autoridad. Mejor 2-3 piezas firmadas que 6 genéricas.

## Cómo usar estos casos
Cuando planees un negocio nuevo, ubícalo en el espectro:
- **¿Más cerca de AioTech?** (B2B, multi-servicio/sector/ubicación, equipo, ciclo largo) → matriz/sector-first, `Organization`, link building robusto.
- **¿Más cerca de Inspira?** (profesional/pequeño, YMYL o persona-céntrico, sede única) → especialidad-first, `Person`, off-site ligero, disciplina anti-thin.
- **¿Otro tipo?** (e-commerce, SaaS) → mantén el esqueleto, cambia las dimensiones (catálogo/categorías para e-commerce; features/casos de uso/integraciones para SaaS) y la restricción dominante (inventario; product-led).
