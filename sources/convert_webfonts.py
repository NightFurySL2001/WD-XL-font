from fontTools.ttLib import TTFont

files = ["WD-XLLubrifontSC-Regular.otf", "WD-XLLubrifontTC-Regular.otf"]

print("Conversion started")
for filename in files:
    f = TTFont(filename)
    f.flavor='woff'
    f.save(filename[:-4]+'.woff')
    print("Exported "+filename[:-4]+'.woff')
    f.flavor='woff2'
    f.save(filename[:-4]+'.woff2')
    print("Exported "+filename[:-4]+'.woff2')