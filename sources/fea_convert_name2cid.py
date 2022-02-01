
from os import chdir, cpu_count, name, write


feature_filename = "HuaYou-feature-main.fea"
output_filename = "HuaYou-feature-CID.fea"

name2cid_filename = "AI0_HuaYou.txt"

def uni_rename(hex_str): #input 0xabcd
    uni_val = hex_str[2:]
    if len(uni_val) > 4:
        return "u"+uni_val.upper()
    else:
        return "uni"+uni_val.upper()

name2cid_list = {}
uni2cid_list = {}
with open(name2cid_filename, "r", encoding="utf-8") as name2cid_open:
    for line in name2cid_open:
        #reading csv
        #convert_arr = line.strip("\n").split(",")
        #reading AI0 file
        convert_arr = line.strip("\n").split("\t")
        name2cid_list[convert_arr[1]] = "\\"+convert_arr[0]
        uni2cid_list[uni_rename(convert_arr[3])] = "\\"+convert_arr[0]

#input string
#output cut off string and suffix
def check_suffix(str, suffix = ""):
    if str.endswith(("]", "'", ";")):
        return_cutoff = str[:-1]
        return_suffix = str[-1]+suffix
    else:
        return (str, suffix)
    return check_suffix(return_cutoff, return_suffix)

#input value
#output boolean, true if is unicode
def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

#input original string and dict of possible string (in keys)
#output new name, boolean if changed
def ask_new_name (name, range):
    if name not in range:
        new_glyph_name = str(input(name+" do not exist. Input new glyph name or press enter to use current value: "))
        if new_glyph_name == "": #pressed enter
            return (new_glyph_name, False)
        elif new_glyph_name in range.keys():
            return (new_glyph_name, True)
        else:
            return (new_glyph_name, False)

#constant variable values, all lowercase
keyword_list = ["anchor", "<anchor", "anchordef", "anon", "anonymous", "base", "by", "contourpoint", "cursive", "enum", "enumerate", "exclude_dflt", "feature", "featurenames", "from", "ignore", "ignorebaseglyphs", "ignoreligatures", "ignoremarks", "include", "include_dflt", "language", "languagesystem", "lookup", "lookupflag", "mark", "markattachmenttype", "markclass", "nameid", "name", "null", "parameters", "pos", "position", "reversesub", "righttoleft", "rsub", "script", "sub", "substitute", "subtable", "table", "useextension", "usemarkfilteringset", "valuerecorddef", "vertoriginy", "vertadvancey"]
table_name_list = ["abvf", "abvm", "abvs", "akhn", "blwf", "blwm", "blws", "cfar", "cjct", "dist", "haln", "half", "nukt", "pstf", "psts", "pref", "pres", "rkrf", "rphf", "vatu", "smpl", "trad", "tnam", "expt", "hojo", "nlck", "jp78", "jp83", "jp90", "jp04", "hngl", "ljmo", "tjmo", "vjmo", "fwid", "hwid", "halt", "twid", "qwid", "pwid", "palt", "pkna", "ruby", "hkna", "vkna", "cpct", "curs", "jalt", "mset", "rclt", "rlig", "isol", "init", "medi", "med2", "fina", "fin2", "fin3", "falt", "stch", "smcp", "c2sc", "pcap", "c2pc", "unic", "cpsp", "case", "ital", "ordn", "valt", "vhal", "vpal", "vert", "vrt2", "vrtr", "vkrn", "ltra", "ltrm", "rtla", "rtlm", "lnum", "onum", "pnum", "tnum", "frac", "afrc", "dnom", "numr", "sinf", "mgrk", "flac", "dtls", "ssty", "aalt", "swsh", "cswh", "calt", "hist", "locl", "rand", "nalt", "salt", "ss01", "ss02", "ss03", "ss04", "ss05", "ss06", "ss07", "ss08", "ss09", "ss10", "ss11", "ss12", "ss13", "ss14", "ss15", "ss16", "ss17", "ss18", "ss19", "ss20", "subs", "sups", "titl", "rvrn", "clig", "dlig", "hlig", "liga", "ccmp", "kern", "mark", "mkmk", "opbd", "lfbd", "rtbd", "size", "ornm", "vmtx"]
lang_name_list = ["dflt", "latn", "cyrl", "grek", "hani", "hang", "bopo", "kana", "zhs", "zht", "zhh"]

with open(feature_filename, "r", encoding="utf-8") as feature_str:
    replace_names = False
    indent_level = 0
    output_file = open(output_filename, "w", encoding="utf-8")
    unwritten_comment = ""
    #check line by line
    for line in feature_str:
        #check for comments
        if line.strip().startswith("#"):
            output_file.write("\t"*indent_level)
            output_file.write(line+"\n")
            continue
        #skip empty lines
        if line.strip() == "":
            output_file.write("\n")
            continue
        
        #split into words to be compared
        word_arr = line.strip().split(" ")

        #check for lookup and features to skip, label which range is checked
        if word_arr[len(word_arr)-1][-1] == "{":
        #    replace_names = True
        #    output_file.write("\t"*indent_level)
        #    output_file.write(" ".join(word_arr)+"\n")
            indent_level+=1
        #    continue
        if word_arr[0][0] == "}":
        #    if indent_level < 1:
        #        replace_names = False
            indent_level-=1
            output_file.write("\t"*indent_level)
            output_file.write(" ".join(word_arr)+"\n")
            continue
        replace_names = True
        
        #check for specific rules to be substitute
        if replace_names:
            write_arr = []
            user_string = False
            anchor_value = False
            comments = False
            pairable_word = False
            for word in word_arr:
                compare_word = ""
                #skip double quoted string
                if user_string:
                    write_arr.append(word)
                    continue
                #for single word
                if word.startswith('"') and word.endswith('"'):
                    write_arr.append(word)
                    continue
                #for long string
                elif word.startswith('"'):
                    write_arr.append(word)
                    user_string = True
                    continue
                elif word.endswith('"'):
                    #already written
                    user_string = False
                    continue

                #skip <anchor>
                if anchor_value:
                    write_arr.append(word)
                    continue
                #for single word
                if word.startswith('<') and word.endswith('>'):
                    write_arr.append(word)
                    continue
                #for long string
                elif word.startswith('<'):
                    write_arr.append(word)
                    anchor_value = True
                    continue
                elif word.endswith('>'):
                    #already written
                    anchor_value = False
                    continue

                #skip symbols
                if word in ("=", "}", "{", ";"):
                    write_arr.append(word)
                    continue
                
                
                #check for glyph name and replace with cid no.
                #separate prefix and suffix
                prefix = ""
                suffix = ""
                #prefix
                if word.startswith("["):
                    compare_word = word[1:]
                    prefix = word[0]
                #suffix
                if word.endswith(("]", "'", ";")):
                    if compare_word:
                        compare_word, suffix = check_suffix(compare_word[:-1], compare_word[-1])
                    else:
                        compare_word, suffix = check_suffix(word[:-1], word[-1])
                #if no prefix and suffix
                if prefix == "" and suffix == "":
                    compare_word = word
                #double check to remove \ symbol
                if compare_word.startswith("\\"):
                    compare_word = compare_word[1:]

                #skip keywords
                if compare_word.lower() in keyword_list or compare_word in table_name_list or compare_word.lower() in lang_name_list:
                    write_arr.append(prefix+compare_word+suffix)
                    #if it is lookup then ignore next term
                    if compare_word.lower() == "lookup":
                        pairable_word = True
                    continue
                #skip user defined lookup name
                if pairable_word:
                    write_arr.append(prefix+compare_word+suffix)
                    pairable_word = False
                    continue
                #skip comments
                if compare_word.startswith("#") or comments:
                    write_arr.append(prefix+compare_word+suffix)
                    comments = True
                    continue
                #skip groups
                if compare_word.startswith("@"):
                    write_arr.append(prefix+compare_word+suffix)
                    continue
                #skip numeric values
                if compare_word.isdigit() or (compare_word.startswith("-") and compare_word[1:].isdigit()) or (compare_word.startswith('0x') and is_hex(compare_word[2:])):
                    write_arr.append(prefix+compare_word+suffix)
                    continue
                #skip if empty
                if compare_word == "":
                    write_arr.append(prefix+suffix)
                    continue

                #append to array to write later
                #loop until a match is found
                found_replaced_cid = False
                while not found_replaced_cid:
                    #print(compare_word)
                    #name is in cid2name list
                    if compare_word in name2cid_list.keys():
                        found_replaced_cid = True
                        write_arr.append(prefix + name2cid_list.get(compare_word) + suffix)

                    #if start with uni or u
                    elif compare_word.startswith("uni") or (compare_word.startswith("u") and len(compare_word)==5 and is_hex(compare_word[1:])):
                        #temporary code to choose -SC if split
                        #if compare_word+"-SC" in name2cid_list.keys():
                        #    compare_word+="-SC"
                        #    continue
                        #end temporary
                        if compare_word in uni2cid_list.keys():
                            #get cid value
                            cid_value = uni2cid_list[compare_word]
                            #get name from cid value
                            key_list = list(name2cid_list.keys())
                            val_list = list(name2cid_list.values())
                            position = val_list.index(cid_value)
                            confirmation = input(compare_word+" do not exist. New name found: " + key_list[position] + ". Use new name? Y for yes: ")
                            if confirmation.lower() == "y":
                                #add to list
                                name2cid_list[compare_word] = cid_value
                                compare_word = key_list[position]
                            else:
                                new_glyph_name, found = ask_new_name(compare_word, name2cid_list)
                                if found: #pressed enter
                                    name2cid_list[compare_word] = name2cid_list[new_glyph_name]
                                else:
                                    write_arr.append(prefix + compare_word + suffix)
                                    found_replaced_cid = True
                        else:
                            new_glyph_name, found = ask_new_name(compare_word, name2cid_list)
                            if found: #pressed enter
                                name2cid_list[compare_word] = name2cid_list[new_glyph_name]
                            else:
                                write_arr.append(prefix + compare_word + suffix)
                                found_replaced_cid = True
                    #not found
                    elif compare_word.strip() != "": 
                        #temporary code to choose -SC if split
                        #if compare_word+"-SC" in name2cid_list.keys():
                        #    compare_word+="-SC"
                        #    continue
                        #end temporary
                        new_glyph_name, found = ask_new_name(compare_word, name2cid_list)
                        if found: #pressed enter
                            name2cid_list[compare_word] = name2cid_list[new_glyph_name]
                        else:
                            write_arr.append(prefix + compare_word + suffix)
                            found_replaced_cid = True
            #write converted line
            output_file.write("\t"*indent_level)
            output_file.write(" ".join(write_arr))
            if write_arr[len(write_arr)-1][-1] != ";":
                unwritten_comment+=line.strip()+" "
            else:
                output_file.write(" #" + unwritten_comment +" "+ line.strip()) #write unconverted terms as comments
                unwritten_comment = ""
            output_file.write("\n")

