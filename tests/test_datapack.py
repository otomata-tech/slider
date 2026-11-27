"""Datapack Excel : rendu à la charte `blank`, validation, déterminisme. Données inventées."""
import copy
import hashlib
import io
import json
import zipfile

import pytest
from openpyxl import load_workbook

from lib.charte import Charte
from lib.datapack import DatapackError, describe, render, validate


@pytest.fixture
def charte():
    return Charte.load("blank")


def _spec():
    return {"sheets": [
        {"name": "P&L", "title": "Projet Test | Compte de résultat",
         "columns": [{"kind": "value", "period": "24", "header": "FY24"},
                     {"kind": "value", "period": "25", "header": "FY25"},
                     {"kind": "gap"},
                     {"kind": "var", "header": "Var.", "from": "24", "to": "25"},
                     {"kind": "note", "header": "Note"}],
         "groups": [{"from": "24", "to": "25", "text": "Historique"}],
         "rows": [
             {"kind": "band", "label": "Chiffre d'affaires", "key": "ca", "values": [1000, 1100], "source": "Comptabilité", "var": "pct", "note": "1"},
             {"kind": "spacer"},
             {"kind": "line", "label": "Achats", "key": "ach", "values": [-400, -450], "source": "Comptabilité", "var": "pct"},
             {"kind": "detail", "label": "dont matières", "values": [-100, "n.c."]},
             {"kind": "subtotal", "label": "Marge brute", "key": "mb", "values": "={ca}+{ach}", "var": "pct", "note": "1.1"},
             {"kind": "kpi", "label": "Taux de marge", "values": "={mb}/{ca}", "var": "pp"},
             {"kind": "dots"},
             {"kind": "footnote", "label": "Source : comptes annuels"},
             {"kind": "control", "label": "Marge publiée", "key": "pub", "values": [600, 650], "source": "Information client"},
             {"kind": "check", "label": "Écart", "values": "={mb}-{pub}"},
         ]},
        {"name": "KPI", "title": "Projet Test | Indicateurs",
         "columns": [{"kind": "value", "period": "24", "header": "FY24"},
                     {"kind": "value", "period": "25", "header": "FY25"}],
         "rows": [{"kind": "line", "label": "CA repris", "values": "={P&L!ca}"},
                  {"kind": "line", "label": "CA FY25 figé", "values": "={P&L!ca@25}"}]},
    ]}


def test_rendu(charte, tmp_path):
    wb = render(_spec(), charte)
    chemin = tmp_path / "dp.xlsx"
    wb.save(chemin)
    ws = load_workbook(chemin)["P&L"]
    assert ws["D2"].value == "Projet Test | Compte de résultat"
    assert ws["E4"].value == "Historique" and ws["E4"].alignment.horizontal == "centerContinuous"
    assert [ws.cell(5, c).value for c in (1, 4, 5, 6)] == ["Source", "€ en milliers", "FY24", "FY25"]
    # lignes à partir de 7 : band, spacer, line, detail, subtotal, kpi…
    assert ws["E7"].value == 1000 and ws["A7"].value == "Comptabilité"
    assert ws["E11"].value == "=E7+E9" and ws["F11"].value == "=F7+F9"
    assert ws["H7"].value == '=IFERROR(IF(E7*F7<=0,"n.a.",F7/E7-1),"n.a.")'
    assert ws["H12"].value == '=IFERROR((F12-E12)*100,"n.a.")'
    assert ws["I7"].value == "1" and ws["C7"].fill.fgColor.rgb.endswith("1E3A8A")
    assert ws["F10"].font.italic                                  # « n.c. » en italique
    assert not ws.merged_cells.ranges
    tailles = {c.font.sz for row in ws.iter_rows() for c in row if c.value is not None}
    assert tailles == {10}                                        # une seule taille
    assert len(ws.conditional_formatting) == 1                    # alerte sur l'écart
    kpi = load_workbook(chemin)["KPI"]
    assert kpi["E5"].value == "='P&L'!E7" and kpi["E6"].value == "='P&L'!F7"   # sans surtitres : lignes dès 5


@pytest.mark.parametrize("modif, message", [
    (lambda s: s["sheets"][0]["rows"][0].update(source="VDD p.55"), "hors liste"),
    (lambda s: s["sheets"][0]["rows"][4].update(values="=SUMIF({ca},1)"), "SUMIF non autorisée"),
    (lambda s: s["sheets"][0]["rows"][4].update(values="=E7+{ach}"), "écrite en dur"),
    (lambda s: s["sheets"][0]["rows"][4].update(values="={ca}+{inconnue}"), "clé « inconnue » inconnue"),
    (lambda s: s["sheets"][0]["rows"][2].update(values=[1, 2, 3]), "3 valeurs pour 2"),
    (lambda s: s["sheets"][0]["rows"][2].update(kind="tableau"), "type « tableau » inconnu"),
    (lambda s: s["sheets"][0]["rows"][2].update(key="ca"), "clé « ca » en double"),
    (lambda s: s["sheets"][0]["columns"][3].update(to="26"), "période to « 26 » inconnue"),
    (lambda s: s["sheets"][1]["rows"][0].update(values="={Autre!ca}"), "onglet « Autre » inconnu"),
])
def test_erreurs_localisees(charte, modif, message):
    spec = copy.deepcopy(_spec())
    modif(spec)
    with pytest.raises(DatapackError) as e:
        render(spec, charte)
    assert any(message in err for err in e.value.errors), e.value.errors


def test_charte_qui_viole_ses_regles(charte):
    charte.tokens = copy.deepcopy(charte.tokens)
    charte.tokens["excel"]["functions"] = ["SUM"]
    assert any("charte, variation" in e for e in validate(_spec(), charte))


def _empreinte(wb):
    tampon = io.BytesIO()
    wb.save(tampon)
    with zipfile.ZipFile(tampon) as z:   # le contenu, sans les dates d'écriture du zip
        return hashlib.sha1(b"".join(z.read(n) for n in sorted(z.namelist()) if n != "docProps/core.xml")).hexdigest()


def test_meme_spec_meme_classeur(charte):
    assert _empreinte(render(_spec(), charte)) == _empreinte(render(_spec(), charte))


def test_describe(charte):
    d = describe(charte)
    assert "band" in d["row_kinds"] and "spacer" in d["row_kinds"]
    assert d["functions"] == ["SUM", "IF", "IFERROR"]
    json.dumps(d)
