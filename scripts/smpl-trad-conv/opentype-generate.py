#tc_to_sc = False
for tc_to_sc in (True, False):

    if tc_to_sc:
        one_to_many = open("tc-sc-1-m.txt", "r", encoding="utf-8")
        one_to_one = open("tc-sc-1-1.txt", "r", encoding="utf-8")
        output_file = open("opentype-trad-to-simp.txt", "w", encoding="utf-8")
    else:
        one_to_many = open("sc-tc-1-m.txt", "r", encoding="utf-8")
        one_to_one = open("sc-tc-1-1.txt", "r", encoding="utf-8")
        output_file = open("opentype-simp-to-trad.txt", "w", encoding="utf-8")

    font_source = open("WD-XLLubrifont-src2.000.ttf-han.txt", "r", encoding="utf-8")

    #get font list
    font_char_list = []
    for line in font_source:
        font_char_list.append(line.strip("\r\n"))

    #convert character to unicode
    def convert_uni(char):
        uni_val = str(hex(ord(char))).upper()[2:]
        if len(uni_val) > 4:
            return "u"+uni_val
        else:
            return "uni"+uni_val

    written=[]
    for line in one_to_many:
        text = line.strip("\r\n")
        orig = text[0]
        if orig not in font_char_list: #first word not in list - no need conversion
            continue
        sub = text[2:]
        temp = ""
        #checking first
        for word in sub: #check all the other, write to file if present
            if word in font_char_list:
                temp += word
        if temp == "" or temp == orig: #if nothing to sub/sub using same word only - no need conversion
            continue
        #start writing after check all word present
        output_file.write("sub "+convert_uni(orig)+" from [ ")
        for word in temp:
            output_file.write(convert_uni(word)+" ")
        #end writing
        output_file.write("];\n")
        written.append(orig)

    for line in one_to_one:
        if line[0] in written: #debug check
            print(line)
        if line[0] in font_char_list and line[2] in font_char_list and line[0] not in written:
            output_file.write("sub "+convert_uni(line[0])+" by "+convert_uni(line[2])+" ;\n")
            written.append(line[0])
