
from os import chdir, cpu_count, name, write


UVS_filename = "UVS_sequence"
output_filename = "UVS_sequence_CID"

name2cid_filename = "AI0_HuaYou.txt"

def uni_rename(hex_str): #input 0xabcd
    uni_val = hex_str[2:]
    if len(uni_val) > 4:
        return "u"+uni_val.upper()
    else:
        return "uni"+uni_val.upper()

name2cid_list = {}
with open(name2cid_filename, "r", encoding="utf-8") as name2cid_open:
    for line in name2cid_open:
        #reading csv
        #convert_arr = line.strip("\n").split(",")
        #reading AI0 file
        convert_arr = line.strip("\n").split("\t")
        name2cid_list[convert_arr[1]] = " CID+"+convert_arr[0]

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

with open(UVS_filename, "r", encoding="utf-8") as feature_str:
    output_file = open(output_filename, "w", encoding="utf-8")

    #check line by line
    for line in feature_str:
        #check for comments
        if line.strip().startswith("#"):
            output_file.write(line+"\n")
            continue
        #skip empty lines
        if line.strip() == "":
            output_file.write("\n")
            continue
        
        #split by ; and convert last one to cid
        word_arr = line.strip().split(";")

        write_arr = []

        write_arr.append(word_arr[0])
        write_arr.append(word_arr[1])
        
        if word_arr[2].strip() in name2cid_list.keys():
            write_arr.append(name2cid_list[word_arr[2].strip()])
        else:
            found_new_name = False
            while not found_new_name:
                new_glyph_name, found = ask_new_name(word_arr[2].strip(), name2cid_list)
                if found: #pressed enter
                    write_arr.append(name2cid_list[new_glyph_name])
                    found_new_name = True
        
        output_file.write(";".join(write_arr))
        output_file.write(" #" + word_arr[2].strip()) #write unconverted terms as comments
        output_file.write("\n")

