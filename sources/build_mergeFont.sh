#!/bin/bash
############################################################
# Help                                                     #
############################################################
Help()
{
  # Display Help
  echo "Build WD-XL Lubrifont."
  echo
  echo "Syntax: build_mergeFont.sh [-h|b|c|s|r]"
  echo "options:"
  echo "-h     Print this Help."
  echo "-b     Re-merge source files from scratch."
  echo "-c     Build TTC collection."
  echo "-s     Shutdown when done."
  echo "-r     Release mode."
  echo
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################
set -e

startdir=../fonts

# Make folders
if [ -d "$startdir" ]; then
    rm -rf "$startdir"
fi

mkdir -p "$startdir"
mkdir -p "$startdir/OTF"
mkdir -p "$startdir/TTF"

# Script parameters
rebuild=""
done_shutdown=""
release=""
collection=""

# Parse parameters, usage: build_mergeFont.sh -b -s -r -c
while getopts ":h" option; do
   case $option in
      h) # display Help
        Help
        exit;;
      b) # Rebuild
        rebuild="y" ;;
      c) # Collection
        collection="y" ;;
      s) # Shutdown
        done_shutdown="y" ;;
      r) # Release
        release="r" ;;
     \?) # Invalid option
        echo "Error: Invalid option"
        exit;;
   esac
done

if [ "$release" == "r" ]; then
    release_tag="-r"
    echo "Release mode set"
else
    release_tag=""
fi

if [ "$rebuild" == "y" ]; then
    echo "Start building"
    # Start build program
    python3 merge_font_use_mergeFonts.py
fi

# Feature file
python3 split_simp_trad_cid.py
python3 fea_convert_name2cid.py
python3 UVS_parser.py

# Extract font
tx -t1 WD-XLLubrifont-Regular.ttf tempfont_SC.pfa
tx -t1 WD-XLLubrifont-Trad.ttf tempfont_TC.pfa
tx -t1 WD-XLLubrifont-JP83.ttf tempfont_JP83.pfa
tx -t1 WD-XLLubrifont-JP90.ttf tempfont_JP90.pfa
tx -t1 WD-XLLubrifont-JP04.ttf tempfont_JP04.pfa

# Merge
mergeFonts font.pfa map_SC.txt tempfont_SC.pfa map_TC.txt tempfont_TC.pfa map_JP83.txt tempfont_JP83.pfa map_JP90.txt tempfont_JP90.pfa map_JP04.txt tempfont_JP04.pfa

# Prepare build
mergeFonts -cid cidfontinfo-SC cidfont-SC.ps map_HuaYou.txt font.pfa
mergeFonts -cid cidfontinfo-TC cidfont-TC.ps map_HuaYou.txt font.pfa
mergeFonts -cid cidfontinfo-JPS cidfont-JPS.ps map_HuaYou.txt font.pfa
mergeFonts -cid cidfontinfo-JPN cidfont-JPN.ps map_HuaYou.txt font.pfa

# Build
echo "### Start building SC ver ###"
mergeFonts -cid cidfontinfo-SC cidfont-SC.ps map_HuaYou.txt font.pfa
makeotf -f cidfont-SC.ps -omitMacNames -mf FontMenuNameDB -ff feature_SC.fea -cs 25 -ch cmap_SC.txt -ci UVS_sequence_CID -osv 5 -osbOn 6 -o "$startdir/OTF" $release_tag

echo "### Start building TC ver ###"
mergeFonts -cid cidfontinfo-TC cidfont-TC.ps map_HuaYou.txt font.pfa
makeotf -f cidfont-TC.ps -omitMacNames -mf FontMenuNameDB -ff feature_TC.fea -cs 2 -ch cmap_TC.txt -ci UVS_sequence_CID -osv 5 -osbOn 6 -o "$startdir/OTF" $release_tag

echo "### Start building JPS ver ###"
mergeFonts -cid cidfontinfo-JPS cidfont-JPS.ps map_HuaYou.txt font.pfa
makeotf -f cidfont-JPS.ps -omitMacNames -mf FontMenuNameDB -ff feature_JPS.fea -cs 1 -ch cmap_JP90.txt -ci UVS_sequence_CID -osv 5 -osbOn 6 -o "$startdir/OTF" $release_tag

echo "### Start building JPN ver ###"
mergeFonts -cid cidfontinfo-JPN cidfont-JPN.ps map_HuaYou.txt font.pfa
makeotf -f cidfont-JPN.ps -omitMacNames -mf FontMenuNameDB -ff feature_JPN.fea -cs 1 -ch cmap_JP04.txt -ci UVS_sequence_CID -osv 5 -osbOn 6 -o "$startdir/OTF" $release_tag


if [ "$collection" == "y" ]; then
    echo "Building TTC"
    otf2otc -t "CFF=0" -o $startdir/WD-XLLubrifont.ttc $startdir/OTF/WD-XLLubrifontSC-Regular.otf $startdir/OTF/WD-XLLubrifontTC-Regular.otf $startdir/OTF/WD-XLLubrifontJPS-Regular.otf $startdir/OTF/WD-XLLubrifontJPN-Regular.otf
fi

# Process files
for f in WD-XLLubrifontSC-Regular.otf WD-XLLubrifontTC-Regular.otf WD-XLLubrifontJPS-Regular.otf WD-XLLubrifontJPN-Regular.otf; do
    echo "Processing file: $f"
    sfntedit -d DSIG "$f"
    python add_design_language.py "$f"
    otf2ttf -o "$startdir/TTF/${f%.otf}.ttf" "$f"
    python googlefonts_metrics.py "$startdir/TTF/${f%.otf}.ttf"
    gftools fix-nonhinting "$startdir/TTF/${f%.otf}.ttf" "$startdir/TTF/${f%.otf}.ttf" --no-backup
done

if [ "$done_shutdown" == "y" ]; then
    # When done
    sudo shutdown -h now
fi