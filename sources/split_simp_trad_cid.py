import csv
from tkinter.ttk import Separator

#convert source
#conversion_name = "simp-to-trad" #trad-to-simp simp-to-trad
for conversion_name in ["trad-to-simp","simp-to-trad"]:
    output_name_prefix = conversion_name.replace("-","_")

    #read source file
    input_file = open("csv-"+conversion_name+".txt", "r", encoding="utf-8")
    #write output file
    output_file = open("feature-ot-"+conversion_name+"-split.fea", "w", encoding="utf-8")

    #read name-cid map list
    name2cid_filename = "AI0_HuaYou.txt"
    name2cid_list = {}
    with open(name2cid_filename, "r", encoding="utf-8") as name2cid_open:
        for line in name2cid_open:
            #reading csv
            #convert_arr = line.strip("\n").split(",")
            #reading AI0 file
            convert_arr = line.strip("\n").split("\t")
            name2cid_list[convert_arr[1]] = "\\"+convert_arr[0]

    #read SC-TC different glyph list
    split_file = open("comparison_HuaYou.txt", "r", encoding="utf-8")
    split_reader = csv.reader(split_file, delimiter="\t")
    diff_chars = {}
    keys=[]
    for number, line in enumerate(split_reader):
        if number == 0:
            #initialize
            diff_chars[line[0]]=[]
            diff_chars[line[1]]=[]
            diff_chars[line[2]]=[]
            keys = [line[0], line[1], line[2]] #orig, SC, TC
            continue
        if line[2].startswith("(="):
            continue #no difference
        if line[0].startswith("U+"):
            uni_hex = line[0][2:]
            if len(uni_hex) == 4:
                uni_str = "uni"+uni_hex.upper()
            else:
                uni_str = "u"+uni_hex.upper()
            diff_chars[keys[0]].append(uni_str)
        else:
            diff_chars[keys[0]].append(line[0])
        diff_chars[keys[1]].append(line[1])
        diff_chars[keys[2]].append(line[2])

    #define for final output
    grouped_output=[] #for sub X from []
    individual_output=[] #for sub X by Y
    differentiated_output_1 = []
    differentiated_output_2 = []


    ### START CONVERSION
    multi = True
    for line in input_file:
        #line marker
        if line.strip("\n") == "#START ONE-TO-MANY":
            multi = True
            continue
        if line.strip("\n") == "#START ONE-TO-ONE":
            multi = False
            continue

        #parsing and making new file
        search, replace = line.strip("\n").split("->")
        if multi: #one to many scenario
            #split many into arr
            if ";" in replace: #one to many
                replace_arr = replace.split(";")
                output_arr = [] #store final output terms with suffix (if have)
                for item in replace_arr:
                    if item in diff_chars[keys[0]]: #if have 2 region
                        index_no_item = diff_chars[keys[0]].index(item)
                        output_arr.append(name2cid_list[diff_chars[keys[1]][index_no_item]])
                        output_arr.append(name2cid_list[diff_chars[keys[2]][index_no_item]])
                    else:
                        output_arr.append(name2cid_list[item])
                #if search term hv suffix (sub -SC from X,Y,Z; sub -TC from X,Y,Z) -> can be used for both font
                if search in diff_chars[keys[0]]:
                    index_no_search = diff_chars[keys[0]].index(search)
                    grouped_output.append("    sub "+ name2cid_list[diff_chars[keys[1]][index_no_search]] + " from [ " + " ".join(output_arr) + " ] ;\n")
                    grouped_output.append("    sub "+ name2cid_list[diff_chars[keys[2]][index_no_search]] + " from [ " + " ".join(output_arr) + " ] ;\n")
                else: #search term no suffix (sub A from [X,Y,Z])
                    grouped_output.append("    sub "+ name2cid_list[search] + " from [ " + " ".join(output_arr) + " ] ;\n")
            else: #one to one
                #if replaced term has different suffix (SC/TC)
                if replace in diff_chars[keys[0]]:
                    #if search has different suffix (sub -SC from [-SC -TC]; sub -TC from [-SC -TC]) -> can be applied to both font
                    if search in diff_chars[keys[0]]:
                        index_no_search = diff_chars[keys[0]].index(search)
                        index_no_replace = diff_chars[keys[0]].index(replace)
                        grouped_output.append("    sub "+ name2cid_list[diff_chars[keys[1]][index_no_search]] + " from [ " + name2cid_list[diff_chars[keys[1]][index_no_replace]] + " " + name2cid_list[diff_chars[keys[2]][index_no_replace]] + " ] ;\n")
                        grouped_output.append("    sub "+ name2cid_list[diff_chars[keys[2]][index_no_search]] + " from [ " + name2cid_list[diff_chars[keys[1]][index_no_replace]] + " " + name2cid_list[diff_chars[keys[2]][index_no_replace]] + " ] ;\n")
                    else: #seach dont hv different suffix (sub X from [-SC -TC]) -> one liner for both fonts
                        index_no_replace = diff_chars[keys[0]].index(replace)
                        grouped_output.append("    sub "+ name2cid_list[search] + " from [ " + name2cid_list[diff_chars[keys[1]][index_no_replace]] + " " + name2cid_list[diff_chars[keys[2]][index_no_replace]] + " ] ;\n")
                #if replaced dont have different suffix, but search term does (sub -SC from X; sub -TC from X) -> still be accessed from both font
                elif search in diff_chars[keys[0]]:
                    index_no_search = diff_chars[keys[0]].index(search)
                    grouped_output.append("    sub "+ name2cid_list[diff_chars[keys[1]][index_no_search]] + " from [ " + name2cid_list[replace] + " ] ;\n")
                    grouped_output.append("    sub "+ name2cid_list[diff_chars[keys[2]][index_no_search]] + " from [ " + name2cid_list[replace] + " ] ;\n")
                #if both dont have suffix (sub A from [X])
                else:
                    grouped_output.append("    sub "+ name2cid_list[search] + " from [ " + name2cid_list[replace] + " ] ;\n")
        else: #one to one scenario
            #if replaced term has different suffix (SC/TC)
            if replace in diff_chars[keys[0]]:
                #if search has different suffix (sub -SC by -SC; sub -TC by -TC) -> can be applied to both font
                if search in diff_chars[keys[0]]:
                    index_no_search = diff_chars[keys[0]].index(search)
                    index_no_replace = diff_chars[keys[0]].index(replace)
                    individual_output.append("    sub "+ name2cid_list[diff_chars[keys[1]][index_no_search]] + " by " + name2cid_list[diff_chars[keys[1]][index_no_replace]] + ";\n")
                    individual_output.append("    sub "+ name2cid_list[diff_chars[keys[2]][index_no_search]] + " by " + name2cid_list[diff_chars[keys[2]][index_no_replace]] + ";\n")
                else: #seach dont hv different suffix (sub X by -SC/-TC) -> only used in one font
                    index_no_replace = diff_chars[keys[0]].index(replace)
                    differentiated_output_1.append("    sub "+ name2cid_list[search] + " by " + name2cid_list[diff_chars[keys[1]][index_no_replace]] + ";\n")
                    differentiated_output_2.append("    sub "+ name2cid_list[search] + " by " + name2cid_list[diff_chars[keys[2]][index_no_replace]] + ";\n")
            #if replaced dont have different suffix, but search term does (sub [-SC -TC] by X) -> one liner for both fonts
            elif search in diff_chars[keys[0]]:
                index_no_search = diff_chars[keys[0]].index(search)
                individual_output.append("    sub [ "+ name2cid_list[diff_chars[keys[1]][index_no_search]] + " " + name2cid_list[diff_chars[keys[2]][index_no_search]] + " ] by " + name2cid_list[replace] + ";\n")
            #if both dont have suffix (sub A by B)
            else:
                individual_output.append("    sub "+ name2cid_list[search] + " by " + name2cid_list[replace] + ";\n")

    #write to file
    output_file.write("lookup "+output_name_prefix+"_one_to_many {\n")
    output_file.writelines(grouped_output)
    output_file.write("} "+output_name_prefix+"_one_to_many ;\n\n")

    output_file.write("lookup "+output_name_prefix+"_one_to_one {\n")
    output_file.writelines(individual_output)
    output_file.write("} "+output_name_prefix+"_one_to_one ;\n\n")

    output_file.write("lookup "+output_name_prefix+"_"+keys[1]+"only {\n")
    output_file.writelines(differentiated_output_1)
    output_file.write("} "+output_name_prefix+"_"+keys[1]+"only ;\n\n")

    output_file.write("lookup "+output_name_prefix+"_"+keys[2]+"only {\n")
    output_file.writelines(differentiated_output_2)
    output_file.write("} "+output_name_prefix+"_"+keys[2]+"only ;\n\n")