"""Crédit Agricole brand tokens — python-pptx ready.

Source de vérité : tokens.json. Si tu modifies, sync tokens.json + tokens.css.
"""
from pptx.dml.color import RGBColor

# -- colors ------------------------------------------------------------------
PRIMARY        = RGBColor(0x00, 0x89, 0x91)   # Sarcelle CA
PRIMARY_DARK   = RGBColor(0x00, 0x71, 0x78)
PRIMARY_DEEP   = RGBColor(0x00, 0x58, 0x60)

SIGNATURE      = RGBColor(0x82, 0xB6, 0x00)   # Vert pomme CA
SIGNATURE_DARK = RGBColor(0x75, 0xA3, 0x00)
SIGNATURE_DEEP = RGBColor(0x3D, 0x6D, 0x04)

ACCENT_MINT    = RGBColor(0x49, 0xCE, 0xAA)

ALERT          = RGBColor(0xFF, 0x35, 0x21)
WARNING        = RGBColor(0x8A, 0x6D, 0x3B)
INFO           = RGBColor(0x33, 0x7A, 0xB7)

TEXT           = RGBColor(0x2E, 0x37, 0x38)
TEXT_STRONG    = RGBColor(0x00, 0x00, 0x00)
TEXT_SOFT      = RGBColor(0x40, 0x40, 0x40)
MUTED          = RGBColor(0x67, 0x67, 0x67)
MUTED_SOFT     = RGBColor(0xA6, 0xA6, 0xA6)

RULE           = RGBColor(0xD9, 0xD9, 0xD9)
RULE_SOFT      = RGBColor(0xE0, 0xE0, 0xE0)

BG             = RGBColor(0xFF, 0xFF, 0xFF)
BG_SOFT        = RGBColor(0xF5, 0xF5, 0xF5)
BG_CANVAS      = RGBColor(0xEB, 0xEB, 0xEB)

PANEL_MINT     = RGBColor(0xE8, 0xF4, 0xEF)
PANEL_TEAL     = RGBColor(0xE6, 0xF1, 0xF2)
PANEL_CREAM    = RGBColor(0xF8, 0xF5, 0xEE)

# -- fonts -------------------------------------------------------------------
FONT_PRIMARY   = "Raleway"
FONT_CONDENSED = "Raleway"  # pas de version condensed officielle CA

# -- type scale (sizes in pt) -------------------------------------------------
SIZE_H1      = 46
SIZE_H2      = 30
SIZE_H3      = 22
SIZE_LEAD    = 13
SIZE_BODY    = 10.5
SIZE_SMALL   = 9
SIZE_EYEBROW = 9
SIZE_LABEL   = 8.5

# -- layout ------------------------------------------------------------------
PAGE_MARGIN_MM = 9
GUTTER_MM      = 6
