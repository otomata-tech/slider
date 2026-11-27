"""Datapack Excel à la charte : Claude décrit le contenu, le moteur fait la forme.

Un datapack se décrit en JSON (dict Python) : des onglets, chacun avec ses colonnes
et ses lignes. Chaque ligne a un `kind` dont le style vient de la charte
(`tokens.json#excel.rows`) : le moteur ne connaît ni couleur ni police. Les
formules s'écrivent avec des clés de ligne, résolues au rendu :

    {ca}            ligne « ca », même colonne, même onglet
    {ca@24}         ligne « ca », colonne de la période « 24 »
    {Lead P&L!ca}   ligne « ca » de l'onglet « Lead P&L », même période

Tout est vérifié avant d'écrire une cellule, et chaque erreur dit où elle est :
clé inconnue, source hors liste, fonction Excel non autorisée par la charte,
référence de cellule écrite en dur, nombre de valeurs faux… Le classeur
produit n'a aucune cellule fusionnée et se recalcule à l'ouverture.

Usage :
    from lib.charte import Charte
    from lib.datapack import render
    wb = render(spec, Charte.load("blank"))
    wb.save("datapack.xlsx")
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import column_index_from_string, get_column_letter
from openpyxl.workbook.properties import CalcProperties

from .charte import Charte

LAYOUT_KINDS = {"spacer", "dots", "footnote", "text"}   # lignes sans valeurs
COLUMN_KINDS = {"value", "var", "gap", "note"}
VAR_MODES = {"pct", "pp", "abs", "cagr"}
REF_RE = re.compile(r"\{([^{}]+)\}")
FUNC_RE = re.compile(r"([A-Za-z][A-Za-z0-9_.]*)\s*\(")
RAW_CELL_RE = re.compile(r"(?<![A-Za-z0-9_\"'!])\$?[A-Za-z]{1,3}\$?\d+(?![A-Za-z0-9_(])")


class DatapackError(ValueError):
    """Spec invalide : `errors` liste chaque problème, localisé (onglet, ligne)."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("datapack invalide :\n- " + "\n- ".join(errors))


# --------------------------------------------------------------------------- charte

@dataclass
class _Style:
    """Accès à la section `excel` de la charte, couleurs résolues en hex."""

    charte: Charte
    cfg: dict = field(init=False)

    def __post_init__(self):
        cfg = self.charte.tokens.get("excel")
        if not cfg:
            raise KeyError(f"charte '{self.charte.name}' has no 'excel' section")
        self.cfg = cfg

    def hex(self, key: str | None) -> str | None:
        if key is None:
            return None
        return self.charte.color_hex(key).lstrip("#").upper()

    @property
    def font(self) -> str:
        return self.cfg.get("font") or self.charte.font_primary

    @property
    def size(self) -> float:
        return float(self.cfg["size"])

    def F(self, color: str | None = None, bold=False, italic=False) -> Font:
        return Font(name=self.font, size=self.size, bold=bold, italic=italic, color=self.hex(color) or "000000")

    def fill(self, color: str | None) -> PatternFill | None:
        return PatternFill("solid", fgColor=self.hex(color)) if color else None

    def side(self, color: str, style: str = "thin") -> Side:
        return Side(style=style, color=self.hex(color))


# --------------------------------------------------------------------------- validation

def _formula_errors(formula: str, where: str, allowed: set[str], raw_refs: bool = True) -> list[str]:
    errors = []
    bare = REF_RE.sub("0", formula[1:])
    bare = re.sub(r'"[^"]*"', '""', bare)
    for name in FUNC_RE.findall(bare):
        if name.upper() not in allowed:
            errors.append(f"{where} : fonction {name.upper()} non autorisée par la charte "
                          f"(autorisées : {', '.join(sorted(allowed)) or 'aucune'})")
    if raw_refs and (m := RAW_CELL_RE.search(bare)):
        errors.append(f"{where} : référence de cellule « {m.group()} » écrite en dur, utiliser {{clé}}")
    return errors


def validate(spec: dict, charte: Charte) -> list[str]:
    """Toutes les erreurs de la spec, sans rien rendre. Liste vide = rendable."""
    st = _Style(charte)
    rows_cfg, allowed = st.cfg["rows"], {f.upper() for f in st.cfg.get("functions", [])}
    sources = set(st.cfg.get("sources", []))
    errors: list[str] = []
    for mode, tpl in st.cfg["variations"].items():   # la charte doit respecter ses propres règles
        errors += _formula_errors(tpl.format(cur="A1", prev="A2", years=1), f"charte, variation « {mode} »",
                                  allowed, raw_refs=False)
    sheets = spec.get("sheets") or []
    if not sheets:
        return errors + ["aucun onglet (`sheets` vide)"]
    keys: dict[str, set[str]] = {}
    periods: dict[str, set[str]] = {}
    for s in sheets:
        name = s.get("name", "")
        if not name or len(name) > 31 or re.search(r"[\[\]:*?/\\]", name):
            errors.append(f"onglet « {name} » : nom vide, trop long (31 max) ou avec un caractère interdit")
        if name in keys:
            errors.append(f"onglet « {name} » en double")
        keys[name] = set()
        periods[name] = {c.get("period") for c in s.get("columns", []) if c.get("kind") == "value"}
    for s in sheets:
        name = s.get("name", "")
        cols = s.get("columns") or []
        values = [c for c in cols if c.get("kind") == "value"]
        if not values:
            errors.append(f"{name} : aucune colonne de valeurs")
        for c in cols:
            if c.get("kind") not in COLUMN_KINDS:
                errors.append(f"{name} : colonne de type « {c.get('kind')} » inconnu ({', '.join(sorted(COLUMN_KINDS))})")
            if c.get("kind") == "value" and not c.get("period"):
                errors.append(f"{name} : colonne de valeurs sans `period`")
            if c.get("kind") == "var":
                for bout in ("from", "to"):
                    if c.get(bout) not in periods[name]:
                        errors.append(f"{name} : variation « {c.get('header')} » : période {bout} « {c.get(bout)} » inconnue")
                if c.get("force_abs") is not None and not isinstance(c.get("force_abs"), bool):
                    errors.append(f"{name} : variation « {c.get('header')} » : force_abs doit être true ou false")
        for g in s.get("groups", []):
            for bout in ("from", "to"):
                if g.get(bout) not in periods[name]:
                    errors.append(f"{name} : surtitre « {g.get('text')} » : période « {g.get(bout)} » inconnue")
        if s.get("title") is None:
            errors.append(f"{name} : `title` manquant")
        for i, r in enumerate(s.get("rows") or [], 1):
            where = f"{name}, ligne {i} ({r.get('label') or r.get('kind')})"
            kind = r.get("kind")
            if kind not in rows_cfg and kind not in LAYOUT_KINDS:
                errors.append(f"{where} : type « {kind} » inconnu de la charte "
                              f"({', '.join(sorted(set(rows_cfg) | LAYOUT_KINDS))})")
                continue
            if key := r.get("key"):
                if key in keys[name]:
                    errors.append(f"{where} : clé « {key} » en double")
                keys[name].add(key)
            if kind in LAYOUT_KINDS:
                continue
            src = r.get("source")
            if src is not None and src not in sources:
                errors.append(f"{where} : source « {src} » hors liste ({' ; '.join(sorted(sources))})")
            if r.get("var") is not None and r["var"] not in VAR_MODES:
                errors.append(f"{where} : variation « {r['var']} » inconnue ({', '.join(sorted(VAR_MODES))})")
            if (fmt := r.get("format")) is not None and fmt not in st.cfg["formats"]:
                errors.append(f"{where} : format « {fmt} » inconnu de la charte")
            vals = r.get("values")
            if isinstance(vals, list) and len(vals) != len(values):
                errors.append(f"{where} : {len(vals)} valeurs pour {len(values)} colonnes de valeurs")
            formulas = [vals] if isinstance(vals, str) else [v for v in vals or [] if isinstance(v, str) and v.startswith("=")]
            if isinstance(vals, str) and not vals.startswith("="):
                errors.append(f"{where} : `values` texte doit être une formule commençant par « = »")
            for f in formulas:
                errors += _formula_errors(f, where, allowed)
    # références, une fois toutes les clés connues
    for s in sheets:
        name = s.get("name", "")
        for i, r in enumerate(s.get("rows") or [], 1):
            vals = r.get("values")
            formulas = [vals] if isinstance(vals, str) else [v for v in vals or [] if isinstance(v, str) and v.startswith("=")]
            for f in formulas:
                for ref in REF_RE.findall(f):
                    target, key, period = _parse_ref(ref, name)
                    where = f"{name}, ligne {i} ({r.get('label') or r.get('kind')})"
                    if target not in keys:
                        errors.append(f"{where} : onglet « {target} » inconnu dans {{{ref}}}")
                    elif key not in keys[target]:
                        errors.append(f"{where} : clé « {key} » inconnue dans {{{ref}}}")
                    elif period is not None and period not in periods[target]:
                        errors.append(f"{where} : période « {period} » inconnue dans {{{ref}}}")
                    elif target != name and period is None and not periods[name] <= periods[target]:
                        errors.append(f"{where} : {{{ref}}} : l'onglet « {target} » n'a pas toutes les périodes de « {name} »")
    return errors


def _parse_ref(ref: str, sheet: str) -> tuple[str, str, str | None]:
    target, _, rest = ref.rpartition("!")
    key, _, period = rest.partition("@")
    return (target or sheet), key.strip(), (period.strip() or None)


# --------------------------------------------------------------------------- rendu

class _Sheet:
    def __init__(self, book: "_Book", spec: dict):
        self.book, self.spec, self.st = book, spec, book.st
        lay = self.st.cfg["layout"]
        self.name = spec["name"]
        self.c_src = column_index_from_string(lay["source_col"])
        self.c_rule = column_index_from_string(lay["rule_col"])
        self.c_label = column_index_from_string(lay["label_col"])
        self.cols = [dict(c) for c in spec["columns"]]
        for j, c in enumerate(self.cols):
            c["L"] = get_column_letter(self.c_label + 1 + j)
        self.period_col = {c["period"]: c["L"] for c in self.cols if c["kind"] == "value"}
        self.value_cols = [c for c in self.cols if c["kind"] == "value"]
        # numérotation : titre, [espace, surtitres], entête, espace, lignes
        r = lay["title_row"]
        self.r_title = r
        self.r_groups = None
        if spec.get("groups"):
            r += 2
            self.r_groups = r
        self.r_head = r + 1
        r = self.r_head + 1
        self.rows = []
        for row in spec["rows"]:
            r += 1
            self.rows.append((r, row))
        self.keys = {row["key"]: r for r, row in self.rows if row.get("key")}
        self.last_row = r

    # ---- formules
    def resolve(self, formula: str, col: dict) -> str:
        def rep(m):
            target, key, period = _parse_ref(m.group(1), self.name)
            sh = self.book.sheets[target]
            letter = sh.period_col[period or col["period"]]
            prefix = "" if sh is self else "'%s'!" % target.replace("'", "''")
            return f"{prefix}{letter}{sh.keys[key]}"
        return REF_RE.sub(rep, formula)

    def checked(self, formula: str, where: str) -> str:
        """Toute formule écrite, y compris celles du moteur, passe par la liste de la charte."""
        errs = _formula_errors(formula, where, self.book.allowed, raw_refs=False)
        if errs:
            raise DatapackError(errs)
        return formula

    # ---- rendu
    def render(self, wb: Workbook):
        st, lay, ws = self.st, self.st.cfg["layout"], wb.create_sheet(self.name)
        self.ws = ws
        ws.sheet_view.showGridLines = bool(lay.get("gridlines", False))
        ws.sheet_view.zoomScale = lay.get("zoom", 100)
        if tab := self.spec.get("tab_color") or lay.get("tab_color"):
            ws.sheet_properties.tabColor = st.hex(tab)
        w = lay["widths"]
        ws.column_dimensions[get_column_letter(self.c_src)].width = w["source"]
        for c in range(self.c_src + 1, self.c_label):
            ws.column_dimensions[get_column_letter(c)].width = w["rule"] if c == self.c_rule else w["spacer"]
        ws.column_dimensions[get_column_letter(self.c_label)].width = self.spec.get("label_width", w["label"])
        for c in self.cols:
            ws.column_dimensions[c["L"]].width = c.get("width", w[c["kind"]])
        self._title()
        if self.r_groups:
            self._groups()
        self._head()
        for r, row in self.rows:
            kind = row["kind"]
            ws.row_dimensions[r].height = lay["heights"].get(kind, lay["heights"]["default"])
            if kind == "spacer":
                continue
            if kind == "dots":
                for x in self._cells(r):
                    x.border = Border(top=st.side(st.cfg["dots"]["color"], "dotted"))
                continue
            if kind in ("footnote", "text"):
                c = st.cfg[kind]
                x = ws.cell(r, self.c_label, row.get("label"))
                x.font = st.F(c["color"], c.get("bold", False), c.get("italic", False))
                continue
            self._data(r, row)
        self._source_column()
        ws.page_setup.orientation = "landscape"
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_area = f"{get_column_letter(self.c_label)}{self.r_title}:{self.cols[-1]['L']}{self.last_row}"

    def _cells(self, r):
        return [self.ws.cell(r, self.c_label)] + [self.ws[f"{c['L']}{r}"] for c in self.cols]

    def _title(self):
        st, c = self.st, self.st.cfg["title"]
        r = self.r_title
        self.ws.row_dimensions[r].height = self.st.cfg["layout"]["heights"]["title"]
        for x in self._cells(r):
            x.border = Border(bottom=st.side(c["border"], c.get("border_style", "thin")))
        x = self.ws.cell(r, self.c_label, self.spec["title"])
        x.font = st.F(c["color"], bold=True)
        x.alignment = Alignment(vertical="center")

    def _groups(self):
        st, c = self.st, self.st.cfg["group"]
        r = self.r_groups
        letters = [col["L"] for col in self.cols]
        for g in self.spec["groups"]:
            i0, i1 = letters.index(self.period_col[g["from"]]), letters.index(self.period_col[g["to"]])
            for j in range(i0, i1 + 1):   # centré sur plusieurs colonnes, jamais de fusion
                x = self.ws[f"{letters[j]}{r}"]
                x.fill, x.font = st.fill(c["fill"]), st.F(c["color"], bold=True)
                x.alignment = Alignment(horizontal="centerContinuous", vertical="center")
                x.border = Border(top=st.side(c["border"]), bottom=st.side(c["border"]))
            self.ws[f"{letters[i0]}{r}"].value = g["text"]

    def _head(self):
        st, c, r = self.st, self.st.cfg["head"], self.r_head
        self.ws.row_dimensions[r].height = self.st.cfg["layout"]["heights"]["head"]
        x = self.ws.cell(r, self.c_label, self.spec.get("unit") or c["unit"])
        x.font, x.border = st.F(c["color"], bold=True), Border(bottom=st.side(c["border"], "medium"))
        x.alignment = Alignment(vertical="bottom")
        for col in self.cols:
            if col["kind"] == "gap":
                continue
            x = self.ws[f"{col['L']}{r}"]
            x.value = col.get("header")
            x.alignment = Alignment(horizontal="center" if col["kind"] == "note" else "right", vertical="bottom", wrap_text=True)
            if col["kind"] == "var":
                x.font = st.F(st.cfg["variation"]["color"], bold=True)
            else:
                x.font, x.border = st.F(c["color"], bold=True), Border(bottom=st.side(c["border"], "medium"))

    def _source_column(self):
        st, c = self.st, self.st.cfg["source_col"]
        for r in range(self.r_head, self.last_row + 1):
            x = self.ws.cell(r, self.c_src)
            x.fill, x.font = st.fill(c["fill"]), st.F(c["color"], bold=(r == self.r_head))
            x.alignment = Alignment(vertical="center")
        self.ws.cell(self.r_head, self.c_src, c["header"])

    def _data(self, r, row):
        st, ws = self.st, self.ws
        s = st.cfg["rows"][row["kind"]]
        fill, bottom = st.fill(s.get("fill")), s.get("border_bottom")
        indent = row.get("indent", s.get("indent", 0))
        border = Border(bottom=st.side(bottom)) if bottom else None
        x = ws.cell(r, self.c_label, row.get("label"))
        x.font = st.F(s.get("label_color", s["color"]), s.get("bold", False), s.get("italic", False))
        x.alignment = Alignment(horizontal="left" if indent else None, indent=indent, vertical="center")
        if s.get("label_fill") or fill:
            x.fill = st.fill(s.get("label_fill")) or fill
        if border:
            x.border = border
        if s.get("rule"):
            ws.cell(r, self.c_rule).fill = st.fill(s["rule"])
        if row.get("source"):
            ws.cell(r, self.c_src, row["source"])
        fmt = st.cfg["formats"][row.get("format") or s["format"]]
        vals = row.get("values")
        where = f"{self.name}, {row.get('label') or row['kind']}"
        for col in self.cols:
            x = ws[f"{col['L']}{r}"]
            if fill:
                x.fill = fill
            if border and col["kind"] != "var":
                x.border = border
            if col["kind"] == "value":
                v = vals if isinstance(vals, str) else (vals[self.value_cols.index(col)] if vals is not None else None)
                if isinstance(v, str) and v.startswith("="):
                    v = self.checked(self.resolve(v, col), where)
                x.value, x.number_format = v, fmt
                x.font = st.F(s["color"], s.get("bold", False), s.get("italic", False))
                if isinstance(v, str) and not v.startswith("="):   # n.c., n.a.
                    tv = st.cfg["text_value"]
                    x.font = st.F(tv["color"], s.get("bold", False), tv.get("italic", True))
                x.alignment = Alignment(horizontal="right", vertical="center")
            elif col["kind"] == "var" and row.get("var"):
                self._var(x, r, col, row["var"], where, s)
            elif col["kind"] == "note" and row.get("note"):
                self._note(x, str(row["note"]))
        if s.get("alert_nonzero"):
            tol = st.cfg.get("check_tolerance", 0.5)
            first, last = self.value_cols[0]["L"], self.value_cols[-1]["L"]
            ws.conditional_formatting.add(f"{first}{r}:{last}{r}", CellIsRule(
                operator="notBetween", formula=[str(-tol), str(tol)],
                font=Font(color=st.hex(s["alert_nonzero"]), bold=True)))

    def _var(self, x, r, col, mode, where, s):
        st = self.st
        if col.get("force_abs") and mode == "pct":
            mode = "abs"
        cur, prev = f"{self.period_col[col['to']]}{r}", f"{self.period_col[col['from']]}{r}"
        tpl = st.cfg["variations"][mode]
        x.value = self.checked(tpl.format(cur=cur, prev=prev, years=col.get("years", 1)), where)
        x.number_format = st.cfg["formats"][{"pct": "percent", "cagr": "percent", "pp": "pp", "abs": "number"}[mode]]
        x.font = st.F(st.cfg["variation"]["color"], s.get("bold", False), s.get("italic", False))
        x.alignment = Alignment(horizontal="right", vertical="center")

    def _note(self, x, note):
        st, c = self.st, self.st.cfg["note"]
        main = "." not in note
        x.value = note
        x.font = st.F(c["main_color"] if main else c["sub_color"], bold=True)
        x.fill = st.fill(c["main_fill"] if main else c["sub_fill"])
        x.alignment = Alignment(horizontal="center", vertical="center")


class _Book:
    def __init__(self, spec: dict, charte: Charte):
        self.st = _Style(charte)
        self.allowed = {f.upper() for f in self.st.cfg.get("functions", [])}
        self.sheets = {}
        for s in spec["sheets"]:
            self.sheets[s["name"]] = _Sheet(self, s)


def render(spec: dict, charte: Charte) -> Workbook:
    """Classeur openpyxl du datapack. Lève DatapackError si la spec est invalide."""
    errors = validate(spec, charte)
    if errors:
        raise DatapackError(errors)
    book = _Book(spec, charte)
    wb = Workbook()
    wb.remove(wb.active)
    for sh in book.sheets.values():
        sh.render(wb)
    wb.calculation = CalcProperties(fullCalcOnLoad=True)   # Excel recalcule à l'ouverture
    return wb


def describe(charte: Charte) -> dict[str, Any]:
    """Ce que la charte permet : types de lignes, formats, sources, fonctions (pour Claude)."""
    cfg = _Style(charte).cfg
    return {
        "row_kinds": sorted(cfg["rows"]) + sorted(LAYOUT_KINDS),
        "column_kinds": sorted(COLUMN_KINDS),
        "var_modes": sorted(VAR_MODES),
        "formats": sorted(cfg["formats"]),
        "sources": cfg.get("sources", []),
        "functions": cfg.get("functions", []),
    }
