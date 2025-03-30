from fontTools.ttLib import TTFont
import pathlib
import os

# This script converts OTF fonts to WOFF and WOFF2 formats using fontTools.
# It assumes that the OTF files are located in a folder named 'OTF' within a 'fonts' directory.
# The converted WOFF and WOFF2 files will be saved in the same directory as the original OTF files.

parent_dir = pathlib.Path("../fonts")

for sub_dir in ["WOFF", "WOFF2"]:
    if not (parent_dir / sub_dir).is_dir():
        os.makedirs(parent_dir / sub_dir, exist_ok=True)

files = [
    "WD-XLLubrifontSC-Regular.otf",
    "WD-XLLubrifontTC-Regular.otf",
    "WD-XLLubrifontJPS-Regular.otf",
    "WD-XLLubrifontJPN-Regular.otf",
]

print("Conversion started")
for filename in files:
    f = TTFont(parent_dir / "OTF" / filename)
    f.flavor = "woff"
    f.save(parent_dir / "WOFF" / f"{filename[:-4]}.woff")
    print("Exported " + filename[:-4] + ".woff")
    f.flavor = "woff2"
    f.save(parent_dir / "WOFF2" / f"{filename[:-4]}.woff2")
    print("Exported " + filename[:-4] + ".woff2")
