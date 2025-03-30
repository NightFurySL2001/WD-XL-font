@echo off
SETLOCAL

set "startdir=..\fonts"

:: make folders
IF EXIST "%startdir%" rmdir /S /Q "%startdir%"

mkdir "%startdir%"
mkdir "%startdir%\OTF"
mkdir "%startdir%\TTF"

:: script params
set "rebuild="
set "done_shutdown="
set "release="
set "collection="

:: parameters, usage: build_mergeFont.bat -b -s -c -r
for %%i in (%*) do (
    if "%%i"=="-b" set "rebuild=y"
    if "%%i"=="-s" set "done_shutdown=y"
    if "%%i"=="-c" set "collection=y"
    if "%%i"=="-r" set "release=r"
)

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
tx -t1 WD-XLLubrifont-Regular.ttf tempfont_SC.pfa
tx -t1 WD-XLLubrifont-Trad.ttf tempfont_TC.pfa
tx -t1 WD-XLLubrifont-JP83.ttf tempfont_JP83.pfa
tx -t1 WD-XLLubrifont-JP90.ttf tempfont_JP90.pfa
tx -t1 WD-XLLubrifont-JP04.ttf tempfont_JP04.pfa
::merge
mergeFonts font.pfa map_SC.txt tempfont_SC.pfa map_TC.txt tempfont_TC.pfa map_JP83.txt tempfont_JP83.pfa map_JP90.txt tempfont_JP90.pfa map_JP04.txt tempfont_JP04.pfa
::prepare build
mergeFonts -cid cidfontinfo-SC cidfont-SC.ps map_HuaYou.txt font.pfa
mergeFonts -cid cidfontinfo-TC cidfont-TC.ps map_HuaYou.txt font.pfa
mergeFonts -cid cidfontinfo-JPS cidfont-JPS.ps map_HuaYou.txt font.pfa
mergeFonts -cid cidfontinfo-JPN cidfont-JPN.ps map_HuaYou.txt font.pfa
::build
echo ### Start building SC ver ###
mergeFonts -cid cidfontinfo-SC cidfont-SC.ps map_HuaYou.txt font.pfa
makeotf -f cidfont-SC.ps -omitMacNames -mf FontMenuNameDB -ff feature_SC.fea -cs 25 -ch cmap_SC.txt -ci UVS_sequence_CID -osv 5 -osbOn 6 -o "%startdir%\OTF" %release_tag%
echo ### Start building TC ver ###
mergeFonts -cid cidfontinfo-TC cidfont-TC.ps map_HuaYou.txt font.pfa
makeotf -f cidfont-TC.ps -omitMacNames -mf FontMenuNameDB -ff feature_TC.fea -cs 2 -ch cmap_TC.txt -ci UVS_sequence_CID -osv 5 -osbOn 6 -o "%startdir%\OTF" %release_tag%
echo ### Start building JPS ver ###
mergeFonts -cid cidfontinfo-JPS cidfont-JPS.ps map_HuaYou.txt font.pfa
makeotf -f cidfont-JPS.ps -omitMacNames -mf FontMenuNameDB -ff feature_JPS.fea -cs 1 -ch cmap_JP90.txt -ci UVS_sequence_CID -osv 5 -osbOn 6 -o "%startdir%\OTF" %release_tag%
echo ### Start building JPN ver ###
mergeFonts -cid cidfontinfo-JPN cidfont-JPS.ps map_HuaYou.txt font.pfa
makeotf -f cidfont-JPN.ps -omitMacNames -mf FontMenuNameDB -ff feature_JPN.fea -cs 1 -ch cmap_JP04.txt -ci UVS_sequence_CID -osv 5 -osbOn 6 -o "%startdir%\OTF" %release_tag%

:: backtick escape space for CFF  only works in PowerShell
if "%collection%" == "y" (
echo "Building TTC"
otf2otc -t "CFF "=0 -o "%startdir%\WD-XLLubrifont.ttc" "%startdir%\OTF\WD-XLLubrifontSC-Regular.otf" "%startdir%\OTF\WD-XLLubrifontTC-Regular.otf" "%startdir%\OTF\WD-XLLubrifontJPS-Regular.otf" "%startdir%\OTF\WD-XLLubrifontJPN-Regular.otf"
)

::echo "Start check"
::fontbakery check-universal --html check-SC.html WD-XLLubrifontSC-Regular.otf
::fontbakery check-universal --html check-TC.html WD-XLLubrifontTC-Regular.otf
::fontbakery check-universal --html check-TTC.html WD-XLLubrifont.ttc

for %%f in (
WD-XLLubrifontSC-Regular.otf
WD-XLLubrifontTC-Regular.otf
WD-XLLubrifontJPS-Regular.otf
WD-XLLubrifontJPN-Regular.otf
) do (
    echo Processing file: "%startdir%\OTF\%%f"
    sfntedit -d DSIG "%startdir%\OTF\%%f"
    python add_design_language.py "%startdir%\OTF\%%f"
    otf2ttf -o "%startdir%\TTF\%%~nf.ttf" "%startdir%\OTF\%%f"
    python googlefonts_metrics.py "%startdir%\TTF\%%~nf.ttf"
    gftools fix-nonhinting "%startdir%\TTF\%%~nf.ttf" "%startdir%\TTF\%%~nf.ttf" --no-backup
)

if "%done_shutdown%" == "y" (
    ::when done
    shutdown /h
)
