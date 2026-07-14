# 03 · Arquitectura: enfoque (FRAMING) + ensamblaje del árbol (CONSUMIR)

## §2 (FRAMING) — Elegir enfoque de arquitectura

Esta es una **decisión de framing**: no diseña URLs, decide la *lógica dominante* de la arquitectura. Su output se registra en `enfoque.md` y condiciona cómo se lee e interpreta el árbol que produjo arquitectura-seo. Documenta el enfoque **elegido**, los **descartados** y el **trade-off aceptado**.

| Enfoque | Dimensiones | Cuándo | Riesgo |
|---|---|---|---|
| **Servicio-first** | `/servicios/[slug]` hub→spokes | Negocio mono-audiencia, pocos servicios | Limitado si hay sectores/ubicaciones fuertes |
| **Sector-first** | `/sectores/[slug]` | La decisión la guía la industria del cliente | Diluye keywords de servicio |
| **Matriz cruzada** (AioTech) | servicios × sectores × ubicaciones + casos | Audiencia mixta + multi-ubicación + sectorial + horizonte 12m + **recursos para 2-3× contenido** | Canibalización si no hay disciplina de canonicales |
| **Especialidad-first** (Inspira) | hub-and-spoke por problemática, anclado en `Person` | Profesional/equipo pequeño, YMYL, sede única | — (el seguro por defecto) |

**Regla de oro:** elige por **tamaño y recursos reales**. Copiar la matriz cruzada a un negocio pequeño produce páginas thin y canibalización — **penalización grave en YMYL**. Una persona no sostiene decenas de páginas únicas.

### SERP reality check (obligatorio ANTES de fijar el enfoque)
El enfoque se elige por tamaño/recursos **y** por lo que el SERP premia hoy. Para las 5-10 keywords flagship, revisar el SERP real: **¿qué TIPO de página está en el top 10?** (service page, directorio/marketplace, guía informacional, comparativa, local pack, e-commerce).
- Si el SERP transaccional lo dominan directorios/marketplaces → una service page propia no rankeará por bien construida que esté: cambiar la apuesta (long-tail, local, comparativas) o competir por presencia EN esos agregadores.
- Registrar en `enfoque.md`: tipo de página dominante por keyword flagship + la implicación aceptada.
- Con datos en vivo: vía `orquestador-seo` (`claude-seo:seo-sxo` para page-type mismatch, `seo-dataforseo` para SERPs). Manual: incógnito + clasificar el top 10.
- Este juicio **caduca** (principio 10): re-revisar en cada decision gate.

### i18n: elección estructural (si discovery Nivel 1 marca bilingüe/multi-región)
La estructura de idioma es una decisión de **lógica dominante**, no de diseño de slugs: decídela aquí y regístrala en `enfoque.md` para que arquitectura-seo emita el árbol con el prefijo/estructura de idioma correcto. Orden por defecto: subdirectorio `/en/` (consolida autoridad) > subdominio > ccTLD (solo multi-región real con equipos separados). El árbol saldrá con esa estructura.

---

## §3 (ENSAMBLAJE) — Arquitectura de URLs: CONSUMIR el árbol

**NO diseñes el árbol de URLs aquí. Ya existe.** arquitectura-seo lo produjo en
`Clientes\<slug>\arquitectura\resultados\arquitectura.csv` (+ `arbol.html` visual, `enlazado.csv`).
Si te descubres escribiendo slugs, page-types o jerarquía desde cero, **DETENTE**: eso es
regenerar, no ensamblar.

**Si falta `arquitectura.csv`:** DETENERSE y derivar a correr arquitectura-seo. No lo generes tú.

**Recipe de consumo (híbrido):**
1. Lee `arquitectura.csv`. Es la fuente de verdad de §3 — referénciala como tal en el spec.
2. Embebe un **resumen compacto derivado**: el árbol de alto nivel (páginas core + hubs por
   dimensión + conteo de spokes por hub) y las páginas dinero (prioridad P1). Márcalo
   *"(derivado de arquitectura.csv; fuente de verdad ahí)"*.
3. Añade la **capa estratégica** que arquitectura-seo NO aporta: por qué esta arquitectura honra la
   restricción dominante (§0.1), qué page-types vigilar en los decision gates, y el racional de
   `accion` (keep/301/fusionar/eliminar) leído de la columna `accion` para sitio existente.
4. §4 internal linking: **consume `enlazado.csv`** igual (referencia + resumen del patrón
   hub-spoke + mix de anchor). No re-derives el enlazado.

**Reglas canónicas / anti-canibalización:** ya están resueltas en el árbol (columnas `page_type`,
`accion`, `intencion`). Aquí solo se **verifica** que el spec las refleja y se anota cualquier
conflicto de intención para los gates; no se re-deciden.

---

## Separación informacional ↔ transaccional
Las queries **informacionales viven en el blog** (pillar + clusters) y **enlazan obligatoriamente a su hub comercial**. Los hubs no se diluyen con contenido informacional. Así el blog alimenta conversión y construye topical authority sin canibalizar el intent transaccional. El árbol ya asigna `page_type` e `intencion` por URL; aquí solo se **verifica** que esa separación se respeta y se anota cualquier mezcla de intent para los gates.

---

## Bilingüe / multi-región (solo si discovery Nivel 1 lo marca)
La estructura de idioma se **decidió en el FRAMING (§2)** y se registró en `enfoque.md`. Aquí no se diseña: se **verifica** y se delega.
- **Verificar** que el árbol (`arquitectura.csv`) refleja la estructura de idioma decidida en el framing (subdirectorio/subdominio/ccTLD) y que hay **paridad por idioma** (cada versión con contenido equivalente, sin ramas thin). Anotar cualquier desajuste para los gates.
- **Criterio estratégico (se conserva):** abrir un idioma solo si habrá contenido completo y mantenido en él — medio sitio traducido = thin + señales mixtas. Mejor un idioma bien que dos a medias.
- **Implementación y auditoría de hreflang** (recíproco, auto-referente por página, `x-default` a la versión principal): `claude-seo:seo-hreflang`. No se diseña aquí.
