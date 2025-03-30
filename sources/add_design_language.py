"""
Script to modify OTF/TTF fonts to include metadata for design primary language.
"""

from fontTools.ttLib import TTFont
from fontTools.ttLib.ttFont import newTable
import sys

input_font_file = sys.argv[1] if len(sys.argv) > 1 else None
if not input_font_file:
    print("Please provide a font file as an argument.")
    sys.exit(1)

font = TTFont(input_font_file)

new_meta = newTable("meta")

def comma_separated_list(lst):
    return ", ".join(lst)

if "SC" in input_font_file:
    new_meta.data["dlng"] = comma_separated_list(["zh", "Hans", "zh-Hans", "zh-Latn", "zh-Latn-pinyin", "Bopo", "Hanb",])
elif "TC" in input_font_file:
    new_meta.data["dlng"] = comma_separated_list(["zh", "Hant", "zh-Hant", "nan", "hak", "yue", "nan-Latn", "nan-Latn-pehoeji", "nan-Latn-tailo", "Bopo", "Hanb",])
elif "JP" in input_font_file:
    new_meta.data["dlng"] = comma_separated_list(["ja", "Jpan", "ja-Jpan",])

new_meta.data["slng"] = comma_separated_list(
    [
        # Chinese
        "zh",
        "Hans",
        "Hant",
        "zh-Hans",
        "zh-Hant",
        "nan",
        "hak",
        "yue",
        # Chinese Transcriptions
        "Bopo",
        "Hanb",
        "zh-Latn",
        "zh-Latn-pinyin",
        "nan-Latn",
        "nan-Latn-pehoeji",
        "nan-Latn-tailo",
        # Japanese
        "ja",
        "Jpan",
        "ja-Jpan",
        # LCG
        "Latn",
        "Cyrl",
        "Grek",
    ]
)

font["meta"] = new_meta
font.save(input_font_file)
