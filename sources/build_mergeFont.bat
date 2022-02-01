@echo off
SETLOCAL
::set y if want to rebuild with program and shutdown when done
set "rebuild="
set "done_shutdown="
:: set r for release mode
set "release=r"

if "%release%" == "r" (
    set "release_tag=-r"
    echo Release mode set
) else (
    set "release_tag="
)

if "%rebuild%" == "y" (
    echo Start building
    ::start build program
    py merge_font_use_mergeFonts.py
)
:: feature file
py split_simp_trad_cid.py
py fea_convert_name2cid.py
py UVS_parser.py
::extract font
tx -t1 .\WD-XLLubrifont-Regular.ttf tempfont_SC.pfa
tx -t1 .\WD-XLLubrifont-Trad.ttf tempfont_TC.pfa
tx -t1 .\WD-XLLubrifont-JP83.ttf tempfont_JP83.pfa
tx -t1 .\WD-XLLubrifont-JP90.ttf tempfont_JP90.pfa
tx -t1 .\WD-XLLubrifont-JP04.ttf tempfont_JP04.pfa
::merge
mergeFonts font.pfa map_SC.txt tempfont_SC.pfa map_TC.txt tempfont_TC.pfa map_JP83.txt tempfont_JP83.pfa map_JP90.txt tempfont_JP90.pfa map_JP04.txt tempfont_JP04.pfa
::prepare build
mergeFonts -cid .\cidfontinfo-SC cidfont-SC.ps .\map_HuaYou.txt font.pfa
mergeFonts -cid .\cidfontinfo-TC cidfont-TC.ps .\map_HuaYou.txt font.pfa
mergeFonts -cid .\cidfontinfo-JPS cidfont-JPS.ps .\map_HuaYou.txt font.pfa
mergeFonts -cid .\cidfontinfo-JPN cidfont-JPN.ps .\map_HuaYou.txt font.pfa
::build
echo ### Start building SC ver ###
mergeFonts -cid .\cidfontinfo-SC cidfont-SC.ps .\map_HuaYou.txt font.pfa
makeotf -f cidfont-SC.ps -omitMacNames -mf .\FontMenuNameDB -ff .\feature_SC.fea -cs 25 %release_tag% -ch .\cmap_SC.txt -ci UVS_sequence_CID
sfntedit -d DSIG .\WD-XLLubrifontSC-Regular.otf
echo ### Start building TC ver ###
mergeFonts -cid .\cidfontinfo-TC cidfont-TC.ps .\map_HuaYou.txt font.pfa
makeotf -f cidfont-TC.ps -omitMacNames -mf .\FontMenuNameDB -ff .\feature_TC.fea -cs 2 %release_tag% -ch .\cmap_TC.txt -ci UVS_sequence_CID
sfntedit -d DSIG .\WD-XLLubrifontTC-Regular.otf
echo ### Start building JPS ver ###
mergeFonts -cid .\cidfontinfo-JPS cidfont-JPS.ps .\map_HuaYou.txt font.pfa
makeotf -f cidfont-JPS.ps -omitMacNames -mf .\FontMenuNameDB -ff .\feature_JPS.fea -cs 1 %release_tag% -ch .\cmap_JP90.txt -ci UVS_sequence_CID
sfntedit -d DSIG .\WD-XLLubrifontJPS-Regular.otf
echo ### Start building JPN ver ###
mergeFonts -cid .\cidfontinfo-JPN cidfont-JPS.ps .\map_HuaYou.txt font.pfa
makeotf -f cidfont-JPN.ps -omitMacNames -mf .\FontMenuNameDB -ff .\feature_JPN.fea -cs 1 %release_tag% -ch .\cmap_JP04.txt -ci UVS_sequence_CID
sfntedit -d DSIG .\WD-XLLubrifontJPN-Regular.otf
:: backtick escape space for CFF  only works in PowerShell
::echo "Building TTC"
::otf2otc -t CFF` =0 -o WD-XLLubrifont.ttc .\WD-XLLubrifontSC-Regular.otf .\WD-XLLubrifontTC-Regular.otf .\WD-XLLubrifontJPS-Regular.otf .\WD-XLLubrifontJPN-Regular.otf
::echo "Start check"
::fontbakery check-universal --html check-SC.html WD-XLLubrifontSC-Regular.otf
::fontbakery check-universal --html check-TC.html WD-XLLubrifontTC-Regular.otf
::fontbakery check-universal --html check-TTC.html WD-XLLubrifont.ttc

if "%done_shutdown%" == "y" (
    ::when done
    shutdown /h
)
