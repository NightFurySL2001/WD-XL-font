final_font = open("HuaYou-src.ttx", "w", encoding="utf-8")

header = open("HuaYou-base.ttx", "r", encoding="utf-8")
for line in header:
    to_write = ""
    #rename font
    if line.strip() == "WD-XL Lubrifont SC":
        to_write = "      WD-XL Lubrifont src\n"
    elif line.strip() == "WDXLLubrifont-SC":
        to_write = "      WDXLLubrifont-src\n"
    elif line.strip() == "SC":
        to_write = "      src\n"
    #skip ending
    elif line.strip() == "</ttFont>":
        to_write == ""
    else:
        to_write = line
    final_font.write(to_write)

final_font.write("\n")

merge_font = open("HuaYou.ttx", "r", encoding="utf-8")
for num, line in enumerate(merge_font):
    #skip header part and <ttfont>
    if num < 2:
        continue
    final_font.write(line)

final_font.close()
