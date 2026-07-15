"""Tests TDD para migrar_raiz.py (Task 7 · G5 raíz única).

Fixtures sintéticas en tmp_path: sqlite reales pequeños, sin tocar disco real.
Se importa el script como módulo (`import migrar_raiz`, guion bajo a propósito).
"""
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import migrar_raiz  # noqa: E402


# --------------------------------------------------------------------------- #
# helpers de fixtures
# --------------------------------------------------------------------------- #
def _mk_origen_db(path, gsc_rows=None):
    """seo.db del origen: gsc_daily (tracking) + hallazgos (tracking)."""
    if gsc_rows is None:
        gsc_rows = [("2026-07-01", 10, "/a"),
                    ("2026-07-02", 20, "/b"),
                    ("2026-07-03", 30, "/c")]
    con = sqlite3.connect(str(path))
    con.execute("CREATE TABLE gsc_daily (fecha TEXT, clicks INTEGER, url TEXT)")
    con.executemany("INSERT INTO gsc_daily VALUES (?,?,?)", gsc_rows)
    con.execute("CREATE TABLE hallazgos (id INTEGER, tipo TEXT)")
    con.executemany("INSERT INTO hallazgos VALUES (?,?)", [(1, "orfana")])
    con.commit()
    con.close()


def _mk_stub_db(path, extra_gsc=None):
    """seo.db STUB del destino: geo_checks con AUTOINCREMENT (ejercita
    sqlite_sequence). Opcionalmente una tabla gsc_daily solapada."""
    con = sqlite3.connect(str(path))
    con.execute("CREATE TABLE geo_checks "
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, check_name TEXT)")
    con.executemany("INSERT INTO geo_checks (check_name) VALUES (?)",
                    [("robots",), ("llms",)])
    if extra_gsc is not None:
        con.execute("CREATE TABLE gsc_daily (fecha TEXT, clicks INTEGER, url TEXT)")
        con.executemany("INSERT INTO gsc_daily VALUES (?,?,?)", extra_gsc)
    con.commit()
    con.close()


@pytest.fixture
def roots(tmp_path):
    """Construye origen/ y destino/ sintéticos y devuelve (origen, destino)."""
    origen = tmp_path / "origen"
    destino = tmp_path / "destino"

    # ---- origen (raíz vieja, con tracking real) ----
    (origen / "conexiones").mkdir(parents=True)
    (origen / "conexiones" / "conexiones.json").write_text(
        json.dumps({"slug": "acme", "gsc": "x"}), encoding="utf-8")
    (origen / "conexiones" / "conexiones.md").write_text(
        "# marcador acme\n", encoding="utf-8")
    (origen / "data").mkdir()
    _mk_origen_db(origen / "data" / "seo.db")
    (origen / "data" / "clarity-heatmaps").mkdir()
    (origen / "data" / "clarity-heatmaps" / "a.csv").write_text(
        "x,y\n1,2\n", encoding="utf-8")
    (origen / "clusters.json").write_text(
        json.dumps({"c": [1, 2]}), encoding="utf-8")
    (origen / "plans").mkdir()
    (origen / "plans" / "CHECKLIST-x.md").write_text(
        "- [ ] tarea origen\n", encoding="utf-8")
    (origen / "reportes").mkdir()
    (origen / "reportes" / "r.md").write_text("# reporte\n", encoding="utf-8")

    # ---- destino (raíz nueva, con stub geo_*) ----
    (destino / "conexiones").mkdir(parents=True)
    (destino / "conexiones" / "cwv.json").write_text(
        json.dumps({"cwv": True}), encoding="utf-8")
    (destino / "data").mkdir()
    _mk_stub_db(destino / "data" / "seo.db")

    return origen, destino


def _hash_tree(root):
    out = {}
    for p in sorted(Path(root).rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def _count(db, table):
    con = sqlite3.connect(str(db))
    try:
        return con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
    finally:
        con.close()


def _run(origen, destino, apply=False):
    argv = ["--slug", "acme", "--from", str(origen), "--to", str(destino)]
    argv.append("--apply" if apply else "--dry-run")
    return migrar_raiz.main(argv)


# --------------------------------------------------------------------------- #
# tests
# --------------------------------------------------------------------------- #
def test_dry_run_no_toca_nada(roots):
    origen, destino = roots
    before_o, before_d = _hash_tree(origen), _hash_tree(destino)
    rc = _run(origen, destino, apply=False)
    assert rc == 0
    assert _hash_tree(origen) == before_o
    assert _hash_tree(destino) == before_d


def test_apply_migra_y_merge_geo(roots):
    origen, destino = roots
    origen_files_before = {p.relative_to(origen)
                           for p in origen.rglob("*") if p.is_file()}

    rc = _run(origen, destino, apply=True)
    assert rc == 0

    dest_db = destino / "data" / "seo.db"
    # tracking del origen + geo del stub en la MISMA BD
    assert _count(dest_db, "gsc_daily") == 3
    assert _count(dest_db, "hallazgos") == 1
    assert _count(dest_db, "geo_checks") == 2
    # sqlite_sequence de geo_checks preservado (AUTOINCREMENT llegó a 2)
    con = sqlite3.connect(str(dest_db))
    seq = con.execute("SELECT seq FROM sqlite_sequence WHERE name='geo_checks'").fetchone()
    con.close()
    assert seq is not None and seq[0] == 2

    # cwv.json intacto; conexiones migradas; backup del stub creado
    assert (destino / "conexiones" / "cwv.json").exists()
    assert (destino / "conexiones" / "conexiones.json").exists()
    assert (destino / "conexiones" / "conexiones.md").exists()
    assert (destino / "data" / "seo.db.stub-pre-merge").exists()

    # carpetas y archivos copiados
    assert (destino / "clusters.json").exists()
    assert (destino / "plans" / "CHECKLIST-x.md").exists()
    assert (destino / "reportes" / "r.md").exists()
    assert (destino / "data" / "clarity-heatmaps" / "a.csv").exists()

    # origen neutralizado: conexiones.json -> conexiones.json.pre-merge
    assert not (origen / "conexiones" / "conexiones.json").exists()
    assert (origen / "conexiones" / "conexiones.json.pre-merge").exists()

    # nada borrado del origen: mismo listado salvo el rename
    origen_files_after = {p.relative_to(origen)
                          for p in origen.rglob("*") if p.is_file()}
    expected = (origen_files_before
                - {Path("conexiones") / "conexiones.json"}
                | {Path("conexiones") / "conexiones.json.pre-merge"})
    assert origen_files_after == expected


def test_idempotente(roots, capsys):
    origen, destino = roots
    assert _run(origen, destino, apply=True) == 0
    capsys.readouterr()  # descarta salida de la 1ª corrida

    ho, hd = _hash_tree(origen), _hash_tree(destino)
    rc = _run(origen, destino, apply=True)
    out = capsys.readouterr().out
    assert rc == 0
    assert "NO-OP" in out
    assert _hash_tree(origen) == ho
    assert _hash_tree(destino) == hd


def test_abort_solapamiento(roots):
    origen, destino = roots
    # stub con gsc_daily poblada con filas DISTINTAS -> solapamiento poblado
    (destino / "data" / "seo.db").unlink()
    _mk_stub_db(destino / "data" / "seo.db",
                extra_gsc=[("2099-01-01", 999, "/z")])

    before_d = _hash_tree(destino)
    rc = _run(origen, destino, apply=True)
    assert rc == 2
    # destino byte-idéntico: ni backup ni copia parcial
    assert _hash_tree(destino) == before_d
    assert not (destino / "data" / "seo.db.stub-pre-merge").exists()
    assert not (destino / "conexiones" / "conexiones.json").exists()
    # origen NO neutralizado
    assert (origen / "conexiones" / "conexiones.json").exists()


def test_no_clobber(roots):
    origen, destino = roots
    # destino ya tiene plans\CHECKLIST-x.md con OTRO contenido
    (destino / "plans").mkdir()
    (destino / "plans" / "CHECKLIST-x.md").write_text(
        "- [x] contenido destino\n", encoding="utf-8")

    rc = _run(origen, destino, apply=True)
    assert rc == 0
    # se conserva el del destino
    assert ((destino / "plans" / "CHECKLIST-x.md").read_text(encoding="utf-8")
            == "- [x] contenido destino\n")


def test_conexiones_distinto_aborta(roots):
    origen, destino = roots
    # destino con conexiones.json DIFERENTE
    (destino / "conexiones" / "conexiones.json").write_text(
        json.dumps({"slug": "acme", "gsc": "OTRO"}), encoding="utf-8")

    before_d = _hash_tree(destino)
    rc = _run(origen, destino, apply=True)
    assert rc == 2
    assert _hash_tree(destino) == before_d
    assert not (destino / "data" / "seo.db.stub-pre-merge").exists()
    assert (origen / "conexiones" / "conexiones.json").exists()
