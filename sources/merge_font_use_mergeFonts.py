from typing import Mapping
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
import unicodedata2 # https://stackoverflow.com/questions/9868792/find-out-the-unicode-script-of-a-character
import sys
import os

#input font name
font_1_name = "WD-XLLubrifont-Regular.ttf"
font_2_name = "WD-XLLubrifont-Trad.ttf"
font_3a_name = "WD-XLLubrifont-jp83.ttf"
font_3b_name = "WD-XLLubrifont-jp90.ttf"
font_3c_name = "WD-XLLubrifont-jp04.ttf"

#output font file
output_name = "HuaYou"

#language tag (all caps)
lang_suffix_1 = "SC"
lang_suffix_2 = "TC"
lang_suffix_3a = "JP83" #only add for jp83 functionality, not used in cmap
lang_suffix_3b = "JP90"
lang_suffix_3c = "JP04"
#does second font contains only glyphs to the specific region 2 only?
is_override_only = True

#override file
override_glyph_names_file = "huayou-override-name.txt"
override_cid_map_file = "huayou-override-map.txt"

#extra for JP90/04
extra_3b_map_file = "jp90-override.txt"
extra_3c_map_file = "jp04-override.txt"

#ignore glyphs list
ignore_glyphs = [".IDCext", ".null", "nonmarkingreturn"]

#open the font and convert to xml with ttx
ttx_name_1 = font_1_name[:-4]+".xml"
ttx_name_2 = font_2_name[:-4]+".xml"
ttx_name_3a = font_3a_name[:-4]+".xml"
ttx_name_3b = font_3b_name[:-4]+".xml"
ttx_name_3c = font_3c_name[:-4]+".xml"

#export XML for reading
file_list = {font_1_name: ttx_name_1, font_2_name: ttx_name_2, font_3a_name: ttx_name_3a, font_3b_name: ttx_name_3b, font_3c_name: ttx_name_3c}
for fontname, filename in file_list.items():
    #if file exist then skip
    if not os.path.isfile(filename):
        try:
            ttfont_var = TTFont(fontname)
            ttfont_var.saveXML(filename,newlinestr="\n",tables=["GlyphOrder","glyf","hmtx","cmap"])
            ttfont_var.close()
            print(fontname + " converted to XML.")
        except IOError:
            print(fontname + " could not be opened.")
            sys.exit(0)

### override names for generated glyph names
override_glyph_names = {}
try:
    with open(override_glyph_names_file, "r", encoding="utf-8") as override_file:
        for line in override_file:
            if line.startswith(("#", "//")):
                continue # ignore commented line
            orig_name, new_name = line.strip("\n").split(",")
            override_glyph_names[orig_name] = new_name
except IOError:
    print("No override name files detected.")

### override CID to code mapping
override_cid_map = {}
try:
    with open(override_cid_map_file, "r", encoding="utf-8") as override_file:
        for line in override_file:
            if line.startswith(("#", "//")):
                continue # ignore commented line
            unicode, region, remap_char_name, keep_status = line.strip("\n").split(",")
            #change unicode to 
            uni_int_val = int(unicode, 16)
            if uni_int_val not in override_cid_map:
                override_cid_map[uni_int_val] = {}
            override_cid_map[uni_int_val][region] = remap_char_name
            if "keep" not in override_cid_map[uni_int_val].keys():
                override_cid_map[uni_int_val]["keep"] = {}
            if keep_status.lower() != "":
                override_cid_map[uni_int_val]["keep"][region] = True
            elif region not in override_cid_map[uni_int_val]["keep"].keys() and keep_status == "":
                override_cid_map[uni_int_val]["keep"][region] = False
except IOError: 
    print("No override CID mapping files detected.")

### override unicode value for region 3b
extra_3b_uni = {}
try:
    with open(extra_3b_map_file, "r", encoding="utf-8") as override_file:
        for line in override_file:
            if line.startswith(("#", "//")) or line.strip() == "":
                continue # ignore commented line n empty line
            if line.startswith("default"): #default TC
                extra_3b_uni["default"] = line.strip("\n").split(",")[1]
                continue
            orig_char, region = line.strip("\n").split(",")
            unicode = str(hex(ord(orig_char))).lower()[2:]
            extra_3b_uni[unicode] = region
except IOError:
    print("No override " + lang_suffix_3b + " mapping files detected.")

### override unicode value for region 3c
extra_3c_uni = {}
try:
    with open(extra_3c_map_file, "r", encoding="utf-8") as override_file:
        for line in override_file:
            if line.startswith(("#", "//")) or line.strip() == "":
                continue # ignore commented line n empty line
            if line.startswith("default"): #default TC
                extra_3c_uni["default"] = line.strip("\n").split(",")[1]
                continue
            orig_char, region = line.strip("\n").split(",")
            unicode = str(hex(ord(orig_char))).lower()[2:]
            extra_3c_uni[unicode] = region
except IOError:
    print("No override " + lang_suffix_3c + " mapping files detected.")


## variables to store the final font
cmap_final = {} # unicode_lowercase(no 0x):{lang_region_1:"name", lang_region_2:"name"}
## variable to store new name fore mergeFonts
# Format: orig name:new name
font_rename_1 = {}
font_rename_2 = {}
font_rename_3a = {}
font_rename_3b = {}
font_rename_3c = {}

glyph_seen = [] #check if the glyph is copied for next font (use font glyph name)

#load font 1
font_tree_1 = ET.parse(ttx_name_1)
font_root_1 = font_tree_1.getroot() #<ttFont sfntVersion="\x00\x01\x00\x00" ttLibVersion="3.44">

#get separable tables
glyf_1 = font_root_1.find('glyf') # <TTGlyph name="char_name" xMin="int" yMin="int" xMax="int" yMax="int">
hmtx_1 = font_root_1.find('hmtx') # <mtx name="char_name" width="int" lsb="int"/>
cmap_temp_1 = font_root_1.find('./cmap/cmap_format_12') # only need format 12 coz format 4 redundant, <map code="0xunicode" name="char_name"/>
cmap_1 = {}
for item in cmap_temp_1: #convert format
    cmap_1[item.attrib["name"]] = item.attrib["code"]
    #=> {".notdef":"0x0", "A":"0x0020", "uniFF0E":"0xff0e"}
    #unicode is lowercase
#or could use: cmap_temp.find(".//*[@name='char_name']").attrib["code"]
#get list of glyph names in the font *in order*
char_names_1 = font_root_1.find('GlyphOrder')
#<GlyphOrder>
#    <GlyphID id="0" name=".notdef"/>
#    <GlyphID id="1" name="nonmarkingreturn"/>


#load font 2
font_tree_2 = ET.parse(ttx_name_2)
font_root_2 = font_tree_2.getroot() #<ttFont sfntVersion="\x00\x01\x00\x00" ttLibVersion="3.44">

#get separable tables
glyf_2 = font_root_2.find('glyf') # <TTGlyph name="char_name" xMin="int" yMin="int" xMax="int" yMax="int">
hmtx_2 = font_root_2.find('hmtx') # <mtx name="char_name" width="int" lsb="int"/>
cmap_temp_2 = font_root_2.find('./cmap/cmap_format_12') # only need format 12 coz format 4 redundant, <map code="0xunicode" name="char_name"/>
cmap_2 = {}
for item in cmap_temp_2: #convert format
    cmap_2[item.attrib["name"]] = item.attrib["code"]
    #=> {".notdef":"0x0", "A":"0x0020", "uniFF0E":"0xff0e"}
char_names_2 = font_root_2.find('GlyphOrder')


font_3_arr = {} #0 for jp83, 1 for jp90, 2 for jp04
for id, font in enumerate((ttx_name_3a, ttx_name_3b, ttx_name_3c)):
    #load JP fonts
    font_tree_3 = ET.parse(font)
    font_root_3 = font_tree_3.getroot() #<ttFont sfntVersion="\x00\x01\x00\x00" ttLibVersion="3.44">
    font_3_arr[id] = {}

    #get separable tables
    font_3_arr[id]["glyf"] = font_root_3.find('glyf') # <TTGlyph name="char_name" xMin="int" yMin="int" xMax="int" yMax="int">
    font_3_arr[id]["hmtx"] = font_root_3.find('hmtx') # <mtx name="char_name" width="int" lsb="int"/>
    cmap_temp_3 = font_root_3.find('./cmap/cmap_format_12') # only need format 12 coz format 4 redundant, <map code="0xunicode" name="char_name"/>
    if cmap_temp_3 is None:
        cmap_temp_3 = font_root_3.find('./cmap/cmap_format_4') # format 4 <map code="0xunicode" name="char_name"/>
    font_3_arr[id]["cmap"] = {}
    for item in cmap_temp_3: #convert format
        font_3_arr[id]["cmap"][item.attrib["name"]] = item.attrib["code"]
        #=> {".notdef":"0x0", "A":"0x0020", "uniFF0E":"0xff0e"}
    font_3_arr[id]["char_names"] = font_root_3.find('GlyphOrder')

### STR DEF FUNC
def dict_get_key(my_dict, name):
    key_list = list(my_dict.keys())
    val_list = list(my_dict.values())
    position = val_list.index(name)
    return key_list[position]
    
def feature_subarr(mydict, key_remove):
    #set remove duplicate value, only list can remove
    b = list(set(mydict.values()))
    b.remove(mydict[key_remove])
    return b

#check two XML Element is same
def elements_equal(e1, e2):
    if e1.tag != e2.tag: return False
    if e1.text != e2.text: return False
    if e1.tail != e2.tail: return False
    if e1.attrib != e2.attrib: return False
    if len(e1) != len(e2): return False
    #recursive loop for all element
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))
    #a = ET.tostring(e1)
    #b = ET.tostring(e2)
    #return (a == b)

### checking if cjk
#conversion to base 10, return 0 if failed
def deci(number):
    try:
        return int(number,16)
    except:
        return 0

# special check range function as python default range don't include ending number
def char_range(start, end):
    return range(start, end+1)
# normal range: range(0,5) --> [0,1,2,3,4], len(range(0,5))=5
# character detect range: char_range(0,5) --> [0,1,2,3,4,5], len(char_range(0,5))=6

#check range of character:
def uni_range_check(char_base10):
    #filter and count unicode
    if char_base10 in char_range(deci("4E00"), deci("9FFF")): #4E00 - 9FFF CJK Unified Ideographs
        return "basic"
    elif char_base10 in char_range(deci("2F00"), deci("2FDF")): #2F00 — 2FDF Kangxi Radicals
        return "kangxi"
    elif char_base10 in char_range(deci("2E80"), deci("2EFF")): #2E80 — 2EFF CJK Radical Supplements
        return "kangxi-sup"
    elif char_base10 == 12295: # U+3007 Ideographic Number Zero Unicode Character
        return "zero"
    elif char_base10 in char_range(deci("3400"), deci("4DBF")): #3400 — 4DBF CJK Unified Ideographs Extension A
        return "ext-a"
    elif char_base10 in char_range(deci("F900"), deci("FAFF")): #F900 — FAFF CJK Compatibility Ideographs
        return "compat"
    elif char_base10 in char_range(deci("20000"), deci("2A6DF")): #20000 — 2A6DF CJK Unified Ideographs Extension B
        return "ext-b"
    elif char_base10 in char_range(deci("2A700"), deci("2B73F")): #2A700 – 2B73F CJK Unified Ideographs Extension C
        return "ext-c"
    elif char_base10 in char_range(deci("2B740"), deci("2B81F")): #2B740 – 2B81F CJK Unified Ideographs Extension D
        return "ext-d"
    elif char_base10 in char_range(deci("2B820"), deci("2CEAF")): #2B820 – 2CEAF CJK Unified Ideographs Extension E
        return "ext-e"
    elif char_base10 in char_range(deci("2CEB0"), deci("2EBEF")): #2CEB0 – 2EBEF CJK Unified Ideographs Extension F
        return "ext-f"
    elif char_base10 in char_range(deci("2F800"), deci("2FA1F")): #2F800 — 2FA1F CJK Compatibility Ideographs Supplement
        return "compat-sup"
    elif char_base10 in char_range(deci("30000"), deci("3134F")): #30000 - 3134F CJK Unified Ideographs Extension G
        return "ext-g"
    return False
### end checking cjk

def unicode_script(uni_value):
    sorted_unicode_category_switch = {
        "Cc": "Control",
        "Cf": "Format",
        "Co": "Private",
        "Ll": "Letter",
        "Lm": "Modifier",
        "Lo": "Letter",
        "Lt": "Letter",
        "Lu": "Letter",
        "Mc": "Mark",
        "Me": "Mark",
        "Mn": "Nonspacing",
        "Nd": "Numeral",
        "Nl": "Numeral",
        "No": "Numeral",
        "Pc": "Punctuation",
        "Pd": "Punctuation",
        "Pe": "Punctuation",
        "Pf": "Punctuation",
        "Pi": "Punctuation",
        "Po": "Punctuation",
        "Ps": "Punctuation",
        "Sc": "Symbol",
        "Sk": "Modifier",
        "Sm": "Math",
        "So": "Symbol",
        "Zs": "Space",
    }
    #no unicode, return none
    if uni_value == "-":
        return "-"
    #turn to character
    uni_chr = chr(deci(uni_value))
    if uni_range_check(deci(uni_value)):
        return "Hanzi"
    uni_script, uni_property = unicodedata2.script_cat(uni_chr)
    #compare and return
    if uni_script == "Unknown":
        return sorted_unicode_category_switch.get(uni_property, "Others")
    else:
        return uni_script

### END DEF FUNC


gid=0 #keep track of number of glyphs


#region 1
last_reported_num = 0
for char in char_names_1:
    char_name = char.attrib["name"]
    if char_name in ignore_glyphs:
        continue
    
    #check if have unicode
    try:
        current_unicode = cmap_1[char_name]
        #init char name in final arr
        cmap_final[current_unicode[2:]] = {}
    except:
        current_unicode = "-"
        cmap_final["!!"+char_name] = {}
    #get glyph outline and advance info for current glyph based on name=""
    current_glyph = glyf_1.find(".//*[@name='" + char_name + "']")
    current_glyph_matrix = hmtx_1.find(".//*[@name='" + char_name + "']") 

    #try to find same glyph in font 2   --> if not found return None
    comparison_glyph_2 = glyf_2.find(".//*[@name='" + char_name + "']")
    comparison_glyph_matrix_2 = hmtx_2.find(".//*[@name='" + char_name + "']")

    #if    glyph exist                and      glyph is not empty            and       (both glyph are not same  or   second font only contain glyphs that are specific in region 2)
    if comparison_glyph_2 is not None and len(list(comparison_glyph_2)) != 0 and (not elements_equal(current_glyph, comparison_glyph_2) or is_override_only):
        #copy both glyphs from original font to final font

        #determine glyph name
        new_char_name_1 = char_name+"-"+lang_suffix_1 # region 1
        new_char_name_2 = char_name+"-"+lang_suffix_2 # region 2
        #override
        if new_char_name_1 in override_glyph_names:
            new_char_name_1 = override_glyph_names[new_char_name_1]
        if new_char_name_2 in override_glyph_names:
            new_char_name_2 = override_glyph_names[new_char_name_2]

        if current_unicode == "-" or int(current_unicode, 16) not in override_cid_map: 
            #this glyph dont hv unicode
            #or this unicode has 2 distinct region glyph, copy both over
            #rename glyph for font 1
            font_rename_1[char_name] = new_char_name_1
            #set cmap record
            if current_unicode != "-":
                cmap_final[current_unicode[2:]][lang_suffix_1] = new_char_name_1
            else:
                cmap_final["!!"+char_name][lang_suffix_1] = new_char_name_1
            #going next glyph, gid increment by 1
            gid+=1

            #rename glyph for font 2
            font_rename_2[char_name] = new_char_name_2
            #set cmap record
            if current_unicode != "-":
                cmap_final[current_unicode[2:]][lang_suffix_2] = new_char_name_2
            else:
                cmap_final["!!"+char_name][lang_suffix_2] = new_char_name_2
            # next glyph, gid increment by 1
            gid+=1

        else:  #one or both glyph are remapped to new glyph
            #assume keep overrided glyph first
            keep_glyph_1 = True
            keep_glyph_2 = True
            #cmap is not overrided
            overrided_cmap_1 = False
            overrided_cmap_2 = False
            
            #check if this unicode have override glyph for region 1
            if lang_suffix_1 in override_cid_map[int(current_unicode, 16)]:
                #record new name and uni mapping
                map_changed_1 = override_cid_map[int(current_unicode, 16)][lang_suffix_1]
                #set cmap record for region 1
                if current_unicode != "-":
                    cmap_final[current_unicode[2:]][lang_suffix_1] = map_changed_1
                else:
                    cmap_final["!!"+char_name][lang_suffix_1] = map_changed_1
                #check keep override
                if not override_cid_map[int(current_unicode, 16)]["keep"][lang_suffix_1]:
                    #dont keep the overrided glyph
                    keep_glyph_1 = False
                else:
                    #keep overrided glyph, dont add cmap record for it
                    overrided_cmap_1 = True
            #copy glyph
            if keep_glyph_1:
                #copy the original glyph over
                map_changed_1 = char_name+"-"+lang_suffix_1
                #get glyph outline and advance info for current glyph based on name=""
                current_glyph = glyf_1.find(".//*[@name='" + char_name + "']")
                current_glyph_matrix = hmtx_1.find(".//*[@name='" + char_name + "']") 
                #if glyph need to change name
                if map_changed_1 in override_glyph_names:
                    map_changed_1 = override_glyph_names[map_changed_1]
                
                #rename glyph for font 1 source
                font_rename_1[char_name] = map_changed_1
                #going next glyph, gid increment by 1
                gid+=1
                #check if not overrided
                if not overrided_cmap_1:
                    #no override, write cmap
                    #set cmap record for region 1
                    if current_unicode != "-":
                        cmap_final[current_unicode[2:]][lang_suffix_1] = map_changed_1
                    else:
                        cmap_final["!!"+char_name][lang_suffix_1] = map_changed_1


            #check if this unicode have override glyph for region 2
            if lang_suffix_2 in override_cid_map[int(current_unicode, 16)]:
                #record new name and uni mapping
                map_changed_2 = override_cid_map[int(current_unicode, 16)][lang_suffix_2]
                #set cmap record for region 2
                if current_unicode != "-":
                    cmap_final[current_unicode[2:]][lang_suffix_2] = map_changed_2
                else:
                    cmap_final["!!"+char_name][lang_suffix_2] = map_changed_2
                #check keep override
                if not override_cid_map[int(current_unicode, 16)]["keep"][lang_suffix_2]:
                    #dont keep the overrided glyph
                    keep_glyph_2 = False
                else:
                    #keep overrided glyph, dont add cmap record for it
                    overrided_cmap_2 = True
            #copy glyph
            if keep_glyph_2:
                #copy the original glyph over
                map_changed_2 = char_name+"-"+lang_suffix_2
                #get glyph outline and advance info for current glyph based on name=""
                current_glyph = glyf_2.find(".//*[@name='" + char_name + "']")
                current_glyph_matrix = hmtx_2.find(".//*[@name='" + char_name + "']") 
                #if glyph need to change name
                if map_changed_2 in override_glyph_names:
                    map_changed_2 = override_glyph_names[map_changed_2]
                
                #rename glyph for font 2 source
                font_rename_2[char_name] = map_changed_2
                # next glyph, gid increment by 1
                gid+=1
                #check if not overrided
                if not overrided_cmap_2:
                    #no override, write cmap
                    #set cmap record for region 2
                    if current_unicode != "-":
                        cmap_final[current_unicode[2:]][lang_suffix_2] = map_changed_2
                    else:
                        cmap_final["!!"+char_name][lang_suffix_2] = map_changed_2
    else:
        #only have region 1 glyph, no region 2 glyph
        #override glyph names
        if char_name in override_glyph_names:
            char_name = override_glyph_names[char_name]

        if current_unicode == "-" or int(current_unicode, 16) not in override_cid_map:
            #this glyph dont hv unicode, no override
            #no rename required
            font_rename_1[char_name] = char_name
            #both region map same glyph
            if current_unicode != "-":
                cmap_final[current_unicode[2:]][lang_suffix_1] = char_name
                cmap_final[current_unicode[2:]][lang_suffix_2] = char_name
            else:
                cmap_final["!!"+char_name][lang_suffix_1] = char_name
                cmap_final["!!"+char_name][lang_suffix_2] = char_name
            gid+=1
        else: #one of region are remapped to new glyph
            #assume keep overrided glyph first
            keep_glyph_1 = True
            keep_glyph_2 = True
            #cmap is not overrided
            overrided_cmap_1 = False
            overrided_cmap_2 = False
            
            #check if this unicode have override glyph for region 1
            if lang_suffix_1 in override_cid_map[int(current_unicode, 16)]:
                #record new name and uni mapping
                map_changed_1 = override_cid_map[int(current_unicode, 16)][lang_suffix_1]
                #set cmap record for region 1
                if current_unicode != "-":
                    cmap_final[current_unicode[2:]][lang_suffix_1] = map_changed_1
                else:
                    cmap_final["!!"+char_name][lang_suffix_1] = map_changed_1
                #check keep override
                if not override_cid_map[int(current_unicode, 16)]["keep"][lang_suffix_1]:
                    #dont keep the overrided glyph
                    keep_glyph_1 = False
                else:
                    #keep overrided glyph, dont add cmap record for it
                    overrided_cmap_1 = True
            #copy glyph
            if keep_glyph_1:
                #copy the original glyph over
                map_changed_1 = char_name+"-"+lang_suffix_1
                #get glyph outline and advance info for current glyph based on name=""
                current_glyph = glyf_1.find(".//*[@name='" + char_name + "']")
                current_glyph_matrix = hmtx_1.find(".//*[@name='" + char_name + "']") 
                #if glyph need to change name
                if map_changed_1 in override_glyph_names:
                    map_changed_1 = override_glyph_names[map_changed_1]
                
                #rename glyph for font 1 source
                font_rename_1[char_name] = map_changed_1
                #going next glyph, gid increment by 1
                gid+=1
                #check if not overrided
                if not overrided_cmap_1:
                    #no override, write cmap
                    #set cmap record for region 1
                    if current_unicode != "-":
                        cmap_final[current_unicode[2:]][lang_suffix_1] = map_changed_1
                    else:
                        cmap_final["!!"+char_name][lang_suffix_1] = map_changed_1


            #check if this unicode have override glyph for region 2
            if lang_suffix_2 in override_cid_map[int(current_unicode, 16)]:
                #record new name and uni mapping
                map_changed_2 = override_cid_map[int(current_unicode, 16)][lang_suffix_2]
                #set cmap record for region 2
                if current_unicode != "-":
                    cmap_final[current_unicode[2:]][lang_suffix_2] = map_changed_2
                else:
                    cmap_final["!!"+char_name][lang_suffix_2] = map_changed_2
                #check keep override
                if not override_cid_map[int(current_unicode, 16)]["keep"][lang_suffix_2]:
                    #dont keep the overrided glyph
                    keep_glyph_2 = False
                else:
                    #keep overrided glyph, dont add cmap record for it
                    overrided_cmap_2 = True
            #copy glyph
            if keep_glyph_2:
                #copy the original glyph over
                map_changed_2 = char_name+"-"+lang_suffix_2
                #get glyph outline and advance info for current glyph based on name=""
                current_glyph = glyf_2.find(".//*[@name='" + char_name + "']")
                current_glyph_matrix = hmtx_2.find(".//*[@name='" + char_name + "']") 
                #if glyph need to change name
                if map_changed_2 in override_glyph_names:
                    map_changed_2 = override_glyph_names[map_changed_2]
                
                #rename glyph for font 2 source
                font_rename_2[char_name] = map_changed_2
                # next glyph, gid increment by 1
                gid+=1
                #check if not overrided
                if not overrided_cmap_2:
                    #no override, write cmap
                    #set cmap record for region 2
                    if current_unicode != "-":
                        cmap_final[current_unicode[2:]][lang_suffix_2] = map_changed_2
                    else:
                        cmap_final["!!"+char_name][lang_suffix_2] = map_changed_2
    glyph_seen.append(char_name)
    
    if gid % 500 == 0:
        print("Done "+str(gid)+" glyphs.")
        last_reported_num = gid
    elif gid % 500 == 1 and (gid - 1) > last_reported_num:
        print("Done "+str(gid - 1)+" glyphs.")
        last_reported_num = gid - 1
    if gid == 65536 or gid == 65537:
        print("Warning: Total glyphs count exceed 65535 glyphs. You might want to recheck your fonts.")
    
    #emergency break in case of problem
    #if gid>501:
    #    break


#region 2
#loop through second font and directly copy anything that is not in first font, no need to add lang_suffix_2 (-TC)
for char in char_names_2:
    char_name = char.attrib["name"]
    #check if seen in font 1
    if char_name in ignore_glyphs or char_name in glyph_seen:
        continue

    #check if have unicode
    try:
        current_unicode = cmap_2[char_name]
    except:
        current_unicode = "-"
    #get glyph outline and advance info for current glyph based on name=""
    current_glyph = glyf_2.find(".//*[@name='" + char_name + "']")
    current_glyph_matrix = hmtx_2.find(".//*[@name='" + char_name + "']") 

    #if     glyph is not empty            
    if len(list(current_glyph)) != 0:
        #if glyph need to change name
        if char_name in override_glyph_names:
            new_char_name = override_glyph_names[char_name]
        else:
            new_char_name = char_name

        #no rename required, just merge in
        font_rename_2[char_name] = new_char_name
        #both region map same glyph
        if current_unicode != "-":
            if current_unicode[2:] not in cmap_final.keys():
                #init char name in final arr
                cmap_final[current_unicode[2:]] = {}
            cmap_final[current_unicode[2:]][lang_suffix_1] = new_char_name
            cmap_final[current_unicode[2:]][lang_suffix_2] = new_char_name
        else:
            if "!!"+char_name not in cmap_final.keys():
                #init char name in final arr
                cmap_final["!!"+char_name] = {}
            cmap_final["!!"+char_name][lang_suffix_1] = new_char_name
            cmap_final["!!"+char_name][lang_suffix_2] = new_char_name
        gid+=1
    glyph_seen.append(char_name)
    
    if gid % 500 == 0:
        print("Done "+str(gid)+" glyphs.")
        last_reported_num = gid
    elif gid % 500 == 1 and (gid - 1) > last_reported_num:
        print("Done "+str(gid - 1)+" glyphs.")
        last_reported_num = gid - 1
    if gid == 65536 or gid == 65537:
        print("Warning: Total glyphs count exceed 65535 glyphs. You might want to recheck your fonts.")

    #if gid>520:
    #    break

#region 3
for id, version in enumerate(font_3_arr):
    glyf_3 = font_3_arr[id]["glyf"]
    hmtx_3 = font_3_arr[id]["hmtx"]
    cmap_3 = font_3_arr[id]["cmap"]
    char_names_3 = font_3_arr[id]["char_names"]
    lang_suffix_3 = (lang_suffix_3a, lang_suffix_3b, lang_suffix_3c)[id]
    font_rename_3 = (font_rename_3a, font_rename_3b, font_rename_3c)[id]
    #region 3
    #loop through third font and copy everything into font, no need to merge according to list, add lang_suffix_3 (-JP)
    for char in char_names_3:
        char_name = char.attrib["name"]
        char_name_suffix = char_name+"-"+lang_suffix_3
        #check if seen in previous fonts
        if char_name_suffix in ignore_glyphs or char_name_suffix in glyph_seen:
            continue

        #check if have unicode
        try:
            current_unicode = cmap_3[char_name]
        except:
            current_unicode = "-"
        #get glyph outline and advance info for current glyph based on name=""
        current_glyph = glyf_3.find(".//*[@name='" + char_name + "']")
        current_glyph_matrix = hmtx_3.find(".//*[@name='" + char_name + "']") 
        
        #if     glyph is not empty            
        if len(list(current_glyph)) != 0:
            #no rename required
            font_rename_3[char_name] = char_name_suffix
            #add unicode to cmap by region
            if current_unicode != "-":
                if current_unicode[2:] not in cmap_final.keys():
                    #init char name in final arr
                    cmap_final[current_unicode[2:]] = {}
                cmap_final[current_unicode[2:]][lang_suffix_3] = char_name_suffix
            else:
                #no unicode
                if "!!"+char_name not in cmap_final.keys():
                    #init char name in final arr
                    cmap_final["!!"+char_name] = {}
                cmap_final["!!"+char_name][lang_suffix_3] = char_name_suffix
            gid+=1
        
        if gid % 500 == 0 and gid > last_reported_num:
            print("Done "+str(gid)+" glyphs.")
            last_reported_num = gid
        elif gid % 500 == 1 and (gid - 1) > last_reported_num:
            print("Done "+str(gid - 1)+" glyphs.")
            last_reported_num = gid - 1
        if gid == 65536 or gid == 65537:
            print("Warning: Total glyphs count exceed 65535 glyphs. You might want to recheck your fonts.")

        #if gid>601:
        #    break


### PARSE FONT FINISH

### START WRITING FILES


### text files for end font
# full list of glyphs in font
cid_gid_ordering = open("AI0_"+output_name+".txt", "w", encoding="utf-8") 
#format code cid_gid_ordering.write(str(cid) +"\t"+ new_char_name_1 +"\t"+ unicode_script(current_unicode) +"\t"+ current_unicode + "\n")
cid_map = open("map_"+output_name+".txt", "w", encoding="utf-8")
#format code (cid + "\t" + new_char_nmae)
cid_map.write("mergeFonts\n")

#sort glyphs that are to be copied over
#first sort by unicode, arranged by SC, TC, JP83, JP90, JP04
cid = 0
cid_list = {}
seen_cid_name = []
for unicode in cmap_final:
    for region in cmap_final[unicode]:
        glyph_name = cmap_final[unicode][region]
        if glyph_name not in seen_cid_name:
            cid_list[cid] = glyph_name
            cid_gid_ordering.write(str(cid) +"\t"+ glyph_name +"\t"+ unicode_script(unicode) +"\tU+"+ unicode.upper() + "\n")
            cid_map.write(str(cid) +"\t"+ glyph_name +"\n")
            seen_cid_name.append(glyph_name)
            cid+=1
#then append no unicode glyph at end
for remap in (font_rename_1, font_rename_2, font_rename_3a, font_rename_3b, font_rename_3c):
    for _, glyph_name in remap.items():
        if glyph_name not in seen_cid_name:
            cid_list[cid] = glyph_name
            cid_gid_ordering.write(str(cid) +"\t"+ glyph_name +"\t-\t-\n")
            cid_map.write(str(cid) +"\t"+ glyph_name +"\n")
            cid+=1
            seen_cid_name.append(glyph_name)

if cid != gid:
    print("Warning: CID not same as GID.\nCID: " + str(cid) + "\nGID: " + str(gid))

# add mapping for override if unicode is not processed yet
for uni_dec, mappings in override_cid_map.items():
    uni_str = hex(uni_dec).lower()[2:]
    if uni_str not in cmap_final.keys():
        cmap_final[uni_str] = {}
        for region, remap_char in mappings.items():
            if region == "keep":
                continue #dict store which region keep
            cmap_final[uni_str][region] = override_cid_map[uni_dec][region]

print(cmap_final)

# mapping files region 1 n 2
cmap_lang_1 = open("cmap_"+lang_suffix_1+".txt", "w", encoding="utf-8")
cmap_lang_2 = open("cmap_"+lang_suffix_2+".txt", "w", encoding="utf-8")
cmap_lang_1_var = []
cmap_lang_2_var = []

#since both region 1 n 2 must have an entry in every unicode of cid_list, just write everything in
for unicode in cmap_final:
    if unicode.startswith("!!"): #no unicode
        continue
    for region, glyph_name in cmap_final[unicode].items():
        if region == lang_suffix_1:
            cmap_lang_1_var.append("<"+ unicode.rjust(8, "0") +">\t"+ str(dict_get_key(cid_list, glyph_name)) + "\n")
            continue
        if region == lang_suffix_2:
            cmap_lang_2_var.append("<"+ unicode.rjust(8, "0") +">\t"+ str(dict_get_key(cid_list, glyph_name)) + "\n")
            continue

# mapping files for JP
cmap_lang_3b = open("cmap_"+lang_suffix_3b+".txt", "w", encoding="utf-8")
cmap_lang_3c = open("cmap_"+lang_suffix_3c+".txt", "w", encoding="utf-8")
cmap_lang_3b_var = []
cmap_lang_3c_var = []
default_3 = {}

for id, extra_3 in enumerate((extra_3b_uni, extra_3c_uni)): #for each region
    lang_suffix_3 = (lang_suffix_3b, lang_suffix_3c)[id]
    cmap_lang_3_var = (cmap_lang_3b_var, cmap_lang_3c_var)[id]
    #add override mapping
    for unicode, remap_region in extra_3.items():
        if unicode == "default":
            default_3[lang_suffix_3] = remap_region
            continue
        try:
            cmap_final[unicode][lang_suffix_3] = cmap_final[unicode][remap_region]
        except KeyError:
            print("Key "+remap_region+" not found for Unicode: U+"+unicode.upper())
    #make cmap, use default region if no remap is done
    for unicode in cmap_final:
        if unicode.startswith("!!"): #no unicode
            continue
        if lang_suffix_3 in cmap_final[unicode]: #use stored overrride
            glyph_name = cmap_final[unicode][lang_suffix_3]
        else: #use default region
            glyph_name = cmap_final[unicode][default_3[lang_suffix_3]]
        cmap_lang_3_var.append("<"+ unicode.rjust(8, "0") +">\t"+ str(dict_get_key(cid_list, glyph_name)) + "\n")

# read template file for cmap file
cmap_template_start = ""
cmap_template_end = ""
start_done = False
with open("cmap.raw") as f:
    for line in f:
        if line.strip() == "==INSERT HERE==":
            start_done = True
            continue #skip this line, no need include
        if start_done:
            cmap_template_end += line
        else:
            cmap_template_start += line

#final writing to cmap
for id, cmap_lang_var in enumerate((cmap_lang_1_var, cmap_lang_2_var, cmap_lang_3b_var, cmap_lang_3c_var)):
    cmap_lang_file = (cmap_lang_1, cmap_lang_2, cmap_lang_3b, cmap_lang_3c)[id]
    #sort cmap first
    cmap_lang_var.sort()
    #final formatting of text files    
    cmap_lang_var.insert(0, str(len(cmap_lang_var))+" begincidchar\n")
    cmap_lang_var.append("endcidchar")
    #write to file
    cmap_lang_file.write(cmap_template_start)
    cmap_lang_file.writelines(cmap_lang_var)
    cmap_lang_file.write(cmap_template_end)
    cmap_lang_file.close()

# locl feature files for all region
gsub_lang_1 = open("feature_gsub_to_"+lang_suffix_1+".fea", "w", encoding="utf-8")
gsub_lang_2 = open("feature_gsub_to_"+lang_suffix_2+".fea", "w", encoding="utf-8")
gsub_lang_3a = open("feature_gsub_to_"+lang_suffix_3a+".fea", "w", encoding="utf-8")
gsub_lang_3b = open("feature_gsub_to_"+lang_suffix_3b+".fea", "w", encoding="utf-8")
gsub_lang_3c = open("feature_gsub_to_"+lang_suffix_3c+".fea", "w", encoding="utf-8")
gsub_lang_1.write("lookup locl_to_"+lang_suffix_1+" {\n")
gsub_lang_2.write("lookup locl_to_"+lang_suffix_2+" {\n")
gsub_lang_3a.write("lookup locl_to_"+lang_suffix_3a+" {\n")
gsub_lang_3b.write("lookup locl_to_"+lang_suffix_3b+" {\n")
gsub_lang_3c.write("lookup locl_to_"+lang_suffix_3c+" {\n")

#switchable variable
gsub_lang_file = (gsub_lang_1, gsub_lang_2, gsub_lang_3a, gsub_lang_3b, gsub_lang_3c)
gsub_order = (lang_suffix_1, lang_suffix_2, lang_suffix_3a, lang_suffix_3b, lang_suffix_3c)
for unicode, mappings in cmap_final.items():
    #if not CJK then skip
    if unicode.startswith("!!") or not uni_range_check(int(unicode, 16)):
        continue
    #no new mapping, no locl feature needed
    if len(mappings) <= 1:
        continue

    for region, glyphname in mappings.items():
        gsub_lang_write = gsub_lang_file[gsub_order.index(region)]
        name_arr = feature_subarr(mappings, region)
        if len(name_arr) == 0:
            continue #no replacement
        elif len(name_arr) == 1:
            name_str = name_arr[0]
            cid_str = "\\" + str(dict_get_key(cid_list, name_str))
        else:
            name_str = "[" + " ".join(name_arr) + "]"
            #print([dict_get_key(cid_list,i) for i in name_arr])
            cid_arr = [str(dict_get_key(cid_list,i)) for i in name_arr]
            cid_str = "[\\" + " \\".join(cid_arr) + "]"
        region_glyph = mappings[region]
        region_cid = dict_get_key(cid_list, region_glyph)
        gsub_lang_write.write("    sub " + cid_str +" by \\"+ str(region_cid) + "; #" + name_str +" -> "+ region_glyph + "\n")

gsub_lang_1.write("} locl_to_"+lang_suffix_1+";")
gsub_lang_2.write("} locl_to_"+lang_suffix_2+";")
gsub_lang_3a.write("} locl_to_"+lang_suffix_3a+";")
gsub_lang_3b.write("} locl_to_"+lang_suffix_3b+";")
gsub_lang_3c.write("} locl_to_"+lang_suffix_3c+";")
gsub_lang_1.close()
gsub_lang_2.close()
gsub_lang_3a.close()
gsub_lang_3b.close()
gsub_lang_3c.close()


#write mergeFont for the final font and 
font_write_rename_1 = open("map_"+lang_suffix_1+".txt", "w", encoding="utf-8")
font_write_rename_2 = open("map_"+lang_suffix_2+".txt", "w", encoding="utf-8")
font_write_rename_3a = open("map_"+lang_suffix_3a+".txt", "w", encoding="utf-8")
font_write_rename_3b = open("map_"+lang_suffix_3b+".txt", "w", encoding="utf-8")
font_write_rename_3c = open("map_"+lang_suffix_3c+".txt", "w", encoding="utf-8")
#format code (cid + "\t" + new_char_nmae)
for id, write_file in enumerate((font_write_rename_1, font_write_rename_2, font_write_rename_3a, font_write_rename_3b, font_write_rename_3c)):
    write_file.write("mergeFonts\n")
    from_arr = (font_rename_1, font_rename_2, font_rename_3a, font_rename_3b, font_rename_3c)[id]
    for orig_name, new_name in from_arr.items():
        write_file.write(str(new_name)+"\t"+str(orig_name)+"\n")

#comparison mapping file record
comparison = open("comparison_"+output_name+".txt", "w", encoding="utf-8")

comparison.write("name\t"+"\t".join((lang_suffix_1, lang_suffix_2, lang_suffix_3a, lang_suffix_3b, lang_suffix_3c)) + "\n")
for glyph_name, mappings in cmap_final.items():
    current_write={}
    if glyph_name.startswith("!!"):
        comparison.write(glyph_name[2:])
    else:
        comparison.write("U+"+glyph_name.upper().rjust(4, "0"))
    comparison.write("\t")

    if lang_suffix_1 in mappings.keys():
        #region 1 is default, hv all glyphs
        current_write[lang_suffix_1] = mappings[lang_suffix_1]
    else:
        current_write[lang_suffix_1] = "-"

    if lang_suffix_2 in mappings.keys():
        #if region 2 share with 1 then write (=SC)
        if mappings[lang_suffix_2] == mappings[lang_suffix_1]:
            current_write[lang_suffix_2] = "(=" + lang_suffix_1 + ")"
        else:
            current_write[lang_suffix_2] = mappings[lang_suffix_2]
    else:
        current_write[lang_suffix_2] = "-"

    if lang_suffix_3a in mappings.keys():
        #3a only add, no share
        current_write[lang_suffix_3a] = mappings[lang_suffix_3a]
    else:
        current_write[lang_suffix_3a] = "-"
    
    #check region 3 one by one
    for id, lang_suffix_3 in enumerate((lang_suffix_3b, lang_suffix_3c)):
        extra_3_uni = (extra_3b_uni, extra_3c_uni)[id]
        #if have mapping
        if lang_suffix_3 in mappings.keys():
            if glyph_name in extra_3_uni: #shared glyph
                current_write[lang_suffix_3] = "(=" + extra_3_uni[glyph_name] + ")"
            else: #new glyph
                current_write[lang_suffix_3] = mappings[lang_suffix_3]
        else: #no mapping, use default region
            if not current_write[default_3[lang_suffix_3]].startswith("(="):
                current_write[lang_suffix_3] = "(=" + default_3[lang_suffix_3] + ")"
            else: #map to map to region
                current_write[lang_suffix_3] = current_write[default_3[lang_suffix_3]]
    comparison.write("\t".join(current_write.values()))
    comparison.write("\n")

# DONE
print("Merge done.\nTotal glyphs in merged font: " + str(cid))