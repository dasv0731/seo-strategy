#!/usr/bin/env python3
r"""migrar_raiz.py — migración idempotente de la raíz vieja de un cliente SEO.

Mueve `Herramientas\SEO Master\<slug>\` (raíz VIEJA, con la BD de tracking real)
a `Clientes\<slug>\` (raíz ÚNICA), fusionando la BD grande del origen con el
stub `geo_*` que ya vive en el destino, sin clobber de lo poblado y neutralizando
la raíz vieja al final (queda como backup, nunca se borra nada).

Contrato CLI (Task 7 · G5):
    python migrar_raiz.py --slug <slug> [--from RUTA] [--to RUTA] [--dry-run] [--apply]

- Sin `--apply` => dry-run (default seguro): reporta cada acción con prefijo
  [DRY] sin ejecutar nada.
- Exit codes: 0 ok / no-op ; 2 abort por pre-check o verificación.

stdlib solamente (pathlib, shutil, sqlite3, argparse). Sin invocaciones externas.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sqlite3
import sys
from pathlib import Path

BACKUP_SUFFIX = ".stub-pre-merge"
NEUTRAL_SUFFIX = ".pre-merge"

DEFAULT_FROM = r"C:\Users\Marke\Documents\Respaldo SEO\Herramientas\SEO Master"
DEFAULT_TO = r"C:\Users\Marke\Documents\Respaldo SEO\Clientes"


# --------------------------------------------------------------------------- #
# salida
# --------------------------------------------------------------------------- #
def _log(prefix: str, msg: str) -> None:
    print(f"[{prefix}] {msg}")


# --------------------------------------------------------------------------- #
# sqlite helpers
# --------------------------------------------------------------------------- #
def _connect_ro(path: Path) -> sqlite3.Connection:
    """Conexión estrictamente de solo-lectura (no crea -wal/-shm ni journal)."""
    uri = path.resolve().as_uri()
    return sqlite3.connect(f"{uri}?mode=ro", uri=True)


def inventario_db(path: Path) -> dict[str, int]:
    """Devuelve {tabla_de_usuario: nº_filas} (excluye tablas internas sqlite_*)."""
    con = _connect_ro(path)
    try:
        tablas = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
        return {t: con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
                for t in tablas}
    finally:
        con.close()


def checkpoint_e_integrity(path: Path, do_checkpoint: bool) -> bool:
    """integrity_check == ok. Con do_checkpoint hace wal_checkpoint(TRUNCATE)
    (escribe: solo en apply, justo antes de copiar)."""
    if do_checkpoint:
        con = sqlite3.connect(str(path))
        try:
            con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            con.commit()
        finally:
            con.close()
    con = _connect_ro(path)
    try:
        row = con.execute("PRAGMA integrity_check").fetchone()
        return bool(row) and row[0] == "ok"
    finally:
        con.close()


def _seq_map(con: sqlite3.Connection) -> dict[str, int]:
    """Contenido de sqlite_sequence (vacío si la tabla no existe)."""
    try:
        return {r[0]: r[1] for r in con.execute(
            "SELECT name, seq FROM sqlite_sequence")}
    except sqlite3.OperationalError:
        return {}


def _reinyectar_exclusivas(backup_db: Path, destino_db: Path,
                           tablas: list[str]) -> None:
    """Re-crea en destino_db las tablas exclusivas del stub (CREATE desde
    sqlite_master.sql + INSERT fila a fila + ajuste de sqlite_sequence)."""
    src = sqlite3.connect(str(backup_db))
    dst = sqlite3.connect(str(destino_db))
    try:
        for t in tablas:
            row = src.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
                (t,)).fetchone()
            if not row or not row[0]:
                continue
            dst.execute(row[0])  # CREATE (con AUTOINCREMENT crea sqlite_sequence)
            cols = [r[1] for r in src.execute(f'PRAGMA table_info("{t}")')]
            collist = ",".join(f'"{c}"' for c in cols)
            placeholders = ",".join("?" * len(cols))
            filas = src.execute(f'SELECT {collist} FROM "{t}"').fetchall()
            if filas:
                dst.executemany(
                    f'INSERT INTO "{t}" ({collist}) VALUES ({placeholders})',
                    filas)
            # índices / triggers propios de la tabla
            for (iname, isql) in src.execute(
                    "SELECT name, sql FROM sqlite_master "
                    "WHERE type IN ('index','trigger') AND tbl_name=? "
                    "AND sql IS NOT NULL", (t,)):
                try:
                    dst.execute(isql)
                except sqlite3.OperationalError as err:
                    _log("X", f"no se pudo recrear índice/trigger {iname}: {err}")
        # sqlite_sequence explícito (fiel al stub aun con borrados previos)
        seqs = _seq_map(src)
        for t in tablas:
            if t not in seqs:
                continue
            cur = dst.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' "
                "AND name='sqlite_sequence'").fetchone()
            if not cur:
                continue  # sin tabla AUTOINCREMENT no hay sqlite_sequence
            exists = dst.execute(
                "SELECT 1 FROM sqlite_sequence WHERE name=?", (t,)).fetchone()
            if exists:
                dst.execute("UPDATE sqlite_sequence SET seq=? WHERE name=?",
                            (seqs[t], t))
            else:
                dst.execute("INSERT INTO sqlite_sequence(name, seq) VALUES(?,?)",
                            (t, seqs[t]))
        dst.commit()
    finally:
        src.close()
        dst.close()


# --------------------------------------------------------------------------- #
# rutas del cliente
# --------------------------------------------------------------------------- #
def _p(root: Path, *parts: str) -> Path:
    return root.joinpath(*parts)


def _origen_db(origen: Path) -> Path:
    return _p(origen, "data", "seo.db")


def _destino_db(destino: Path) -> Path:
    return _p(destino, "data", "seo.db")


def _backup_db(destino: Path) -> Path:
    return _p(destino, "data", "seo.db" + BACKUP_SUFFIX)


def _stub_ref(destino: Path) -> Path | None:
    """La fuente de verdad del stub original: el backup si existe (re-corridas
    parciales), si no la BD del destino, si no None."""
    bak = _backup_db(destino)
    if bak.exists():
        return bak
    ddb = _destino_db(destino)
    if ddb.exists():
        return ddb
    return None


# --------------------------------------------------------------------------- #
# idempotencia
# --------------------------------------------------------------------------- #
def es_noop(origen: Path, destino: Path) -> bool:
    """True si la migración ya se aplicó: origen neutralizado (sin
    conexiones.json, con .pre-merge) Y destino con las tablas de tracking."""
    cj = _p(origen, "conexiones", "conexiones.json")
    neutral = _p(origen, "conexiones", "conexiones.json" + NEUTRAL_SUFFIX)
    neutralizado = (not cj.exists()) and neutral.exists()
    if not neutralizado:
        return False
    ddb = _destino_db(destino)
    odb = _origen_db(origen)
    if not ddb.exists() or not odb.exists():
        return False
    try:
        inv_o = inventario_db(odb)
        inv_d = inventario_db(ddb)
    except sqlite3.Error:
        return False
    # todas las tablas de tracking del origen están (pobladas) en el destino
    return all(t in inv_d and inv_d[t] >= n for t, n in inv_o.items() if n > 0)


# --------------------------------------------------------------------------- #
# pre-checks (SOLO lectura: nunca escribe; corre antes de cualquier mutación)
# --------------------------------------------------------------------------- #
def precheck(origen: Path, destino: Path) -> dict:
    """Devuelve dict con ok/reason y el contexto para apply.
    Ordena todas las comprobaciones que pueden abortar ANTES de escribir nada."""
    odb = _origen_db(origen)
    if not odb.exists():
        return {"ok": False, "reason": f"no existe la BD del origen: {odb}"}

    if not checkpoint_e_integrity(odb, do_checkpoint=False):
        return {"ok": False, "reason": f"integrity_check FALLA en el origen: {odb}"}

    inv_origen = inventario_db(odb)

    stub = _stub_ref(destino)
    inv_stub = inventario_db(stub) if stub is not None else {}

    # clasificación por PRESENCIA de nombre (no por conteo del origen): una tabla
    # poblada en el stub cuyo nombre TAMBIÉN existe en el origen es solapamiento
    # aunque el origen la tenga con 0 filas — copiar el origen encima perdería
    # las filas del stub en silencio. Decisión humana => abort atómico.
    exclusivas = sorted(t for t, n in inv_stub.items()
                        if n > 0 and t not in inv_origen)
    solapadas = sorted(t for t, n in inv_stub.items()
                       if n > 0 and t in inv_origen)
    if solapadas:
        return {"ok": False,
                "reason": ("tablas del stub pobladas cuyo nombre también existe "
                           f"en el origen (decisión humana): {', '.join(solapadas)}")}

    # conexiones.json
    ocj = _p(origen, "conexiones", "conexiones.json")
    dcj = _p(destino, "conexiones", "conexiones.json")
    if dcj.exists() and ocj.exists():
        if dcj.read_bytes() != ocj.read_bytes():
            return {"ok": False,
                    "reason": f"conexiones.json distinto en destino: {dcj}"}

    return {"ok": True, "reason": None,
            "inv_origen": inv_origen, "inv_stub": inv_stub,
            "exclusivas": exclusivas, "stub": stub}


# --------------------------------------------------------------------------- #
# operaciones de copia
# --------------------------------------------------------------------------- #
def copiar_si_falta(src: Path, dst: Path, dry: bool) -> None:
    """Copia src->dst solo si falta. Si existe idéntico -> SKIP. Si existe
    distinto -> conserva el destino y avisa (no clobber)."""
    if not src.exists():
        return
    rel = dst.name
    if dst.exists():
        if dst.read_bytes() == src.read_bytes():
            _log("SKIP", f"{rel} ya presente e idéntico")
        else:
            _log("X", f"{rel} existe con distinto contenido -> se conserva el destino")
        return
    if dry:
        _log("DRY", f"copiar {src} -> {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    _log("OK", f"copiado {rel}")


def merge_carpeta(src: Path, dst: Path, dry: bool) -> None:
    """Merge recursivo archivo-a-archivo sin clobber (conserva lo del destino)."""
    if not src.exists():
        return
    for f in sorted(src.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(src)
        target = dst / rel
        if target.exists():
            _log("SKIP", f"{src.name}/{rel} ya existe en destino")
            continue
        if dry:
            _log("DRY", f"copiar {src.name}/{rel}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, target)
        _log("OK", f"{src.name}/{rel}")


def migrar_db(origen: Path, destino: Path, exclusivas: list[str],
              dry: bool) -> None:
    """Backup del stub -> checkpoint origen -> copy2 del origen encima ->
    re-inyectar tablas exclusivas del stub (desde el backup)."""
    odb = _origen_db(origen)
    ddb = _destino_db(destino)
    bak = _backup_db(destino)

    if dry:
        if ddb.exists() and not bak.exists():
            _log("DRY", f"backup del stub -> {bak.name}")
        _log("DRY", f"checkpoint origen + copy2 {odb} -> {ddb}")
        if exclusivas:
            _log("DRY", f"re-inyectar tablas exclusivas del stub: {', '.join(exclusivas)}")
        return

    ddb.parent.mkdir(parents=True, exist_ok=True)

    # 1) backup del stub (solo si no existe ya) — fuente de las exclusivas
    if ddb.exists() and not bak.exists():
        shutil.copy2(ddb, bak)
        _log("OK", f"backup del stub -> {bak.name}")

    # 2) checkpoint del origen (pliega WAL) antes de copiar
    if not checkpoint_e_integrity(odb, do_checkpoint=True):
        raise RuntimeError("integrity_check FALLA en el origen tras checkpoint")

    # 3) copiar la BD grande del origen encima del destino
    shutil.copy2(odb, ddb)
    _log("OK", f"copiada la BD del origen -> {ddb}")

    # 4) re-inyectar las tablas exclusivas del stub desde el backup
    if exclusivas and bak.exists():
        _reinyectar_exclusivas(bak, ddb, exclusivas)
        _log("OK", f"re-inyectadas tablas exclusivas del stub: {', '.join(exclusivas)}")


def verificar(origen: Path, destino: Path, inv_origen: dict,
              inv_stub: dict, exclusivas: list[str]) -> bool:
    """integrity_check destino ok; conteos origen==destino; exclusivas del stub
    preservadas; tamaño destino >= origen."""
    odb, ddb = _origen_db(origen), _destino_db(destino)
    if not checkpoint_e_integrity(ddb, do_checkpoint=False):
        _log("X", "integrity_check FALLA en el destino")
        return False
    inv_d = inventario_db(ddb)
    for t, n in inv_origen.items():
        if inv_d.get(t) != n:
            _log("X", f"conteo {t}: origen={n} destino={inv_d.get(t)}")
            return False
    for t in exclusivas:
        if inv_d.get(t) != inv_stub.get(t):
            _log("X", f"tabla del stub {t} no preservada: "
                      f"stub={inv_stub.get(t)} destino={inv_d.get(t)}")
            return False
    if ddb.stat().st_size < odb.stat().st_size:
        _log("X", "tamaño destino < tamaño origen")
        return False
    _log("OK", "verificación integrada: integrity_check + conteos + tamaño")
    return True


def neutralizar(origen: Path, dry: bool) -> None:
    """Renombra origen/conexiones/conexiones.json -> conexiones.json.pre-merge.
    NO borra nada; la raíz vieja queda como backup."""
    cj = _p(origen, "conexiones", "conexiones.json")
    dest = _p(origen, "conexiones", "conexiones.json" + NEUTRAL_SUFFIX)
    if not cj.exists():
        _log("SKIP", "origen ya neutralizado (sin conexiones.json)")
        return
    if dry:
        _log("DRY", f"neutralizar: {cj.name} -> {dest.name}")
        return
    os.replace(cj, dest)
    _log("OK", f"neutralizado: {cj.name} -> {dest.name}")


# --------------------------------------------------------------------------- #
# orquestación
# --------------------------------------------------------------------------- #
def _ejecutar(origen: Path, destino: Path, dry: bool) -> int:
    # 0) idempotencia: ya migrado -> no-op
    if es_noop(origen, destino):
        _log("NO-OP", "migración ya aplicada (origen neutralizado + destino con tracking)")
        return 0

    # 1) pre-checks (solo lectura; abortan sin escribir)
    pc = precheck(origen, destino)
    if not pc["ok"]:
        _log("X", f"ABORT pre-check: {pc['reason']}")
        return 2

    exclusivas = pc["exclusivas"]
    inv_origen = pc["inv_origen"]
    inv_stub = pc["inv_stub"]

    if dry:
        _log("DRY", f"destino: {destino}  (se crearía si falta)")
        migrar_db(origen, destino, exclusivas, dry=True)
        copiar_si_falta(_p(origen, "conexiones", "conexiones.json"),
                        _p(destino, "conexiones", "conexiones.json"), dry=True)
        copiar_si_falta(_p(origen, "conexiones", "conexiones.md"),
                        _p(destino, "conexiones", "conexiones.md"), dry=True)
        merge_carpeta(_p(origen, "data", "clarity-heatmaps"),
                      _p(destino, "data", "clarity-heatmaps"), dry=True)
        merge_carpeta(_p(origen, "plans"), _p(destino, "plans"), dry=True)
        merge_carpeta(_p(origen, "reportes"), _p(destino, "reportes"), dry=True)
        copiar_si_falta(_p(origen, "clusters.json"),
                        _p(destino, "clusters.json"), dry=True)
        neutralizar(origen, dry=True)
        _log("DRY", "fin dry-run (nada modificado)")
        return 0

    # 2) apply
    destino.mkdir(parents=True, exist_ok=True)
    migrar_db(origen, destino, exclusivas, dry=False)
    copiar_si_falta(_p(origen, "conexiones", "conexiones.json"),
                    _p(destino, "conexiones", "conexiones.json"), dry=False)
    copiar_si_falta(_p(origen, "conexiones", "conexiones.md"),
                    _p(destino, "conexiones", "conexiones.md"), dry=False)
    merge_carpeta(_p(origen, "data", "clarity-heatmaps"),
                  _p(destino, "data", "clarity-heatmaps"), dry=False)
    merge_carpeta(_p(origen, "plans"), _p(destino, "plans"), dry=False)
    merge_carpeta(_p(origen, "reportes"), _p(destino, "reportes"), dry=False)
    copiar_si_falta(_p(origen, "clusters.json"),
                    _p(destino, "clusters.json"), dry=False)

    # 3) verificación (falla => exit 2 SIN neutralizar)
    if not verificar(origen, destino, inv_origen, inv_stub, exclusivas):
        _log("X", "ABORT verificación: NO se neutraliza el origen")
        return 2

    # 4) neutralizar la raíz vieja
    neutralizar(origen, dry=False)
    _log("OK", "migración completa")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Migración idempotente de la raíz vieja de un cliente SEO.")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--from", dest="frm", default=None,
                    help="raíz vieja (default: Herramientas\\SEO Master\\<slug>)")
    ap.add_argument("--to", dest="to", default=None,
                    help="raíz nueva (default: Clientes\\<slug>)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)

    origen = Path(args.frm) if args.frm else Path(DEFAULT_FROM) / args.slug
    destino = Path(args.to) if args.to else Path(DEFAULT_TO) / args.slug
    dry = args.dry_run or not args.apply  # default seguro; ante ambos, dry gana

    _log("DRY" if dry else "OK",
         f"slug={args.slug}  from={origen}  to={destino}  modo={'DRY-RUN' if dry else 'APPLY'}")
    try:
        return _ejecutar(origen, destino, dry)
    except Exception as exc:  # noqa: BLE001 — fallo controlado -> exit 2
        _log("X", f"ABORT excepción: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
