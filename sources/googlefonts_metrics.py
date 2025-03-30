"""
Script to modify TTF fonts to match Google Fonts-specific CJK metrics requirements.
See https://github.com/google/fonts/issues/8911 for more information.
"""
from fontTools.ttLib import TTFont
import sys

input_font_file = sys.argv[1] if len(sys.argv) > 1 else None
if not input_font_file:
    print("Please provide a font file as an argument.")
    sys.exit(1)

font = TTFont(input_font_file)

font["OS/2"].sTypoAscender = 945
font["OS/2"].sTypoDescender = -235
font["OS/2"].sTypoLineGap = 0
font["hhea"].ascender = 945
font["hhea"].descender = -235
font["hhea"].lineGap = 0
font["OS/2"].usWinAscent = 1168
font["OS/2"].usWinDescent = 235
font["OS/2"].fsSelection = 0x00c0
font.save(input_font_file)