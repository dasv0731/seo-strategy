# Tests de regresión del skill

Escenarios ficticios para verificar que el skill produce estrategias correctas en distintos rubros y situaciones. Se corren **antes** de editar el skill (baseline / RED: documentar qué falla) y **después** (GREEN: verificar que la edición lo arregló sin romper lo demás).

## Cómo correr un escenario

Despachar un subagente **fresco** (sin contexto de la edición) con este prompt neutro — idéntico en RED y GREEN para que la comparación sea limpia:

```
Eres un consultor SEO senior. Diseña la estrategia para el cliente de abajo usando
EXCLUSIVAMENTE la metodología del skill en: ~/.claude/skills/seo-master-plan
Lee SKILL.md primero y luego las referencias que el propio skill te indique para este caso.
Aplica la metodología al pie de la letra.

CLIENTE: [pegar el brief del escenario]

ENTREGA (tu mensaje final, máx. 700 palabras, sin preámbulos):
1. Restricción dominante (§0.1)
2. Enfoque de arquitectura, dimensiones/content-types y 6-10 URLs de ejemplo
3. Núcleo del grafo schema (tipos clave, país/idioma)
4. Plan Mes 1: primeras fases EN ORDEN (qué haces primero y por qué)
5. Setup de conversión + tracking (eventos)
6. KPIs y gates
7. Riesgos principales del caso
```

**No** dar pistas al subagente sobre qué se está evaluando.

## Evaluación

Contrastar la salida contra el checklist "Cobertura esperada" del escenario. Un ítem cuenta como cubierto solo si aparece **sustantivamente** (no por mención de pasada).

| Escenario | Ejercita |
|---|---|
| `escenario-migracion-servicios.md` | Playbook de migración/sitio existente, quick wins |
| `escenario-ecommerce.md` | Parametrización vertical, facetas, Product schema, país MX, conversión purchase |
| `escenario-saas.md` | Dimensiones SaaS, comparativas BOFU, GDPR/consent, trial |
| `escenario-local-multisede.md` | Multi-sede real, booking, restaurante, país CO, alcance trimestral |
| `escenario-optimizacion-continua.md` | Sitio sano sin rediseño: quick wins, pruning, canibalización, KPI de crecimiento (variante de `13`) |
