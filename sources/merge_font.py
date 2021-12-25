import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
import unicodedata2 # https://stackoverflow.com/questions/9868792/find-out-the-unicode-script-of-a-character
import sys
import os

#input font name
font_1_name = "WD-XLLubrifont-Regular.ttf"
font_2_name = "WD-XLLubrifont-Trad.ttf"
font_3_name = "WD-XLLubrifont-JP.ttf"

#output font file
output_xml = "HuaYou.ttx"
output_template_xml = "HuaYou-base.ttx"

#language tag (all caps)
lang_suffix_1 = "SC"
lang_suffix_2 = "TC"
lang_suffix_3 = "JP"
#does second font contains only glyphs to the specific region 2 only?
is_override_only = True

#override file
override_glyph_names_file = "huayou-override-name.txt"
override_cid_map_file = "huayou-override-map.txt"
override_uni_map_file = "huayou-override-uni.txt"

#ignore glyphs list
ignore_glyphs = [".IDCext"]

try:
    #open the font and convert to xml with ttx
    ttx_name_1 = font_1_name[:-4]+".xml"
    ttx_name_2 = font_2_name[:-4]+".xml"
    ttx_name_3 = font_3_name[:-4]+".xml"
    #if file exist then skip
    if not os.path.isfile(ttx_name_1) or not os.path.isfile(output_template_xml):
        ttfont_var_1 = TTFont(font_1_name)
        ttfont_var_1.saveXML(ttx_name_1,newlinestr="\n",tables=["GlyphOrder","glyf","hmtx","cmap"])
        #sample base to be merged in
        ttfont_var_1.saveXML(output_template_xml,newlinestr="\n",skipTables=["GlyphOrder","glyf","hmtx","cmap","GPOS","GSUB","GDEF"])
        ttfont_var_1.close()
        print("Font 1 converted to XML.")
    #region 2
    if not os.path.isfile(ttx_name_2):
        ttfont_var_2 = TTFont(font_2_name)
        ttfont_var_2.saveXML(ttx_name_2,newlinestr="\n",tables=["GlyphOrder","glyf","hmtx","cmap"])
        ttfont_var_2.close()
        print("Font 2 converted to XML.")
    #JP special
    if not os.path.isfile(ttx_name_3):
        ttfont_var_3 = TTFont(font_3_name)
        ttfont_var_3.saveXML(ttx_name_3,newlinestr="\n",tables=["GlyphOrder","glyf","hmtx","cmap"])
        ttfont_var_3.close()
        print("Font 3 converted to XML.")
except IOError:
    print("Font could not be opened.")
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
except:
    print("No override name files detected.")

### override CID to code mapping
override_cid_map = {}
#try:
with open(override_cid_map_file, "r", encoding="utf-8") as override_file:
    for line in override_file:
        if line.startswith(("#", "//")):
            continue # ignore commented line
        unicode, region, remap_char_name = line.strip("\n").split(",")
        #change unicode to 
        uni_int_val = int(unicode, 16)
        if uni_int_val not in override_cid_map:
            override_cid_map[uni_int_val] = {}
        override_cid_map[uni_int_val][region] = remap_char_name
#except:
#    print("No override CID mapping files detected.")
#list to store affected glyphs by changes, initiate by region
override_cid_map_affected = {}
for region in [lang_suffix_1, lang_suffix_2, lang_suffix_3]: #initiate both dict above by region
    override_cid_map_affected[region] = {} 



### text files for end font
# full list of glyphs in font
cid_gid_ordering = open("AI0_"+output_xml[:-4]+".txt", "w", encoding="utf-8")
cid_map = open("map_"+output_xml[:-4]+".txt", "w", encoding="utf-8")
cid_map.write("mergeFonts\n")
cid_list = {}

# mapping files and feature files per locale
cmap_lang_1 = open("cmap_"+lang_suffix_1+".txt", "w", encoding="utf-8")
cmap_lang_2 = open("cmap_"+lang_suffix_2+".txt", "w", encoding="utf-8")
cmap_lang_1_var = []
cmap_lang_2_var = []
gsub_lang_1 = open("feature_gsub_"+lang_suffix_2+"_to_"+lang_suffix_1+".fea", "w", encoding="utf-8")
gsub_lang_2 = open("feature_gsub_"+lang_suffix_1+"_to_"+lang_suffix_2+".fea", "w", encoding="utf-8")
gsub_lang_1.write("lookup locl_"+lang_suffix_2+"_to_"+lang_suffix_1+" {\n")
gsub_lang_2.write("lookup locl_"+lang_suffix_1+"_to_"+lang_suffix_2+" {\n")
gsub_lang_end_write = [] #store changed mapping pairs to write in the end
#convert 1 to 2 for quick check
substitute_list = open("convert_"+lang_suffix_1+"_"+lang_suffix_2+".txt", "w", encoding="utf-8")
substitute_list.write("orig,"+lang_suffix_1+","+lang_suffix_2+"\n")
#convert 1 to 3 for quick check
region_3_list = open("convert_"+lang_suffix_1+"_"+lang_suffix_3+".txt", "w", encoding="utf-8")
region_3_list.write("orig,"+lang_suffix_1+","+lang_suffix_3+"\n")

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
    #=> {".notdef":"0", "A":"0020"}
#or could use: cmap_temp.find(".//*[@name='char_name']").attrib["code"]
#get list of glyph names in the font
char_names_2 = font_root_2.find('GlyphOrder')


#load font 3
font_tree_3 = ET.parse(ttx_name_3)
font_root_3 = font_tree_3.getroot() #<ttFont sfntVersion="\x00\x01\x00\x00" ttLibVersion="3.44">

#get separable tables
glyf_3 = font_root_3.find('glyf') # <TTGlyph name="char_name" xMin="int" yMin="int" xMax="int" yMax="int">
hmtx_3 = font_root_3.find('hmtx') # <mtx name="char_name" width="int" lsb="int"/>
cmap_temp_3 = font_root_3.find('./cmap/cmap_format_12') # only need format 12 coz format 4 redundant, <map code="0xunicode" name="char_name"/>
cmap_3 = {}
for item in cmap_temp_3: #convert format
    cmap_3[item.attrib["name"]] = item.attrib["code"]
    #=> {".notdef":"0", "A":"0020"}
#or could use: cmap_temp.find(".//*[@name='char_name']").attrib["code"]
#get list of glyph names in the font
char_names_3 = font_root_3.find('GlyphOrder')


#create empty root for final font
end_font_root = ET.Element("ttFont")
end_font_root.set("sfntVersion", font_root_1.attrib["sfntVersion"])
end_font_root.set("ttLibVersion", font_root_1.attrib["ttLibVersion"])
#prepare table, GlyphOrder must before glyf to parse correctly
end_font_glyphorder = ET.SubElement(end_font_root,"GlyphOrder")
end_font_glyf = ET.SubElement(end_font_root,"glyf")
end_font_hmtx = ET.SubElement(end_font_root,"hmtx")
end_font_cmap = ET.SubElement(end_font_root,"cmap") #empty filler, mapping should be fixed in AFDKO
#adding <tableVersion version="0"/>
end_font_cmap_tableVer = ET.SubElement(end_font_cmap,"tableVersion")
end_font_cmap_tableVer.set("version", "0")
#adding <cmap_format_4 platformID="3" platEncID="1" language="0">
end_font_cmap_format4 = ET.SubElement(end_font_cmap,"cmap_format_4")
end_font_cmap_format4.set("platformID", "3")
end_font_cmap_format4.set("platEncID", "1")
end_font_cmap_format4.set("language", "0")
#adding <cmap_format_12 platformID="3" platEncID="10" format="12" reserved="0" length="63028" language="0" nGroups="5251">
end_font_cmap_format12 = ET.SubElement(end_font_cmap,"cmap_format_12")
end_font_cmap_format12.set("platformID", "3")
end_font_cmap_format12.set("platEncID", "10")
end_font_cmap_format12.set("format", "12")
end_font_cmap_format12.set("reserved", "0")
end_font_cmap_format12.set("length", cmap_temp_1.attrib["length"])
end_font_cmap_format12.set("language", "0")
end_font_cmap_format12.set("nGroups", cmap_temp_1.attrib["nGroups"])


end_font = (end_font_glyf,end_font_hmtx,end_font_cmap,end_font_glyphorder)

### STR DEF FUNC
def get_cid_by_char_name(my_dict, name):
    key_list = list(my_dict.keys())
    val_list = list(my_dict.values())
    position = val_list.index(name)
    return key_list[position]

def copy_glyph_to_end_font(cid, in_glyf_record, in_hmtx_record, in_unicode, in_char_name, end_font):
    #return the glyph id in end_font file
    end_glyf, end_hmtx, end_cmap, end_glyphorder = end_font
    #change the glyph name before adding
    in_glyf_record.attrib["name"] = in_char_name
    in_hmtx_record.attrib["name"] = in_char_name
    #adding into font
    end_glyf.append(in_glyf_record)
    end_hmtx.append(in_hmtx_record)
    #create subelement in glyph order
    current_gid = ET.SubElement(end_glyphorder,"GlyphID")
    current_gid.attrib["id"] = str(cid) #must string, else error
    current_gid.attrib["name"] = in_char_name

    if in_unicode != "-": #if have unicode value
        #find cmap subtable
        end_format4 = end_cmap.find('./cmap_format_4')
        end_format12 = end_cmap.find('./cmap_format_12')
        #create subelement in format 12 (full unicode repetiore)
        current_map_tag = ET.SubElement(end_format12,"map")
        current_map_tag.set("code", in_unicode)
        current_map_tag.set("name", in_char_name)
        #adding cmap
        #format 4 accepts bmp only
        if int(in_unicode[2:],16) <= int(0xFFFF):
            end_format4.append(current_map_tag)
    #return gid
    #return list(end_glyf).index(in_glyf_record)
    #in new font, gid=cid, just return cid
    return cid


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
    uni_chr = chr(deci(uni_value[2:]))
    if uni_range_check(deci(uni_value[2:])):
        return "Hanzi"
    uni_script, uni_property = unicodedata2.script_cat(uni_chr)
    #compare and return
    if uni_script == "Unknown":
        return sorted_unicode_category_switch.get(uni_property, "Others")
    else:
        return uni_script

### END DEF FUNC


cid=0 #keep track of cid
glyph_seen = [] #check if the glyph is copied for next font (use font glyph name)

glyph_split = [] #list of glyphs that has TC (unicode only)

#region 1
last_reported_num = 0
for char in char_names_1:
    char_name = char.attrib["name"]
    if char_name in ignore_glyphs:
        continue
    
    #check if have unicode
    try:
        current_unicode = cmap_1[char_name]
    except:
        current_unicode = "-"
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
            #copy glyph over from font 1
            font_glyph_id_1 = copy_glyph_to_end_font(cid, current_glyph, current_glyph_matrix, current_unicode, new_char_name_1, end_font)
            #prepare cmap file for makeotf
            #write CID \t .notdef_SC \t GID \t Unicode
            #glyph from lang 1 (SC), lang 2 (TC) no unicode
            cid_gid_ordering.write(str(cid) +"\t"+ new_char_name_1 +"\t"+ unicode_script(current_unicode) +"\t"+ current_unicode + "\n")
            cid_map.write(str(cid) +"\t"+ new_char_name_1 + "\n")
            cid_list[cid] = new_char_name_1
            if current_unicode != "-":
                cmap_lang_1_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
            
            #going next glyph, cid increment by 1
            cid+=1

            #copy glyph over from font 2, default end font dont have cmap for this record
            font_glyph_id_2 = copy_glyph_to_end_font(cid, comparison_glyph_2, comparison_glyph_matrix_2, "-", new_char_name_2, end_font)
            cid_gid_ordering.write(str(cid) +"\t"+ new_char_name_2 +"\t"+ unicode_script(current_unicode) +"\t"+ current_unicode + "\n")
            cid_map.write(str(cid) +"\t"+ new_char_name_2 + "\n")
            cid_list[cid] = new_char_name_2
            #glyph from lang 2 (TC), lang 1 (SC) no unicode
            if current_unicode != "-":
                cmap_lang_2_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
            
            # next glyph, cid increment by 1
            cid+=1

            # write locale sub
            gsub_lang_1.write("    sub \\" + str(font_glyph_id_2) +" by \\"+ str(font_glyph_id_1) + "; #" + new_char_name_2 +" -> "+ new_char_name_1 + "\n")
            gsub_lang_2.write("    sub \\" + str(font_glyph_id_1) +" by \\"+ str(font_glyph_id_2) + "; #" + new_char_name_1 +" -> "+ new_char_name_2 + "\n")
            

            substitute_list.write(char_name + "," + new_char_name_1 + "," + new_char_name_2 + "\n")

        else:  #one or both glyph are remapped to new glyph
            #get the new char name region 1
            if lang_suffix_1 in override_cid_map[int(current_unicode, 16)]:
                #record new name
                map_changed_1 = override_cid_map[int(current_unicode, 16)][lang_suffix_1]
            else:
                #copy the original glyph over
                map_changed_1 = char_name+"-"+lang_suffix_1
                #get glyph outline and advance info for current glyph based on name=""
                current_glyph = glyf_1.find(".//*[@name='" + char_name + "']")
                current_glyph_matrix = hmtx_1.find(".//*[@name='" + char_name + "']") 
                #if glyph need to change name
                if map_changed_1 in override_glyph_names:
                    map_changed_1 = override_glyph_names[map_changed_1]
                
                #copy glyph from original font to final font
                font_glyph_id = copy_glyph_to_end_font(cid, current_glyph, current_glyph_matrix, current_unicode, map_changed_1, end_font)
                cid_gid_ordering.write(str(cid) +"\t"+ map_changed_1 +"\t"+ unicode_script(current_unicode) +"\t"+ current_unicode + "\n")
                cid_map.write(str(cid) +"\t"+ map_changed_1 + "\n")
                cid_list[cid] = map_changed_1
                if current_unicode != "-":
                    cmap_lang_1_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
                # next glyph, cid increment by 1
                cid+=1

            #get the new char name region 2
            if lang_suffix_2 in override_cid_map[int(current_unicode, 16)]:
                #record new name
                map_changed_2 = override_cid_map[int(current_unicode, 16)][lang_suffix_2]
            else:
                #copy the original glyph over
                map_changed_2 = char_name+"-"+lang_suffix_2
                #get glyph outline and advance info for current glyph based on name=""
                current_glyph = glyf_2.find(".//*[@name='" + char_name + "']")
                current_glyph_matrix = hmtx_2.find(".//*[@name='" + char_name + "']") 
                #if glyph need to change name
                if map_changed_2 in override_glyph_names:
                    map_changed_2 = override_glyph_names[map_changed_2]
                
                #copy glyph from original font to final font
                font_glyph_id = copy_glyph_to_end_font(cid, current_glyph, current_glyph_matrix, current_unicode, map_changed_2, end_font)
                cid_gid_ordering.write(str(cid) +"\t"+ map_changed_2 +"\t"+ unicode_script(current_unicode) +"\t"+ current_unicode + "\n")
                cid_map.write(str(cid) +"\t"+ map_changed_2 + "\n")
                cid_list[cid] = map_changed_2
                if current_unicode != "-":
                    cmap_lang_2_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
                # next glyph, cid increment by 1
                cid+=1
            #add to locale sub
            gsub_lang_end_write.append((map_changed_1, map_changed_2))
            
            substitute_list.write(char_name + "," + map_changed_1 + "," + map_changed_2 + "\n")


        #record this unicode has splitted glyph
        glyph_split.append(current_unicode)

    
    else:
        #only have region 1 glyph, no region 2 glyph
        #override glyph names
        if char_name in override_glyph_names:
            char_name = override_glyph_names[char_name]

        if current_unicode == "-" or int(current_unicode, 16) not in override_cid_map:
            #this glyph dont hv unicode, no override
            #both region use same glyph
            font_glyph_id = copy_glyph_to_end_font(cid, current_glyph, current_glyph_matrix, current_unicode, char_name, end_font)
            cid_gid_ordering.write(str(cid) +"\t"+ char_name +"\t"+ unicode_script(current_unicode) +"\t"+ current_unicode + "\n")
            cid_map.write(str(cid) +"\t"+ char_name + "\n")
            if current_unicode != "-":
                cmap_lang_1_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
                cmap_lang_2_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
            cid+=1
        else: #one of region are remapped to new glyph
            #get the new char name region 1
            if lang_suffix_1 in override_cid_map[int(current_unicode, 16)]:
                #record new name
                map_changed_1 = override_cid_map[int(current_unicode, 16)][lang_suffix_1]
            else:
                #copy the original glyph over as lang 1 glyph
                map_changed_1 = char_name+"-"+lang_suffix_1
                #get glyph outline and advance info for current glyph based on name=""
                current_glyph = glyf_1.find(".//*[@name='" + char_name + "']")
                current_glyph_matrix = hmtx_1.find(".//*[@name='" + char_name + "']") 
                #if glyph need to change name
                if map_changed_1 in override_glyph_names:
                    map_changed_1 = override_glyph_names[map_changed_1]
                
                #copy glyph from original font to final font
                font_glyph_id = copy_glyph_to_end_font(cid, current_glyph, current_glyph_matrix, current_unicode, map_changed_1, end_font)
                cid_gid_ordering.write(str(cid) +"\t"+ map_changed_1 +"\t"+ unicode_script(current_unicode) +"\t"+ current_unicode + "\n")
                cid_map.write(str(cid) +"\t"+ map_changed_1 + "\n")
                cid_list[cid] = map_changed_1
                if current_unicode != "-":
                    cmap_lang_1_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
                # next glyph, cid increment by 1
                cid+=1

            #get the new char name region 2
            if lang_suffix_2 in override_cid_map[int(current_unicode, 16)]:
                #record new name
                map_changed_2 = override_cid_map[int(current_unicode, 16)][lang_suffix_2]
            else:
                #copy the original glyph in region 1 over as region glyph 2
                map_changed_2 = char_name+"-"+lang_suffix_2
                #get glyph outline and advance info for current glyph based on name=""
                current_glyph = glyf_1.find(".//*[@name='" + char_name + "']")
                current_glyph_matrix = hmtx_1.find(".//*[@name='" + char_name + "']") 
                #if glyph need to change name
                if map_changed_2 in override_glyph_names:
                    map_changed_2 = override_glyph_names[map_changed_2]
                
                #copy glyph from original font to final font
                font_glyph_id = copy_glyph_to_end_font(cid, current_glyph, current_glyph_matrix, current_unicode, map_changed_2, end_font)
                cid_gid_ordering.write(str(cid) +"\t"+ map_changed_2 +"\t"+ unicode_script(current_unicode) +"\t"+ current_unicode + "\n")
                cid_map.write(str(cid) +"\t"+ map_changed_2 + "\n")
                cid_list[cid] = map_changed_2
                if current_unicode != "-":
                    cmap_lang_2_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
                # next glyph, cid increment by 1
                cid+=1
            #add to locale sub
            gsub_lang_end_write.append((map_changed_1, map_changed_2))
            
            substitute_list.write(char_name + "," + map_changed_1 + "," + map_changed_2 + "\n")
    glyph_seen.append(char_name)
    
    if cid % 500 == 0:
        print("Done "+str(cid)+" glyphs.")
        last_reported_num = cid
    elif cid % 500 == 1 and (cid - 1) > last_reported_num:
        print("Done "+str(cid - 1)+" glyphs.")
        last_reported_num = cid - 1
    
    if cid == 65536 or cid == 65537:
        print("Warning: Total glyphs count exceed 65535 glyphs. You might want to recheck your fonts.")
    
    #emergency break in case of problem
    #if cid>501:
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
        #copy glyph from original font to final font
        font_glyph_id = copy_glyph_to_end_font(cid, current_glyph, current_glyph_matrix, current_unicode, new_char_name, end_font)
        cid_gid_ordering.write(str(cid) +"\t"+ new_char_name +"\t"+ unicode_script(current_unicode) +"\t"+ current_unicode + "\n")
        cid_map.write(str(cid) +"\t"+ new_char_name + "\n")
        cid_list[cid] = new_char_name
        if current_unicode != "-":
            cmap_lang_1_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
            cmap_lang_2_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
        cid+=1
    glyph_seen.append(char_name)
    
    if cid % 500 == 0:
        print("Done "+str(cid)+" glyphs.")
        last_reported_num = cid
    elif cid % 500 == 1 and (cid - 1) > last_reported_num:
        print("Done "+str(cid - 1)+" glyphs.")
        last_reported_num = cid - 1

    if cid == 65536 or cid == 65537:
        print("Warning: Total glyphs count exceed 65535 glyphs. You might want to recheck your fonts.")

    #if cid>520:
    #    break


#region 3
#loop through third font and copy everything into font, no need to merge according to list, add lang_suffix_3 (-JP)
for char in char_names_3:
    char_name = char.attrib["name"]
    char_name_suffix = char_name+"-"+lang_suffix_3
    #check if seen in font 1
    if char_name_suffix in ignore_glyphs or char_name_suffix in glyph_seen:
        continue

    #lang 3 do not map to unicode, just copy as appended glyph
    current_unicode = "-"
    #get glyph outline and advance info for current glyph based on name=""
    current_glyph = glyf_3.find(".//*[@name='" + char_name + "']")
    current_glyph_matrix = hmtx_3.find(".//*[@name='" + char_name + "']") 
    
    #if     glyph is not empty            
    if len(list(current_glyph)) != 0:
        #copy glyph from original font to final font
        font_glyph_id = copy_glyph_to_end_font(cid, current_glyph, current_glyph_matrix, current_unicode, char_name_suffix, end_font)
        cid_gid_ordering.write(str(cid) +"\t"+ char_name_suffix +"\t"+ unicode_script(current_unicode) +"\t"+ current_unicode + "\n")
        cid_map.write(str(cid) +"\t"+ char_name_suffix + "\n")
        cid_list[cid] = char_name_suffix
        #if current_unicode != "-": #lang 3 no mapping to unicode
        #    cmap_lang_1_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
        #    cmap_lang_2_var.append("<"+ current_unicode[2:].rjust(8, "0") +">\t"+ str(cid) + "\n")
        cid+=1
    glyph_seen.append(char_name)
    
    if cid % 500 == 0:
        print("Done "+str(cid)+" glyphs.")
        last_reported_num = cid
    elif cid % 500 == 1 and (cid - 1) > last_reported_num:
        print("Done "+str(cid - 1)+" glyphs.")
        last_reported_num = cid - 1

    if cid == 65536 or cid == 65537:
        print("Warning: Total glyphs count exceed 65535 glyphs. You might want to recheck your fonts.")

    #if cid>601:
    #    break

#write remaining unmapped unicode in override_cid_map
for uni_int_val, lang_mapping in override_cid_map.items():
    #convert unicode value from integer back to hex string (w/out 0x)
    unicode_str = str(hex(uni_int_val))[2:]
    if lang_suffix_1 in lang_mapping:
        new_char_name = lang_mapping[lang_suffix_1]
        if new_char_name in cid_list.values():
            cid = get_cid_by_char_name(cid_list, new_char_name)
        else:
            print("Remapped glyph not found for cmap. Glyph name: "+ new_char_name)
            continue
        cmap_lang_1_var.append("<"+ unicode_str.lower().rjust(8, "0") +">\t"+ str(cid) + "\n")
    if lang_suffix_2 in lang_mapping:
        new_char_name = lang_mapping[lang_suffix_2]
        if new_char_name in cid_list.values():
            cid = get_cid_by_char_name(cid_list, new_char_name)
        else:
            print("Remapped glyph not found for cmap. Glyph name: "+ new_char_name)
            continue
        cmap_lang_2_var.append("<"+ unicode_str.lower().rjust(8, "0") +">\t"+ str(cid) + "\n")


#write final file for locale gsub (gsub for diff glyph in diff region)
for (char_name_2, char_name_1) in gsub_lang_end_write:
    #skip if substitute glyph not found
    try:
        cid_1 = get_cid_by_char_name(cid_list, char_name_1)
    except:
        print("Remapped glyph not found for gsub. Glyph name: "+ char_name_1)
        continue
    try:
        cid_2 = get_cid_by_char_name(cid_list, char_name_2)
    except:
        print("Remapped glyph not found for gsub. Glyph name: "+ char_name_2)
        continue
    #skip if both cid end up same
    if cid_1 == cid_2:
        continue
    gsub_lang_1.write("    sub \\" + str(cid_2) +" by \\"+ str(cid_1) + "; #" + char_name_2 +" -> "+ char_name_1 + "\n")
    gsub_lang_2.write("    sub \\" + str(cid_1) +" by \\"+ str(cid_2) + "; #" + char_name_1 +" -> "+ char_name_2 + "\n")

#sort cmap first
cmap_lang_1_var.sort()
cmap_lang_2_var.sort()

#final formatting of text files    
cmap_lang_1_var.insert(0, str(len(cmap_lang_1_var))+" begincidchar\n")
cmap_lang_2_var.insert(0, str(len(cmap_lang_2_var))+" begincidchar\n")
cmap_lang_1_var.append("endcidchar")
cmap_lang_2_var.append("endcidchar")
cmap_lang_1.writelines(cmap_lang_1_var)
cmap_lang_2.writelines(cmap_lang_2_var)
gsub_lang_1.write("} locl_TC_to_SC;")
gsub_lang_2.write("} locl_SC_to_TC;")

#pretty wrap xml
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

#pretty wrap root by adding spaces to end
#https://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
indent(end_font_root)
#wrap Element in ElementTree
end_font_tree = ET.ElementTree(end_font_root)
end_font_tree.write(output_xml, encoding='utf-8', xml_declaration=True)

print("Merge done.\nTotal glyphs in merged font: " + str(cid) + "\nFinal file in: " + output_xml)