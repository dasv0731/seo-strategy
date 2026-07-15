# G5 · Raíz única por cliente — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Modelos:** cada task se construye con subagentes **Opus/high** (implementer + reviewer por task). Al final, revisión de rama con **Fable/xhigh** (Task 10, Step 4). No pushear/mergear sin visto bueno del usuario.

**Goal:** Raíz única `Clientes\<slug>\`: blindar el baile `data\`→`data_prev`→`rmtree` de extraccion con una allowlist de durables (`seo.db`, `seo.db-wal`, `seo.db-shm`, `clarity-heatmaps`), migrar físicamente la raíz vieja `Herramientas\SEO Master\metalectro\` a `Clientes\metalectro\` con un script idempotente, neutralizar la raíz vieja (backup, sin borrar), y verificar E2E que el ecosistema resuelve y opera desde la raíz nueva.

**Architecture:** Un solo cambio de código en skills: `~/.claude/skills/extraccion/scripts/crawlear-cliente.py` (repo git canónico instalado, remote `dasv0731/skill-extraccion`; la copia `Nuevas skills\Extraccion\` es backup plano que se sincroniza después). Retoque cosmético en `~/.claude/skills/seo-analisis/scripts/_comun.py` (instalado NO-git; canónico versionado = `Nuevas skills\Analisis\`, remote `dasv0731/skill-seo-analisis`). El script one-shot `migrar_raiz.py` vive en `Nuevas skills\Estrategia\docs\rework\scripts\` (repo `dasv0731/seo-strategy`) — es un artefacto del programa de rework, no una capacidad de skill. Diseño aprobado: `2026-07-15-g5-raiz-unica-design.md`.

**Tech Stack:** Python 3 (stdlib: pathlib, shutil, sqlite3, argparse), pytest (estilo del ecosistema: conftest + tmp_path + monkeypatch), Git.

## Global Constraints

- **Enfoque A (allowlist de durables).** Fuera de alcance: Enfoque B (mover durables fuera de `data\`), tocar `db_path` (`clients.py:55-58`), mover heatmaps fuera de `data\`, borrar la raíz vieja, unificar `cwv\seo.db`.
- **Solo se toca código en extraccion** (+ docstring de `_comun.py`). Las otras 9 skills siguen la raíz sola vía `conexiones/conexiones.json`.
- **Solo metalectro se migra en esta sesión.** El script queda listo para esacero/golgana/aiotech (existen en la raíz vieja) pero NO se corren.
- **Nada se borra de la raíz vieja.** Neutralizar = renombrar `conexiones.json → conexiones.json.pre-merge`. Los 40,5 MB quedan de BACKUP hasta confirmación del usuario.
- **Nunca invocar Screaming Frog en tests** (stub/monkeypatch del crawl).
- **Hecho crítico verificado 2026-07-15:** el stub `Clientes\metalectro\data\seo.db` (36.864 bytes) NO está vacío — tiene 5 tablas `geo_*` (geo_runs=1, geo_checks=48, resto 0 filas), **disjuntas** de las 16 tablas del origen (40.542.208 bytes, `PRAGMA integrity_check`=ok: gsc_daily=149.899, ga4_daily=8.622, hallazgos=1.688, clarity_daily=3.360, clarity_heatmap=2.771, url_status=439, lb_backlinks=50, lb_snapshots=2, changes_log=7, rank_tracking/core_keywords/page_content/index_status/lb_prospectos/lb_eventos=0). La migración preserva las `geo_*` por merge de tablas exclusivas.
- **Commits:** extraccion en el instalado (rama `g5-raiz-unica`); seo-analisis en `Nuevas skills\Analisis` (rama `g5-raiz-unica`); script+docs+cierre en Estrategia (rama `g5-raiz-unica`). Preguntar antes de pushear.

---

### Task 1: Ramas de trabajo limpias en los 3 repos

**Files:**
- Ninguno (solo estado git).

**Interfaces:**
- Consumes: nada.
- Produces: ramas `g5-raiz-unica` en extraccion (instalado), Analisis (dev) y Estrategia, con working trees limpios.

- [ ] **Step 1: extraccion (canónico = instalado)**

Run:
```bash
cd ~/.claude/skills/extraccion && git status --short && git branch --show-current
git checkout -b g5-raiz-unica
```
Expected: working tree limpio (verificado 2026-07-15: rama `master`, 1 commit `3ca131d`), nueva rama `g5-raiz-unica`.

- [ ] **Step 2: Analisis (canónico dev de seo-analisis)**

Run:
```bash
cd "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Analisis" && git status --short
git checkout -b g5-raiz-unica
```
Expected: limpio (rama `master`), nueva rama.

- [ ] **Step 3: Estrategia**

Run:
```bash
cd "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Estrategia" && git status --short
git checkout -b g5-raiz-unica
git add docs/rework/2026-07-15-g5-raiz-unica-design.md docs/rework/2026-07-15-g5-raiz-unica-plan.md
git commit -m "docs(rework): G5 raíz única — diseño y plan"
```
Expected: rama `g5-raiz-unica` con los dos docs commiteados (si el tree tenía los docs sin commitear, este commit los captura).

---

### Task 2: [TDD] Infraestructura de tests de extraccion + unit de `_restaurar_durables`

extraccion NO tiene `tests/` (verificado: solo `SKILL.md`, `requirements.txt`, `scripts\`). Se crea calcando el estilo pytest del ecosistema (p.ej. `~/.claude/skills/seo-sync/tests/conftest.py`: `sys.path.insert` + fixtures; aquí además `importlib` porque `crawlear-cliente.py` lleva guion).

**Files:**
- Create: `~/.claude/skills/extraccion/tests/conftest.py`
- Create: `~/.claude/skills/extraccion/tests/test_durables.py`
- Modify: `~/.claude/skills/extraccion/scripts/crawlear-cliente.py` (añadir `DURABLES` + `_restaurar_durables`; hoy L62-69 tiene `RENOMBRES` — la constante nueva va debajo)

**Interfaces:**
- Consumes: rama de Task 1.
- Produces: `DURABLES` y `_restaurar_durables(src, dst)` implementados y con tests verdes; loader reutilizable para Task 3.

- [ ] **Step 1 (RED): Crear `tests/conftest.py` con el loader**

```python
import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def cargar(nombre_archivo, nombre_modulo):
    """Carga un script con guion en el nombre (p.ej. crawlear-cliente.py) como módulo."""
    spec = importlib.util.spec_from_file_location(nombre_modulo, SCRIPTS / nombre_archivo)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre_modulo] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def cc():
    return cargar("crawlear-cliente.py", "crawlear_cliente")
```

Nota: el top-level de `crawlear-cliente.py` hace `sys.stdout.reconfigure(...)` (L39); bajo captura de pytest `sys.stdout` es un `CaptureIO` (subclase de `TextIOWrapper`) y `reconfigure` existe. Si en esta máquina fallara, correr pytest con `-s` o monkeypatchear `sys.stdout` antes de `cargar` — no cambiar el script por esto.

- [ ] **Step 2 (RED): Crear `tests/test_durables.py` con los unit tests**

```python
def test_mueve_archivo(cc, tmp_path):
    src, dst = tmp_path / "src", tmp_path / "dst"
    src.mkdir(); dst.mkdir()
    (src / "seo.db").write_bytes(b"DBREAL")
    movidos = cc._restaurar_durables(src, dst)
    assert (dst / "seo.db").read_bytes() == b"DBREAL"
    assert not (src / "seo.db").exists()
    assert "seo.db" in movidos


def test_mueve_carpeta_con_contenido(cc, tmp_path):
    src, dst = tmp_path / "src", tmp_path / "dst"
    (src / "clarity-heatmaps").mkdir(parents=True); dst.mkdir()
    (src / "clarity-heatmaps" / "heat.csv").write_text("url,clicks\n/a,5\n")
    cc._restaurar_durables(src, dst)
    assert (dst / "clarity-heatmaps" / "heat.csv").read_text() == "url,clicks\n/a,5\n"
    assert not (src / "clarity-heatmaps").exists()


def test_ignora_faltantes(cc, tmp_path):
    src, dst = tmp_path / "src", tmp_path / "dst"
    src.mkdir(); dst.mkdir()
    assert cc._restaurar_durables(src, dst) == []  # sin durables: no-op, sin excepción


def test_no_clobbea_destino_existente(cc, tmp_path):
    src, dst = tmp_path / "src", tmp_path / "dst"
    src.mkdir(); dst.mkdir()
    (src / "seo.db").write_bytes(b"NUEVO")
    (dst / "seo.db").write_bytes(b"YA-ESTABA")
    movidos = cc._restaurar_durables(src, dst)
    assert (dst / "seo.db").read_bytes() == b"YA-ESTABA"  # defensa: no ocurre en el flujo
    assert "seo.db" not in movidos


def test_durables_es_el_contrato(cc):
    assert cc.DURABLES == ["seo.db", "seo.db-wal", "seo.db-shm", "clarity-heatmaps"]
```

Run: `cd ~/.claude/skills/extraccion && python -m pytest tests/test_durables.py -q`
Expected: **FALLA** (AttributeError: no existe `_restaurar_durables` ni `DURABLES`). Confirmar el RED antes de seguir.

- [ ] **Step 3 (GREEN): Implementar en `crawlear-cliente.py`**

Debajo del bloque `RENOMBRES` (tras L69), añadir:

```python
# Durables de tracking dentro de data\ — CONTRATO (ver SKILL.md):
# el baile data->data_prev de cada crawl los preserva. Si una skill de
# tracking agrega otro durable en data\, AÑADIRLO AQUÍ.
DURABLES = ["seo.db", "seo.db-wal", "seo.db-shm", "clarity-heatmaps"]


def _restaurar_durables(src, dst):
    """Mueve cada durable existente (archivo o carpeta) de src a dst.

    Ignora faltantes. Si dst ya tiene ese nombre, no mueve y avisa (defensa;
    no ocurre en el flujo normal). Devuelve la lista de nombres movidos."""
    movidos = []
    for nombre in DURABLES:
        origen = src / nombre
        if not origen.exists():
            continue
        if (dst / nombre).exists():
            print(f"  [!] durable ya existe en destino, no se mueve: {nombre}")
            continue
        shutil.move(str(origen), str(dst / nombre))
        movidos.append(nombre)
    return movidos
```

Run: `python -m pytest tests/test_durables.py -q`
Expected: **5 passed**.

- [ ] **Step 4: Sanidad — el orquestador sigue importable/parseable**

Run: `cd ~/.claude/skills/extraccion && python -c "import ast; ast.parse(open('scripts/crawlear-cliente.py', encoding='utf-8').read()); print('OK')"`
Expected: `OK`.

---

### Task 3: [TDD] Blindar el baile data→data_prev (éxito, rollback, --saltar-crawl)

**Files:**
- Create: `~/.claude/skills/extraccion/tests/test_recrawl_durables.py`
- Modify: `~/.claude/skills/extraccion/scripts/crawlear-cliente.py` (bloque del paso 2: hoy L249-270)

**Interfaces:**
- Consumes: `_restaurar_durables` (Task 2), loader `cc` del conftest.
- Produces: ambas ramas del baile preservan durables; tests de escenario verdes.

- [ ] **Step 1 (RED): Crear `tests/test_recrawl_durables.py`**

Fixture de cliente sintético + monkeypatch del crawl (NUNCA Screaming Frog real). `crawlear` tiene firma `(cli, url, plantilla_cfg, data, proyecto, con_extras)` (L125); `correr` corre scripts hermanos (L106-108) y se stubbea a `0`; `gui_abierta` (L96) a `False`; `CLI_PATHS` (L43-46) a un exe fake que existe.

```python
import sys

import pytest

CSV_VIEJO = "Address,Link Score\nhttps://ejemplo.com/,5\n"


@pytest.fixture
def cliente(tmp_path):
    carpeta = tmp_path / "clientes" / "acme"
    data = carpeta / "data"
    data.mkdir(parents=True)
    (carpeta / "sitio.yaml").write_text("sitio: https://ejemplo.com\nplantilla: estatica\n",
                                        encoding="utf-8")
    plantillas = tmp_path / "clientes" / "_plantillas"
    plantillas.mkdir()
    (plantillas / "plantilla-estatica.seospiderconfig").write_bytes(b"cfg")
    # durables + un export viejo del crawl anterior
    (data / "seo.db").write_bytes(b"DBREAL" * 1000)
    (data / "clarity-heatmaps").mkdir()
    (data / "clarity-heatmaps" / "heat.csv").write_text("k,v\n", encoding="utf-8")
    (data / "internal_html.csv").write_text(CSV_VIEJO, encoding="utf-8")
    return carpeta


@pytest.fixture
def entorno(cc, cliente, tmp_path, monkeypatch):
    fake_cli = tmp_path / "sf-cli.exe"
    fake_cli.write_bytes(b"")
    monkeypatch.setattr(cc, "CLI_PATHS", [str(fake_cli)])
    monkeypatch.setattr(cc, "gui_abierta", lambda: False)
    monkeypatch.setattr(cc, "correr", lambda script, *a: 0)  # extraer-schemas/archivar stub
    monkeypatch.setattr(sys, "argv",
                        ["crawlear-cliente.py", str(cliente), "--sin-archivar"])
    return cc


def test_exito_preserva_durables(entorno, cliente, monkeypatch):
    def crawl_ok(cli, url, plantilla_cfg, data, proyecto, con_extras):
        (data / "internal_html.csv").write_text(
            "Address,Link Score\nhttps://ejemplo.com/,7\n", encoding="utf-8")
        return 0
    monkeypatch.setattr(entorno, "crawlear", crawl_ok)
    assert entorno.main() == 0
    data = cliente / "data"
    assert (data / "seo.db").read_bytes() == b"DBREAL" * 1000        # durable intacto
    assert (data / "clarity-heatmaps" / "heat.csv").exists()          # carpeta durable intacta
    assert "7" in (data / "internal_html.csv").read_text()            # exports NUEVOS
    assert not (cliente / "data_prev").exists()                       # data_prev limpiado


def test_rollback_preserva_durables_y_csvs(entorno, cliente, monkeypatch):
    monkeypatch.setattr(entorno, "crawlear", lambda *a, **k: 1)      # crawl falla sin exports
    with pytest.raises(SystemExit):
        entorno.main()
    data = cliente / "data"
    assert (data / "seo.db").read_bytes() == b"DBREAL" * 1000        # durable intacto
    assert (data / "clarity-heatmaps" / "heat.csv").exists()
    assert (data / "internal_html.csv").read_text() == CSV_VIEJO      # CSVs ORIGINALES
    assert not (cliente / "data_prev").exists()                       # sin residuos


def test_saltar_crawl_no_toca_data(entorno, cliente, monkeypatch):
    monkeypatch.setattr(sys, "argv",
                        ["crawlear-cliente.py", str(cliente), "--saltar-crawl", "--sin-archivar"])
    def bomba(*a, **k):
        raise AssertionError("--saltar-crawl no debe crawlear")
    monkeypatch.setattr(entorno, "crawlear", bomba)
    assert entorno.main() == 0
    data = cliente / "data"
    assert (data / "seo.db").read_bytes() == b"DBREAL" * 1000
    assert (data / "internal_html.csv").read_text() == CSV_VIEJO
    assert not (cliente / "data_prev").exists()
```

Run: `python -m pytest tests/test_recrawl_durables.py -q`
Expected: **RED** — `test_exito_preserva_durables` y `test_rollback_preserva_durables_y_csvs` fallan (hoy el baile borra `seo.db`); `test_saltar_crawl_no_toca_data` ya pasa (L246-247 omite el baile — el test lo cementa).

- [ ] **Step 2 (GREEN): Cablear el blindaje en `main()`**

En el bloque del paso 2 (hoy L249-270), tras `data.mkdir(parents=True, exist_ok=True)` (L255) y ANTES de `rc = crawlear(...)` (L257):

```python
        if prev.exists():
            movidos = _restaurar_durables(prev, data)
            if movidos:
                print("  durables preservados: " + ", ".join(movidos))
```

Y en la rama de fallo (hoy L262-266), ANTES del `shutil.rmtree(data, ignore_errors=True)`:

```python
        if not (data / "internal_html.csv").exists():
            if prev.exists():
                _restaurar_durables(data, prev)   # devolver durables antes de la nuke
            shutil.rmtree(data, ignore_errors=True)
            if prev.exists():
                prev.rename(data)
            fallar(f"El crawl falló (código {rc}). Se restauró el data\\ anterior.")
```

El resto del bloque no cambia: el check de `data_prev\` huérfano (L250-252) y el `rmtree(prev)` final de éxito (L269-270) quedan igual — con los durables ya movidos a `data`, ese `rmtree` es seguro.

Run: `python -m pytest tests/ -q`
Expected: **8 passed** (5 de Task 2 + 3 de escenario).

- [ ] **Step 3: Revisión del diff**

Run: `cd ~/.claude/skills/extraccion && git diff scripts/crawlear-cliente.py`
Expected a ojo: SOLO (a) constante `DURABLES` + helper, (b) move prev→data tras mkdir, (c) rescate data→prev en rollback. Ningún otro cambio de flujo (el `--saltar-crawl`, la validación, los pasos 3-5 intactos).

---

### Task 4: Contrato `DURABLES` en `extraccion\SKILL.md`

**Files:**
- Modify: `~/.claude/skills/extraccion/SKILL.md` (párrafo "`data\` es transitorio", L70-73)

**Interfaces:**
- Consumes: Tasks 2-3 (el contrato ya es real en el código).
- Produces: SKILL.md declara la excepción de durables y la regla de mantenimiento.

- [ ] **Step 1: Reemplazar el párrafo L70-73**

Texto actual (L70-73):
```
`data\` es **transitorio** (cada crawl lo regenera). El archivo histórico son los
CSVs en `historico\<fecha>\` — nunca se archiva HTML: el crawl completo queda en la
base de datos de Screaming Frog (File > Crawls, por proyecto) y se re-exporta por
crawl ID.
```

Reemplazar por:
```
`data\` es **transitorio** (cada crawl lo regenera) — **EXCEPTO los durables de
tracking**, que el baile `data`→`data_prev` de cada crawl preserva (constante
`DURABLES` en `crawlear-cliente.py`): `seo.db`, `seo.db-wal`, `seo.db-shm` y
`clarity-heatmaps\`. **CONTRATO:** si una skill de tracking agrega otro archivo o
carpeta durable dentro de `data\`, hay que añadirlo a `DURABLES` — lo que no esté en
la lista se borra en el siguiente crawl. El archivo histórico son los CSVs en
`historico\<fecha>\` — nunca se archiva HTML: el crawl completo queda en la base de
datos de Screaming Frog (File > Crawls, por proyecto) y se re-exporta por crawl ID.
```

- [ ] **Step 2: Verificar**

Run: `rg -n "DURABLES|EXCEPTO" ~/.claude/skills/extraccion/SKILL.md`
Expected: ambas palabras presentes en la sección del contrato de `data\`.

---

### Task 5: Commit de extraccion + sync del backup plano

**Files:**
- Modify (git): repo `~/.claude/skills/extraccion` (rama `g5-raiz-unica`)
- Modify (copia): `C:\Users\Marke\Documents\Respaldo SEO\Nuevas skills\Extraccion\` (backup plano, sin git)

**Interfaces:**
- Consumes: Tasks 2-4.
- Produces: commit único del blindaje; backup dev sincronizado.

- [ ] **Step 1: Commit en el canónico (instalado)**

```bash
cd ~/.claude/skills/extraccion
git add scripts/crawlear-cliente.py SKILL.md tests/
git commit -m "feat(g5): blindaje de durables en el baile data->data_prev (DURABLES: seo.db, wal, shm, clarity-heatmaps) + contrato en SKILL.md + tests"
git status --short
```
Expected: working tree limpio tras el commit.

- [ ] **Step 2: Sincronizar el backup plano**

```bash
cp "/c/Users/Marke/.claude/skills/extraccion/scripts/crawlear-cliente.py" "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Extraccion/crawlear-cliente.py"
cp "/c/Users/Marke/.claude/skills/extraccion/SKILL.md" "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Extraccion/SKILL.md"
```
Nota: el backup plano NO tiene subcarpeta `scripts\` ni `tests\` (los scripts viven sueltos en su raíz — verificado); copiar los 2 archivos tocados basta.

- [ ] **Step 3: Verificar sync**

Run: `diff "/c/Users/Marke/.claude/skills/extraccion/scripts/crawlear-cliente.py" "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Extraccion/crawlear-cliente.py" && echo SYNC-OK`
Expected: `SYNC-OK`.

---

### Task 6: Docstring de raíz única en `_comun.py` (seo-analisis)

**Files:**
- Modify: `~/.claude/skills/seo-analisis/scripts/_comun.py` (docstring L1-6; instalado, NO-git)
- Modify: `C:\Users\Marke\Documents\Respaldo SEO\Nuevas skills\Analisis\scripts\_comun.py` (canónico git; cabecera idéntica, verificado)

**Interfaces:**
- Consumes: rama `g5-raiz-unica` de Analisis (Task 1).
- Produces: docstring sin mención a la raíz vieja; commit en el repo dev.

- [ ] **Step 1: Editar AMBAS copias**

Texto actual (L1-6, idéntico en ambas):
```python
"""Infraestructura compartida de seo-analisis: resolucion, normalizacion, scoring.

Dos raices por cliente:
  client_dir -> conexiones/conexiones.json + data/seo.db (Herramientas\\SEO Master\\<slug>)
  crawl_dir  -> estrategia.yaml + data\\ + historico\\   (Clientes\\<slug>)
"""
```

Reemplazar por:
```python
"""Infraestructura compartida de seo-analisis: resolucion, normalizacion, scoring.

Raiz unica por cliente (Clientes\\<slug>): client_dir resuelve por
conexiones/conexiones.json + data/seo.db, y crawl_dir (sitio.yaml/estrategia.yaml +
data\\ + historico\\) es la misma carpeta salvo override con --crawl-dir.
"""
```

Solo cambia el docstring — cero cambios de comportamiento (la lógica de `resolver()` L110-127 no se toca).

- [ ] **Step 2: Verificar y commitear**

Run:
```bash
rg -n "SEO Master" ~/.claude/skills/seo-analisis/scripts/_comun.py "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Analisis/scripts/_comun.py" || echo LIMPIO
diff ~/.claude/skills/seo-analisis/scripts/_comun.py "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Analisis/scripts/_comun.py" && echo IDENTICOS
cd "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Analisis"
python -m pytest tests/test_comun.py -q
git add scripts/_comun.py
git commit -m "docs(g5): _comun.py — docstring a raíz única Clientes\\<slug>"
```
Expected: `LIMPIO`, `IDENTICOS`, tests de `_comun` en verde, commit hecho.

---

### Task 7: [TDD] `migrar_raiz.py` — migración idempotente de la raíz vieja

**Files:**
- Create: `Nuevas skills\Estrategia\docs\rework\scripts\migrar_raiz.py`
- Create: `Nuevas skills\Estrategia\docs\rework\scripts\test_migrar_raiz.py`

**Interfaces:**
- Consumes: nada de tasks previas (independiente del blindaje).
- Produces: script CLI probado contra raíces sintéticas, listo para la corrida real (Task 8) y para esacero/golgana/aiotech en el futuro.

**Contrato CLI:**
`python migrar_raiz.py --slug <slug> [--from RUTA] [--to RUTA] [--dry-run] [--apply]`
- Defaults: `--from = C:\Users\Marke\Documents\Respaldo SEO\Herramientas\SEO Master\<slug>`, `--to = C:\Users\Marke\Documents\Respaldo SEO\Clientes\<slug>` (el destino se crea si no existe).
- Sin `--apply` ⇒ **dry-run** (default seguro; `--dry-run` explícito también vale). Exit codes: `0` ok/no-op, `2` abort por pre-check.

**Algoritmo (del diseño § C — implementar tal cual):**
1. **Pre-checks:** el origen `data\seo.db` existe, abre, `PRAGMA wal_checkpoint(TRUNCATE)` + `PRAGMA integrity_check` = ok. Inventario del stub destino (si existe): tablas **exclusivas** con filas → van a merge (hoy: `geo_*`); tablas **solapadas** con filas en ambos lados → **exit 2** con listado (decisión humana). `conexiones.json` ya en destino: idéntico → skip; distinto → exit 2.
2. **Copias (merge sin clobber):** `conexiones\conexiones.json` + `conexiones.md` (existe en el origen — verificado); `data\seo.db` = backup del stub a `data\seo.db.stub-pre-merge` (si no existe ya) → `shutil.copy2` del origen → re-inyectar tablas exclusivas del stub (CREATE desde `sqlite_master.sql` + `INSERT` fila a fila + actualizar `sqlite_sequence` de esas tablas); `data\clarity-heatmaps\`, `plans\`, `reportes\` recursivo archivo-a-archivo sin sobrescribir; `clusters.json` solo si falta (si existe distinto → reportar y conservar destino).
3. **Verificación integrada:** `integrity_check` = ok en destino; conteo por tabla origen == destino; tablas del stub preservadas con sus conteos; tamaño destino ≥ tamaño origen. Falla ⇒ exit 2 SIN neutralizar.
4. **Neutralizar:** rename `origen\conexiones\conexiones.json → conexiones.json.pre-merge`. NO borrar nada.
5. **Idempotencia:** si origen ya neutralizado Y el destino ya tiene las tablas de tracking del origen ⇒ imprimir `[NO-OP] migración ya aplicada` y exit 0 sin tocar nada.
- Dry-run: imprime cada acción con prefijo `[DRY]` sin ejecutar nada.

- [ ] **Step 1 (RED): Escribir `test_migrar_raiz.py`**

Fixtures sintéticas en `tmp_path` (sin tocar disco real): `origen/` con `conexiones\conexiones.json` (`{"slug":"acme", ...}`) + `conexiones.md`, `data\seo.db` (sqlite con `gsc_daily` 3 filas y `hallazgos` 1 fila), `data\clarity-heatmaps\a.csv`, `clusters.json`, `plans\CHECKLIST-x.md`, `reportes\r.md`; `destino/` con `conexiones\cwv.json` y `data\seo.db` stub (sqlite con `geo_checks` 2 filas, `AUTOINCREMENT` para ejercitar `sqlite_sequence`). Importar el script normalmente (`import migrar_raiz` — nombre con guion bajo a propósito). Tests:

1. `test_dry_run_no_toca_nada` — correr sin `--apply`; hash de todos los archivos de ambas raíces idéntico antes/después; exit 0.
2. `test_apply_migra_y_merge_geo` — con `--apply`: destino `seo.db` tiene `gsc_daily`=3 **y** `geo_checks`=2; `cwv.json` intacto; `conexiones.json` + `conexiones.md` presentes; `seo.db.stub-pre-merge` existe; `clusters.json`/`plans\CHECKLIST-x.md`/`reportes\r.md`/`clarity-heatmaps\a.csv` copiados; origen tiene `conexiones.json.pre-merge` y NO `conexiones.json`; nada borrado del origen (mismo listado de archivos, solo el rename).
3. `test_idempotente` — segundo `--apply` sobre el resultado: exit 0, imprime NO-OP, hashes intactos.
4. `test_abort_solapamiento` — origen y stub ambos con `gsc_daily` poblada con filas distintas: exit 2 y destino byte-idéntico (ni backup ni copia parcial).
5. `test_no_clobber` — destino ya tiene `plans\CHECKLIST-x.md` con otro contenido: tras `--apply` se conserva el del destino.
6. `test_conexiones_distinto_aborta` — destino con `conexiones\conexiones.json` diferente: exit 2 sin cambios.

Run: `cd "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Estrategia/docs/rework/scripts" && python -m pytest test_migrar_raiz.py -q`
Expected: **RED** (ModuleNotFoundError / fallos).

- [ ] **Step 2 (GREEN): Implementar `migrar_raiz.py`**

Estructura sugerida (stdlib solamente; el implementador puede ajustar nombres internos manteniendo CLI, algoritmo y tests):
`main()` / `precheck(origen, destino)` / `inventario_db(path)` (dict tabla→filas) / `checkpoint_e_integrity(path)` / `migrar_db(origen_db, destino_db, dry)` (backup + copy2 + merge de exclusivas + sqlite_sequence) / `merge_carpeta(src, dst, dry)` (recursivo, sin clobber, reporta skips) / `copiar_si_falta(src, dst, dry)` / `verificar(origen_db, destino_db, tablas_stub)` / `neutralizar(origen, dry)` / `es_noop(origen, destino)`. Cada acción imprime una línea (`[DRY]`/`[OK]`/`[SKIP]`/`[X]`).

Run: `python -m pytest test_migrar_raiz.py -q`
Expected: **6 passed**.

- [ ] **Step 3: Commit**

```bash
cd "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Estrategia"
git add docs/rework/scripts/migrar_raiz.py docs/rework/scripts/test_migrar_raiz.py
git commit -m "feat(g5): migrar_raiz.py — migración idempotente raíz vieja -> Clientes\\<slug> (merge geo_*, no-clobber, neutralización)"
```

---

### Task 8: Migración real de metalectro (dry-run → apply → verificación)

**PRE-REQUISITO DURO: Task 3 y Task 5 completadas** (el blindaje debe estar commiteado ANTES de poner la BD real bajo `Clientes\metalectro\data\` — si no, el próximo crawl la borraría).

**Files:**
- Read/Write en disco (no repos): `Herramientas\SEO Master\metalectro\` → `Clientes\metalectro\`

**Interfaces:**
- Consumes: `migrar_raiz.py` (Task 7) verde; blindaje commiteado (Task 5).
- Produces: `Clientes\metalectro\` como raíz única con la BD de 40,5 MB; raíz vieja neutralizada como backup.

- [ ] **Step 1: Confirmar blindaje en su sitio (gate)**

Run: `cd ~/.claude/skills/extraccion && git log --oneline -1 && rg -n "DURABLES" scripts/crawlear-cliente.py | head -2`
Expected: commit de Task 5 visible y constante presente. **Si no, DETENERSE.**

- [ ] **Step 2: Dry-run**

Run:
```bash
python "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Estrategia/docs/rework/scripts/migrar_raiz.py" --slug metalectro
```
Expected: reporte `[DRY]` que lista: copiar conexiones.json+conexiones.md, backup del stub + copiar seo.db (40.542.208 bytes) + merge de 5 tablas `geo_*`, clarity-heatmaps\, clusters.json, plans\ (~31 archivos), reportes\ (3), neutralizar origen. **Cero cambios en disco.**

- [ ] **Step 3: Apply**

Run: el mismo comando + `--apply`.
Expected: exit 0, reporte `[OK]` por pieza, verificación integrada en verde.

- [ ] **Step 4: Verificación objetiva post-apply**

Run:
```bash
python - <<'EOF'
import os, sqlite3
db = r"C:\Users\Marke\Documents\Respaldo SEO\Clientes\metalectro\data\seo.db"
c = sqlite3.connect(db)
n = dict((t, c.execute(f'select count(*) from "{t}"').fetchone()[0])
         for (t,) in c.execute("select name from sqlite_master where type='table'"))
assert n["gsc_daily"] == 149899 and n["ga4_daily"] == 8622, n
assert n["hallazgos"] == 1688 and n["clarity_heatmap"] == 2771 and n["url_status"] == 439, n
assert n["geo_checks"] == 48 and n["geo_runs"] == 1, n          # stub preservado
assert c.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert os.path.getsize(db) >= 40_000_000
viejo = r"C:\Users\Marke\Documents\Respaldo SEO\Herramientas\SEO Master\metalectro\conexiones"
assert os.path.exists(os.path.join(viejo, "conexiones.json.pre-merge"))
assert not os.path.exists(os.path.join(viejo, "conexiones.json"))
assert os.path.getsize(os.path.join(os.path.dirname(viejo), "data", "seo.db")) == 40542208  # backup intacto
print("MIGRACION VERIFICADA")
EOF
```
Expected: `MIGRACION VERIFICADA`.

- [ ] **Step 5: Idempotencia real**

Run: repetir el comando de Step 3 (`--apply`).
Expected: `[NO-OP] migración ya aplicada`, exit 0, nada cambia.

---

### Task 9: Verificación E2E desde la raíz nueva (solo metalectro)

**Files:**
- Ninguno permanente (dashboard regenera `Clientes\metalectro\reportes\dashboard.html`; simulación en el scratchpad).

**Interfaces:**
- Consumes: Task 8 aplicada.
- Produces: evidencia de que las skills operan desde `Clientes\metalectro` con la BD real.

- [ ] **Step 1: Resolución de cliente (seo-analisis / clients.py compartido)**

Run (cwd = la carpeta del cliente, para ejercitar `find_client_dir`):
```bash
cd "/c/Users/Marke/Documents/Respaldo SEO/Clientes/metalectro"
python -c "import sys; sys.path.insert(0, r'C:\Users\Marke\.claude\skills\seo-analisis\scripts'); import clients; d = clients.resolve_dir(); print(d); print(clients.db_path(d))"
```
Expected: imprime `...\Clientes\metalectro` y `...\Clientes\metalectro\data\seo.db` (NO la raíz vieja).

- [ ] **Step 2: Dashboard abre la BD de 40,5 MB y renderiza checklists**

Run:
```bash
python "/c/Users/Marke/.claude/skills/seo-dashboard/scripts/dashboard.py" --client-dir "C:\Users\Marke\Documents\Respaldo SEO\Clientes\metalectro"
grep -c "ola" "/c/Users/Marke/Documents/Respaldo SEO/Clientes/metalectro/reportes/dashboard.html"
```
Expected: `dashboard generado: ...Clientes\metalectro\reportes\dashboard.html`; el grep ≥ 1 (checklists `CHECKLIST-ola*.md` de `plans\` renderizados vía `dashboard.py:596-599`); el HTML pesa cientos de KB (series GSC reales, no el stub — `collect_data` conecta vía `clients.db_path`, `dashboard.py:1019`).

- [ ] **Step 3: Humo seo-cambios (read-only contra la BD real)**

Run:
```bash
python "/c/Users/Marke/.claude/skills/seo-cambios/scripts/report.py" --client-dir "C:\Users\Marke\Documents\Respaldo SEO\Clientes\metalectro" --report heatmap
```
Expected: sale data de heatmaps (la tabla `clarity_heatmap` tiene 2.771 filas) — prueba de que resuelve la BD migrada, sin escribir nada.

- [ ] **Step 4: Simular la nuke sobre una COPIA del data\ real**

Run:
```bash
python - <<'EOF'
import shutil, sys
from pathlib import Path
sys.path.insert(0, r"C:\Users\Marke\.claude\skills\extraccion\tests")
from conftest import cargar
cc = cargar("crawlear-cliente.py", "crawlear_cliente_sim")
scratch = Path(r"C:\Users\Marke\AppData\Local\Temp\claude") / "g5-sim"
if scratch.exists(): shutil.rmtree(scratch)
carpeta = scratch / "metalectro"
real = Path(r"C:\Users\Marke\Documents\Respaldo SEO\Clientes\metalectro\data")
shutil.copytree(real, carpeta / "data")
size_db = (carpeta / "data" / "seo.db").stat().st_size
# el baile blindado, tal cual main(): rama de éxito
data, prev = carpeta / "data", carpeta / "data_prev"
data.rename(prev); data.mkdir()
cc._restaurar_durables(prev, data)
(data / "internal_html.csv").write_text("Address\nx\n")   # "crawl" fake
shutil.rmtree(prev)
assert (data / "seo.db").stat().st_size == size_db, "seo.db NO sobrevivió"
assert (data / "clarity-heatmaps").is_dir(), "clarity-heatmaps NO sobrevivió"
print("NUKE SIMULADA: durables sobreviven —", size_db, "bytes")
EOF
```
Expected: `NUKE SIMULADA: durables sobreviven — 40... bytes`. (El `data\` real NO se toca.)

- [ ] **Step 5: SEO_WORKSPACE inerte**

Run (PowerShell):
```powershell
"proc=[{0}] user=[{1}] machine=[{2}]" -f $env:SEO_WORKSPACE, [Environment]::GetEnvironmentVariable('SEO_WORKSPACE','User'), [Environment]::GetEnvironmentVariable('SEO_WORKSPACE','Machine')
```
Expected: los tres vacíos → el fallback legacy de `clients.py:39-43` es inerte; nada puede re-resolver hacia la raíz vieja por esa vía.

---

### Task 10: Cierre del programa + revisión final

**Files:**
- Modify: `Nuevas skills\Estrategia\docs\rework\contratos-conexiones.md` (§5, bloque G5 — hoy L186-187)

**Interfaces:**
- Consumes: Tasks 1-9 verificadas.
- Produces: G5 marcado ✅ con el alcance real; ramas listas para revisión; reporte al usuario.

- [ ] **Step 1: Reescribir el bloque G5 en `contratos-conexiones.md §5`**

Reemplazar el bloque actual (L186-187: "G5 (menor) · seo-vitals usa `cwv\seo.db` aparte…") por:
```markdown
**G5 · Raíz única por cliente. ✅ HECHO (2026-07-15):** retirada la raíz vieja
`Herramientas\SEO Master\<slug>\`. extraccion blinda los durables de `data\` (contrato
`DURABLES` = seo.db, seo.db-wal, seo.db-shm, clarity-heatmaps\ en crawlear-cliente.py + SKILL.md);
`migrar_raiz.py` (docs/rework/scripts/, idempotente) migró metalectro a `Clientes\metalectro\`
(seo.db 40,5 MB con merge de las tablas geo_* del stub, conexiones, clusters.json, plans\,
reportes\, heatmaps) y neutralizó la raíz vieja (`conexiones.json.pre-merge`; queda como backup,
nada borrado). esacero/golgana/aiotech pendientes de correr el mismo script. La unificación de
`cwv\seo.db` en `data\seo.db` (texto original de este gap) queda DIFERIDA como decisión futura.
Diseño y plan en `docs/rework/2026-07-15-g5-raiz-unica-{design,plan}.md`.
```

- [ ] **Step 2: Commit del cierre**

```bash
cd "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Estrategia"
git add docs/rework/contratos-conexiones.md
git commit -m "docs(rework): G5 hecho — raíz única Clientes\\<slug> (metalectro migrado; cwv\\seo.db diferido)"
```

- [ ] **Step 3: Suites completas en verde (gate de cierre)**

Run:
```bash
cd ~/.claude/skills/extraccion && python -m pytest tests/ -q
cd "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Estrategia/docs/rework/scripts" && python -m pytest test_migrar_raiz.py -q
cd "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Analisis" && python -m pytest tests/ -q
```
Expected: todo en verde (8 + 6 + suite existente de Analisis).

- [ ] **Step 4: Revisión final de ramas con Fable/xhigh**

Lanzar el reviewer final (modelo **Fable, xhigh**) sobre los diffs de las 3 ramas `g5-raiz-unica` (extraccion, Analisis, Estrategia) contra su base, con el diseño como spec. Corregir cualquier Critical antes de reportar.

- [ ] **Step 5: Reporte y gate humano de push**

Informar al usuario: estado de las 3 ramas y commits, resultado de la migración (Task 8 Step 4) y del E2E (Task 9), y **preguntar antes de pushear/mergear**. Recordar los pendientes que quedan fuera de esta sesión: correr `migrar_raiz.py` en esacero/golgana/aiotech, borrar la raíz vieja cuando el usuario confirme, y observar el primer re-crawl REAL de metalectro (primer ejercicio del blindaje con Screaming Frog de verdad).

## Self-Review (hecho al escribir el plan)

- **Cobertura del diseño:** § A (blindaje + contrato + tests) → Tasks 2-5. § B (docstring) → Task 6. § C (migración) → Tasks 7-8, incluido el merge de `geo_*` que el supuesto original ("stub sin filas propias") no cubría. § D (E2E) → Task 9 (dashboard, resolución, humo seo-cambios, nuke simulada, SEO_WORKSPACE). § E (alcance/repos/modelos) → Global Constraints + Tasks 1/5/6 + header. Cierre → Task 10.
- **Orden anti-riesgo:** el blindaje (Tasks 2-5) va ANTES de la migración (Task 8) y Task 8 Step 1 lo verifica como gate — la BD real nunca queda bajo `Clientes\` sin blindaje commiteado.
- **file:line citados verificados hoy:** crawlear-cliente.py L39/L43-46/L96/L106-108/L125/L129-131/L246-247/L249-270; SKILL.md L70-73; _comun.py L1-6/L110-127; clients.py L17-27/L39-43/L55-58; dashboard.py L596-599/L1019/L1063-1069; contratos-conexiones.md L186-187.
- **Idempotencia y no-clobber** tienen tests dedicados (Task 7 tests 3-6) y verificación real (Task 8 Step 5).
