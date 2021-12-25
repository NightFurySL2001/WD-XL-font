::Please prepare all the files before according to build_commands: copy full cmap and copy csv-simp-to-trad
::Run merge_font.py before
py merge_ttx.py
ttx HuaYou-src.ttx
py split_simp_trad_cid.py
py fea_convert_name2cid.py
py UVS_parser.py
tx -t1 .\HuaYou-src.ttf font.pfa
echo "Start building SC ver"
mergeFonts -cid .\cidfontinfo-SC cidfont-SC.ps .\map_HuaYou.txt font.pfa
makeotf -f cidfont-SC.ps -omitMacNames -mf .\FontMenuNameDB -ff .\feature_SC.fea -cs 25 -r -ch .\cmap_SC.txt -ci UVS_sequence_CID
sfntedit -d DSIG .\WD-XLLubrifontSC-Regular.otf
echo "Start building TC ver"
mergeFonts -cid .\cidfontinfo-TC cidfont-TC.ps .\map_HuaYou.txt font.pfa
makeotf -f cidfont-TC.ps -omitMacNames -mf .\FontMenuNameDB -ff .\feature_TC.fea -cs 2 -r -ch .\cmap_TC.txt -ci UVS_sequence_CID
sfntedit -d DSIG .\WD-XLLubrifontTC-Regular.otf
:: backtick escape space for CFF  only works in PowerShell
::echo "Building TTC"
::otf2otc -t CFF` =0 -o WD-XLLubrifont.ttc .\WD-XLLubrifontSC-Regular.otf .\WD-XLLubrifontTC-Regular.otf
echo "Start check"
fontbakery check-universal --html check-SC.html WD-XLLubrifontSC-Regular.otf
fontbakery check-universal --html check-TC.html WD-XLLubrifontTC-Regular.otf
::fontbakery check-universal --html check-TTC.html WD-XLLubrifont.ttc