"""Masque : graphique natif PPTX en couleurs charte (barres / lignes / donut).

Le graphique est un vrai objet chart PowerPoint (éditable, données modifiables
dans PPT), pas une image — il s'exporte proprement en PDF via LibreOffice.
Comble le trou du kit : stat-cards pour un chiffre isolé, chart_block pour une
série.
"""
from __future__ import annotations

from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Cm, Pt

from lib.pptx_helpers import SLIDE_W_CM, add_rect
from layouts._header import draw as draw_header, title_block, MARGIN_CM

_TYPES = {
    "bar":   XL_CHART_TYPE.COLUMN_CLUSTERED,
    "line":  XL_CHART_TYPE.LINE_MARKERS,
    "donut": XL_CHART_TYPE.DOUGHNUT,
}


def _palette(ca):
    return [ca.color("primary"), ca.color("primary-dark"), ca.color("accent-mint"),
            ca.color("muted-soft"), ca.color("primary-deep"), ca.color("info")]


def render(slide, ca, *,
           title: str,
           categories: list,
           series: list,
           page_num: int,
           kind: str = "bar",
           subtitle: str | None = None,
           eyebrow: str | None = None,
           section_tag: str | None = None,
           date_text: str | None = None):
    """`series` : list de (nom, [valeurs]) alignées sur `categories`.
    `kind` : "bar" | "line" | "donut"."""
    if kind not in _TYPES:
        raise ValueError(f"chart_block: kind inconnu {kind!r} (bar|line|donut)")

    add_rect(slide, 0, 0, SLIDE_W_CM, 19.05, fill=ca.color("bg"))
    draw_header(slide, ca, page_num=page_num, date_text=date_text,
                logo_path=ca.default("header_logo"))
    title_block(slide, ca, title=title, eyebrow=eyebrow, subtitle=subtitle)

    cd = CategoryChartData()
    cd.categories = categories
    for name, vals in series:
        cd.add_series(name, vals)

    x, y = MARGIN_CM, 5.0
    w = SLIDE_W_CM - 2 * MARGIN_CM
    h = 12.0
    gframe = slide.shapes.add_chart(_TYPES[kind], Cm(x), Cm(y), Cm(w), Cm(h), cd)
    chart = gframe.chart

    # pas de titre de chart (le bloc de titre de slide s'en charge)
    chart.has_title = False

    # police charte sur tout le graphique
    chart.font.name = ca.font_primary
    chart.font.size = Pt(10)
    chart.font.color.rgb = ca.color("text")

    # légende : seulement si multi-séries ou donut
    multi = len(series) > 1 or kind == "donut"
    chart.has_legend = multi
    if multi:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False

    pal = _palette(ca)
    plot = chart.plots[0]

    if kind == "donut":
        pts = plot.series[0].points
        for i, pt in enumerate(pts):
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = pal[i % len(pal)]
        plot.has_data_labels = True
        plot.data_labels.number_format = "0"
        plot.data_labels.number_format_is_linked = False
    elif kind == "line":
        for i, s in enumerate(plot.series):
            s.format.line.color.rgb = pal[i % len(pal)]
            s.format.line.width = Pt(2.25)
    else:  # bar
        for i, s in enumerate(plot.series):
            s.format.fill.solid()
            s.format.fill.fore_color.rgb = pal[i % len(pal)]
        plot.gap_width = 80

    # axe de valeurs discret (pas de gridlines criardes) — bar/line uniquement
    if kind != "donut":
        try:
            va = chart.value_axis
            va.has_major_gridlines = True
            va.major_gridlines.format.line.color.rgb = ca.color("rule")
            va.major_gridlines.format.line.width = Pt(0.5)
            va.format.line.fill.background()
        except (NotImplementedError, AttributeError, ValueError):
            pass
