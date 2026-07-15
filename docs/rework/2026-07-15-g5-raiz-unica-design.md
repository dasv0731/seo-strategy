# G5 · Raíz única por cliente — diseño

> Parte del rework del ecosistema SEO por cliente. Precedido por G1 (diseño-secciones→raíz),
> G2 (estrategia.yaml→sitio.yaml), G3 (master consume el árbol), G4 (orquestador enruta al
> ecosistema). Este documento cubre **G5**: retirar la raíz vieja de tracking
> (`Herramientas\SEO Master\<slug>\`) y dejar **una sola raíz por cliente**:
> `C:\Users\Marke\Documents\Respaldo SEO\Clientes\<slug>\`.
> Todos los hechos de disco citados fueron verificados el 2026-07-15.

## Problema

El ecosistema tiene **dos raíces por cliente**:

| Raíz | Qué contiene hoy (metalectro, verificado) |
|---|---|
| `Herramientas\SEO Master\metalectro\` (**VIEJA**, tracking) | `conexiones\conexiones.json` + `conexiones.md` (el marcador que resuelven las skills), `data\seo.db` (**40.542.208 bytes**, 16 tablas, ~150k filas GSC: `gsc_daily` 149.899, `ga4_daily` 8.622, `hallazgos` 1.688, `clarity_daily` 3.360, `clarity_heatmap` 2.771, `url_status` 439, `lb_backlinks` 50, `changes_log` 7…), `data\clarity-heatmaps\`, `clusters.json`, `plans\` (8 `CHECKLIST-*.md` que lee el dashboard + planes de ejecución), `reportes\` (3 auditorías) |
| `Clientes\metalectro\` (estrategia/crawl/vitals) | `estrategia.yaml`, `conexiones\cwv.json`, `data\` (CSVs del crawl + `page_source\` + un `seo.db` de **36.864 bytes**), `cwv\seo.db`, `historico\`, `base\`, `geo\`, `linkbuilding\`, etc. |

Las 10 skills de tracking (seo-setup-cliente, seo-sync, seo-analisis, seo-analisis-gsc,
seo-cambios, seo-dashboard, seo-vitals, arquitectura-seo, geo-audit, linkbuilding) resuelven la
carpeta del cliente subiendo desde cwd hasta hallar `conexiones/conexiones.json`
(`clients.py:17-27` `find_client_dir`, compartido "SHARED v2"), o `--client-dir`, o el fallback
legacy `SEO_WORKSPACE`+slug (`clients.py:39-43`) — **`SEO_WORKSPACE` NO está seteado**, ese
fallback es inerte. Todas usan `db_path(cdir) = cdir/data/seo.db` (`clients.py:55-58`).

**Por qué la BD real sigue en la raíz vieja:** la skill `extraccion`
(`C:\Users\Marke\.claude\skills\extraccion\scripts\crawlear-cliente.py:249-270`) en cada crawl
real hace el baile `data.rename(data_prev)` (L253-254) → `data.mkdir()` vacío (L255) → crawl →
en éxito `shutil.rmtree(data_prev)` (L269-270); en fallo `rmtree(data)` + `data_prev.rename(data)`
(L262-266). Es decir, **borra todo `data\`**, incluyendo cualquier `seo.db` que viva ahí. El
contrato lo declara `extraccion\SKILL.md:70-73`: "`data\` es **transitorio** (cada crawl lo
regenera)". Por eso el tracking nunca pudo mudarse a `Clientes\` (extraccion no corre sobre la
raíz vieja) y seo-vitals lo esquivó poniéndose en `cwv\seo.db`.

**Hecho adicional verificado (no estaba en el supuesto inicial):** el `seo.db` "stub" de
`Clientes\metalectro\data\` **NO está vacío**: contiene 5 tablas `geo_*` de geo-audit
(`geo_runs` 1, `geo_checks` 48, `geo_hallazgos`/`geo_menciones`/`geo_paginas` 0) — **disjuntas**
de las 16 tablas del origen. Un copy/overwrite ciego destruiría esas 49 filas. La migración
las preserva por merge de tablas exclusivas (ver § C).

## Enfoque elegido (decidido con el usuario): **A — allowlist de durables**

Blindar el baile de `data\` en extraccion para que una lista corta de **durables** sobreviva a
cada re-crawl, migrar físicamente el contenido de la raíz vieja a `Clientes\<slug>\` y
neutralizar la raíz vieja (dejarla como backup, sin resolver como cliente).

**Descartado (fuera de alcance):** Enfoque B (sacar lo durable fuera de `data\`), tocar
`db_path`, mover `clarity-heatmaps\` fuera de `data\`, borrar la raíz vieja, y unificar
`cwv\seo.db` en `data\seo.db` (la pregunta original de la entrada G5 en
`contratos-conexiones.md §5` queda explícitamente diferida: seo-vitals sigue en `cwv\seo.db`).

## Diseño

### § A — Blindaje de durables en extraccion (ÚNICO cambio de código en skills)

En `crawlear-cliente.py`:

- **Constante contrato** (junto a `RENOMBRES`, ~L62):
  `DURABLES = ["seo.db", "seo.db-wal", "seo.db-shm", "clarity-heatmaps"]` — archivos o carpetas
  dentro de `data\` que pertenecen al tracking, no al crawl. (`-wal`/`-shm` hoy no existen en
  disco; se listan de forma defensiva por si una conexión SQLite queda en modo WAL.)
- **Helper `_restaurar_durables(src, dst)`**: mueve cada durable existente (archivo o dir) de
  `src` a `dst`; ignora faltantes; si el destino ya tiene ese nombre, no mueve y avisa
  (defensa — no ocurre en el flujo); devuelve la lista de movidos.
- **Rama de éxito** (hoy L253-255 → L269-270): tras `data.mkdir()`, mover durables
  `data_prev → data` **ANTES** del crawl. Así `data_prev` ya no contiene durables y el
  `rmtree(data_prev)` final (L269-270) es seguro. `data\` fresco queda con durables + CSVs
  nuevos del crawl. (La CLI de Screaming Frog escribe sus exports con `--output-folder data
  --overwrite`, L129-131; no colisiona con los nombres de los durables.)
- **Rama de rollback** (crawl falla sin exports, hoy L262-266): mover durables `data →
  data_prev`, luego `rmtree(data)` + `data_prev.rename(data)`. Resultado = CSVs originales +
  durables intactos. (Los durables solo llegan a `data\` fresco vía el move desde `data_prev`,
  así que si `data_prev` no existe, no hay durables que rescatar.)
- **`--saltar-crawl` no necesita blindaje** — verificado: con el flag, el paso 2 se omite por
  completo (L246-247) y el baile rename/rmtree (L249-270) no se ejecuta; `data\` no se toca.
  Un test lo cementa igualmente.
- **El check de `data_prev\` huérfano** (L250-252, corrida interrumpida) se conserva tal cual.

**Contrato documentado en `extraccion\SKILL.md`:** la sección "`data\` es transitorio"
(SKILL.md:70-73) pasa a decir "transitorio **EXCEPTO los durables** listados en `DURABLES`
(seo.db, seo.db-wal, seo.db-shm, clarity-heatmaps\), que cada re-crawl preserva". **Regla:**
si una skill de tracking agrega otro durable dentro de `data\`, se añade a `DURABLES`.

**Tests:** extraccion **no tiene carpeta `tests/`** (verificado: solo `SKILL.md`,
`requirements.txt`, `scripts\`) — se crea de cero calcando el estilo pytest del ecosistema
(seo-sync/seo-dashboard: `conftest.py` con `sys.path.insert`, `tmp_path`, `monkeypatch`).
Como `crawlear-cliente.py` lleva guion, se carga vía `importlib.util.spec_from_file_location`.
Cobertura: unit de `_restaurar_durables` (archivo, dir, faltante, colisión en destino) +
escenario "seo.db + clarity-heatmaps\ sobreviven a un re-crawl simulado" en **ambas ramas**
(éxito y rollback) + `--saltar-crawl` no toca `data\`. El crawl real se stubbea
(monkeypatch de `crawlear`, `correr`, `gui_abierta`, `CLI_PATHS`) — nunca se invoca
Screaming Frog.

### § B — Retoque cosmético en seo-analisis

Docstring de `C:\Users\Marke\.claude\skills\seo-analisis\scripts\_comun.py:1-6` (dice
"Dos raices por cliente: client_dir -> … (Herramientas\SEO Master\<slug>) / crawl_dir -> …
(Clientes\<slug>)") → reescribir a raíz única `Clientes\<slug>` (client_dir y crawl_dir
resuelven a la misma carpeta; `crawl_dir` sigue existiendo como override). **NINGUNA otra de
las 10 skills se toca**: siguen la raíz sola vía `conexiones.json` (el marcador se muda con la
migración). Nota de repos: el instalado de seo-analisis **no** es repo git; su canónico
versionado es `Nuevas skills\Analisis\` (remote `dasv0731/skill-seo-analisis`) — se edita en
ambos y se commitea en el repo dev.

### § C — Migración física: `migrar_raiz.py` (idempotente, dry-run por defecto)

**Ubicación elegida: `Nuevas skills\Estrategia\docs\rework\scripts\migrar_raiz.py`**
(repo `dasv0731/seo-strategy`, junto a estos docs). Razones: (1) es un **one-shot del programa
de rework del ecosistema**, no una capacidad recurrente de ninguna skill — el SKILL.md de
extraccion declara "Solo EXTRACCIÓN" y su tabla de scripts es contrato: un script de migración
lo contaminaría y viajaría a toda máquina que instale la skill; (2) toca dominios que
extraccion no posee (conexiones.json, seo.db, plans, reportes); (3) el repo Estrategia ya
versiona los docs del rework, así el script queda auditado junto a su diseño y plan. El código
**permanente** (blindaje) sí va en extraccion. La alternativa `extraccion/scripts/` se descartó
por lo anterior.

**CLI:** `python migrar_raiz.py --slug <slug> [--from RUTA] [--to RUTA] [--dry-run] [--apply]`.
Sin `--apply` ⇒ dry-run (reporta acciones sin ejecutar). Defaults:
`--from = Herramientas\SEO Master\<slug>`, `--to = Clientes\<slug>` (se crea si no existe —
esacero/golgana/aiotech aún no tienen carpeta en `Clientes\`).

**Pasos:**

1. **Pre-checks.** El origen `…\data\seo.db` abre y pasa `PRAGMA integrity_check` (se hace
   `wal_checkpoint(TRUNCATE)` antes de copiar, por si hay WAL vivo). El stub destino se
   inventaría tabla por tabla: (a) tablas **exclusivas** del stub con filas (hoy: las `geo_*`)
   → se **preservan por merge** (paso 2); (b) tablas **solapadas** con filas en ambos lados →
   **ABORT** con mensaje (decisión humana; hoy no ocurre: los conjuntos son disjuntos).
2. **Copiar `Herramientas\SEO Master\<slug>\` → `Clientes\<slug>\`** (merge cuidadoso, nunca
   clobber de lo ya poblado en destino):
   - `conexiones\conexiones.json` (+ `conexiones.md`, existe) → junto al `cwv.json` ya presente
     (si el destino ya tiene `conexiones.json` idéntico → skip; distinto → abort).
   - `data\seo.db`: respaldar el stub como `data\seo.db.stub-pre-merge` → copiar el origen
     (40,5 MB) encima → re-inyectar en el destino las tablas exclusivas del stub (CREATE desde
     `sqlite_master.sql` + INSERT de filas + ajuste de `sqlite_sequence`).
   - `data\clarity-heatmaps\` (merge archivo a archivo, sin clobber).
   - `clusters.json`, `plans\` (los `CHECKLIST-*.md` que lee `dashboard.py:596-599`),
     `reportes\` (continuidad de reportes previos) — el destino hoy no tiene ninguno de los
     tres; el merge sin clobber cubre re-corridas.
3. **Verificar:** `PRAGMA integrity_check` = ok en destino; conteo de filas por tabla
   origen == destino (las 16) **y** tablas del stub preservadas con sus conteos (geo_checks=48,
   geo_runs=1); tamaño destino ≈ 40,5 MB.
4. **Neutralizar la raíz vieja:** renombrar `Herramientas\…\conexiones\conexiones.json →
   conexiones.json.pre-merge` — deja de resolver como cliente (`find_client_dir` ya no la ve);
   los 40,5 MB y todo lo demás quedan como **BACKUP** hasta que el usuario confirme borrado.
   **NO se borra nada** de la raíz vieja.
5. **Idempotencia:** si el destino ya tiene la BD grande con las tablas de tracking y el origen
   ya está neutralizado → **no-op** con reporte claro (exit 0). Corridas parciales se retoman
   sin dañar (merges sin clobber + backup del stub solo si no existe ya).

### § D — Verificación E2E (solo metalectro en esta sesión)

1. **Dashboard desde la raíz nueva:** `seo-dashboard\scripts\dashboard.py` con
   `--client-dir Clientes\metalectro` abre la BD de 40,5 MB vía `clients.db_path`
   (dashboard.py:1019) y genera `reportes\dashboard.html` con datos GSC reales y los
   checklists de `plans\` (dashboard.py:596-599).
2. **Humo de resolución:** desde `Clientes\metalectro` como cwd, `clients.resolve_dir()`
   (seo-analisis) devuelve esa carpeta; `seo-cambios\scripts\report.py --report heatmap`
   lee las 2.771 filas de `clarity_heatmap` (read-only).
3. **Simulación de la nuke:** correr el baile blindado sobre una **COPIA** del `data\` real y
   confirmar supervivencia de `seo.db` (40,5 MB byte a byte) + `clarity-heatmaps\` en éxito y
   rollback (además de la suite pytest con fixtures sintéticas).
4. **`SEO_WORKSPACE` inerte:** no seteado ni en proceso ni en el entorno de usuario/máquina.

### § E — Alcance, repos y modelos de ejecución

- **Solo metalectro se migra ahora.** El script queda idempotente y listo para esacero,
  golgana y aiotech (existen en la raíz vieja; NO se corren en esta sesión).
- **Repos y commits:** extraccion → repo git en el **instalado**
  `~/.claude/skills/extraccion\` (canónico, remote `dasv0731/skill-extraccion`, rama de
  trabajo); la copia dev `Nuevas skills\Extraccion\` es backup plano → se sincroniza tras el
  commit. seo-analisis → al revés: canónico versionado en `Nuevas skills\Analisis\`.
  migrar_raiz.py + docs + cierre → repo Estrategia (`dasv0731/seo-strategy`).
  **No pushear/mergear sin visto bueno del usuario.**
- **Modelos:** build con subagentes **Opus/high** (subagent-driven: implementer + reviewer por
  task); revisión final de rama con **Fable/xhigh**.

## Cierre del programa de rework

Al terminar, actualizar `contratos-conexiones.md §5`: la entrada **G5** se marca ✅ HECHO con
el alcance real (raíz única + blindaje de durables + migración de metalectro), dejando
constancia explícita de que la unificación de `cwv\seo.db` (el texto original de G5) queda
**diferida** como decisión futura.

## Verificación (cómo sabremos que quedó bien)

- La suite pytest nueva de extraccion pasa: unit de `_restaurar_durables` + escenarios de
  re-crawl simulado (éxito/rollback) + `--saltar-crawl` intacto.
- `test_migrar_raiz.py` pasa: dry-run inocuo, apply completo con merge geo_*, idempotencia
  (segundo apply = no-op), abort por solapamiento, no-clobber.
- Migración real: destino con `gsc_daily` = 149.899 y `geo_checks` = 48 en la MISMA BD;
  `integrity_check` ok; origen neutralizado (`conexiones.json.pre-merge`); nada borrado.
- Dashboard generado desde `Clientes\metalectro` muestra series GSC y checklists de olas.
- La simulación de nuke sobre copia real conserva `seo.db` + `clarity-heatmaps\`.
- Grep de sanidad: `_comun.py` sin `Herramientas\SEO Master`; `SKILL.md` de extraccion declara
  el contrato `DURABLES`.
