**WD-XL 滑油字 | WD-XL Lubrifont**

# OpenType 功能 features

WD-XL 滑油字已经设置部分 OpenType 功能：  
WD-XL Lubrifont has set up multiple OpenType features as follow:  
WD-XL 滑油字已經設置部分 OpenType 功能：

## `vert` / `vrt2` — Vertical Alternates

本字体为直式排版设计和设置了标点转换功能，其中包括：  
This font has designed and set up vertical typesetting punctuations including:  
本字型爲直式排版設計和設置了標點轉換功能，其中包括：

SC/TC 共享：`–—―‥…〈〉《》「」『』【】〓〔〕〖〗（）－＝［］｛｝～`  
仅 SC 版：`、。‘’“”！，：；？ㄧ`

## `ccmp` — Glyph Composition/Decomposition

本字体为 [汉语拼音](https://zh.wikipedia.org/zh-cn/%E6%B1%89%E8%AF%AD%E6%8B%BC%E9%9F%B3)、[台罗拼音](https://zh.wikipedia.org/zh-cn/%E8%87%BA%E7%81%A3%E9%96%A9%E5%8D%97%E8%AA%9E%E7%BE%85%E9%A6%AC%E5%AD%97%E6%8B%BC%E9%9F%B3%E6%96%B9%E6%A1%88) 及 [白话字](https://zh.wikipedia.org/zh-cn/%E7%99%BD%E8%A9%B1%E5%AD%97) 设计了对应的拼音符号，其中台罗拼音及白话字因为部分字符并未收录于 Unicode，因此需要 `ccmp` 组字功能为对应的符号进行设置。部分汉语拼音与台罗拼音及白话字共享码位，因此 `ccmp` 功能也涵盖了汉语拼音的组字功能（例如 Ề，Ǚ 和 Ẑ）。  
This font has designed characters needed for [Hanyu Pinyin](https://en.wikipedia.org/wiki/Pinyin), [Taiwan Minnanyu Luomazi Pinyin Fang'an (or Tâi-lô)](https://en.wikipedia.org/wiki/T%C3%A2i-u%C3%A2n_L%C3%B4-m%C3%A1-j%C4%AB_Phing-im_Hong-%C3%A0n) and [Pe̍h-ōe-jī](https://en.wikipedia.org/wiki/Pe%CC%8Dh-%C5%8De-j%C4%AB). As Tâi-lô and Pe̍h-ōe-jī uses some characters that are not included in Unicode, glyph composition/decomposition `ccmp` is used to composite the characters. Hanyu Pinyin has some overlapping characters with Tâi-lô and Pe̍h-ōe-jī, thus `ccmp` feature will also cover Hanyu Pinyin characters (e.g. Ề, Ǚ, Ẑ).  
本字型为 [臺羅拼音](https://zh.wikipedia.org/zh-tw/%E8%87%BA%E7%81%A3%E9%96%A9%E5%8D%97%E8%AA%9E%E7%BE%85%E9%A6%AC%E5%AD%97%E6%8B%BC%E9%9F%B3%E6%96%B9%E6%A1%88)、[白話字](https://zh.wikipedia.org/zh-tw/%E7%99%BD%E8%A9%B1%E5%AD%97) 及 [漢語拼音](https://zh.wikipedia.org/zh-tw/%E6%B1%89%E8%AF%AD%E6%8B%BC%E9%9F%B3) 設計了對應的拼音符號，其中臺羅拼音及白話字因爲部分字符並未收錄於 Unicode，因此需要 `ccmp` 組字功能爲對應的符號進行設置。部分漢語拼音與臺羅拼音及白話字共享碼位，因此 `ccmp` 功能也涵蓋了漢語拼音的組字功能（例如 Ề，Ǚ 和 Ẑ）。

本功能将会自动开启，用户无需进行设置。  
This feature is turned on automatically, users do not need to set up the setting.  
本功能將會自動開啓，用戶無需進行設置。

## `ss01` — Stylistic Set 01 (Alternate X)

为了匹配其他字符的设计，因此本龙为该字体设计了另外一款 `X` 的字形 (glyph)。  
To match with the design of other characters, another glyph is designed for `X`.  
爲了匹配其他字符的設計，因此本龍爲該字型設計了另外一款 `X` 的字形 (glyph)。

![Sample of ss01](ss01.png)

请用户在软件内查找 `样式集` (Stylistic set) 并选择 `ss01`。  
Users are required to find “Stylistic set” and turn on `ss01`.  
請用戶在軟體內查找 `文體集` (Stylistic set) 並選擇 `ss01`。

## `ss18` — Stylistic Set 18 (Western Punctuations)

为了适配西文排版，本字体预留了 `ss18` 以储存西文式标点符号。此功能提供以下字符的西文比例宽度款式：  
The font has reserved `ss18` for Western punctutions. This feature provides Western proportional characters style for characters as below:  
爲了適配西文排版，本字型預留了 `ss18` 以存儲西文式標點符號。此功能提供以下字符的西文比例寬度款式：

* … `U+2026 HORIZONTAL ELLIPSIS` (at bottom) 西文省略号（靠下）
* · `U+002D MIDDLE DOT` (or interpunct, proportional width) 间隔号（比例宽度）
* ‘ `U+2018 LEFT SINGLE QUOTATION MARK` (proportional width) 左蝌蚪单引号（比例宽度）
* ’ `U+2019 RIGHT SINGLE QUOTATION MARK` (proportional width) 右蝌蚪单引号（比例宽度） 
* “ `U+201C LEFT DOUBLE QUOTATION MARK` (proportional width) 左蝌蚪双引号（比例宽度）
* ” `U+201D RIGHT DOUBLE QUOTATION MARK` (proportional width) 右蝌蚪双引号（比例宽度）


## `ss19` — Stylistic Set 19 (Cornered/SC Punctuation)

2.000 版起，WD-XL 滑油字正式将 SC 和 TC 版本整合于同一个 `.ttc` 字体文件中，并且可以共用其中的字形，本字体预留了 `ss19` 以储存中国简体中文使用的置左下式标点符号。此功能目前将调整以下符号：  
Starting from version 2.000, WD-XL Lubrifont merges SC and TC version into one `.ttc` font file, and some glyphs can be shared between these font. The font has reserved `ss19` for China Simplified Chinese cornered bottom left style punctuation. This feature will change the following punctuations:  
2.000 版起，WD-XL 滑油字正式將 SC 和 TC 版本整合於同一個 `.ttc` 字型文件中，並且可以共用其中的字形，本字型預留了 `ss19` 以儲存中國簡體中文使用的置左下式標點符號。此功能目前將調整以下符號：

* 、 `U+3001 IDEOGRAPHIC COMMA` 顿号
* 。 `U+3002 IDEOGRAPHIC FULL STOP` 句号
* ！ `U+FF01 FULLWIDTH EXCLAMATION MARK` 叹号
* ， `U+FF0C FULLWIDTH COMMA` 逗号
* ： `U+FF1A FULLWIDTH COLON` 冒号
* ； `U+FF1B FULLWIDTH SEMICOLON` 分号
* ？ `U+FF1F FULLWIDTH QUESTION MARK` 问号
* … `U+2026 HORIZONTAL ELLIPSIS` (centered) 中文省略号（置中）
* ‘ `U+2018 LEFT SINGLE QUOTATION MARK` (fullwidth) 左蝌蚪单引号（汉字宽度）
* ’ `U+2019 RIGHT SINGLE QUOTATION MARK` (fullwidth) 右蝌蚪单引号（汉字宽度） 
* “ `U+201C LEFT DOUBLE QUOTATION MARK` (fullwidth) 左蝌蚪双引号（汉字宽度）
* ” `U+201D RIGHT DOUBLE QUOTATION MARK` (fullwidth) 右蝌蚪双引号（汉字宽度）

> ． `U+FF0E FULLWIDTH FULL STOP` 全宽西文句号因为排版原因不提供置中版本，因此没有切换需求。  
> ． `U+FF0E FULLWIDTH FULL STOP` 全寬西文句號因爲排版原因不提供置中版本，因此沒有切換需求。

另外，以下字符是中国与台湾区分使用的部分标点，分别收录在 SC 版和 TC 版中，因此本功能也会切换以下符号：  
另外，以下字符是中國與臺灣區分使用的部分標點，分別收錄在 SC 版和 TC 版中，因此本功能也會切換以下符號：

* ˉ `U+02C9 MODIFIER LETTER MACRON` 注音一声
* ˊ `U+02CA MODIFIER LETTER ACUTE ACCENT` 注音二声
* ˇ `U+02C7 CARON` 注音三声
* ˋ `U+02CB MODIFIER LETTER GRAVE ACCENT` 注音四声
* ˙ `U+02D9 DOT ABOVE` 注音轻声


## `ss20` — Stylistic Set 20 (Centered/TC Punctuation)

本字体预留了 `ss20` 以储存台湾繁体中文使用的置中式标点符号。此功能目前将调整以下符号：  
The font has reserved `ss20` for Taiwan Traditional Chinese centered style punctuation. This feature will change the following punctuations:  
本字型預留了 `ss20` 以儲存臺灣正體（繁體）中文使用的置中式標點符號。此功能目前將調整以下符號：

* 、 `U+3001 IDEOGRAPHIC COMMA` 顿号
* 。 `U+3002 IDEOGRAPHIC FULL STOP` 句号
* ！ `U+FF01 FULLWIDTH EXCLAMATION MARK` 叹号
* ， `U+FF0C FULLWIDTH COMMA` 逗号
* ： `U+FF1A FULLWIDTH COLON` 冒号
* ； `U+FF1B FULLWIDTH SEMICOLON` 分号
* ？ `U+FF1F FULLWIDTH QUESTION MARK` 问号
* … `U+2026 HORIZONTAL ELLIPSIS` (centered) 中文省略号（置中）
* ‘ `U+2018 LEFT SINGLE QUOTATION MARK` (proportional width) 左蝌蚪单引号（比例宽度）
* ’ `U+2019 RIGHT SINGLE QUOTATION MARK` (proportional width) 右蝌蚪单引号（比例宽度） 
* “ `U+201C LEFT DOUBLE QUOTATION MARK` (proportional width) 左蝌蚪双引号（比例宽度）
* ” `U+201D RIGHT DOUBLE QUOTATION MARK` (proportional width) 右蝌蚪双引号（比例宽度）

> ． `U+FF0E FULLWIDTH FULL STOP` 全宽西文句号因为排版原因不提供置中版本，因此没有收录。  
> ． `U+FF0E FULLWIDTH FULL STOP` 全寬西文句號因爲排版原因不提供置中版本，因此沒有收錄。

另外，以下字符是中国与台湾区分使用的部分标点，分别收录在 SC 版和 TC 版中，因此本功能也会切换以下符号：  
另外，以下字符是中國與臺灣區分使用的部分標點，分別收錄在 SC 版和 TC 版中，因此本功能也會切換以下符號：

* ˉ `U+02C9 MODIFIER LETTER MACRON` 注音一声
* ˊ `U+02CA MODIFIER LETTER ACUTE ACCENT` 注音二声
* ˇ `U+02C7 CARON` 注音三声
* ˋ `U+02CB MODIFIER LETTER GRAVE ACCENT` 注音四声
* ˙ `U+02D9 DOT ABOVE` 注音轻声


## `liga` — Ligatures

本字体已经设置 ⸺ `U+2E3A TWO-EM DASH` 及 ⸻ `U+2E3B THREE-EM DASH`，但是碍于一般输入法无法输入该二字符，因此在 `liga` 连字功能里面设置以下功能：  
This font has set up both  ⸺ `U+2E3A TWO-EM DASH` and ⸻ `U+2E3B THREE-EM DASH`, but due to normal imput methods could not imput both characters, thus the following features are set up in ligatures `liga`:  
本字型已經設置 ⸺ `U+2E3A TWO-EM DASH` 及 ⸻ `U+2E3B THREE-EM DASH`，但是礙於一般輸入法無法輸入該二字符，因此在 `liga` 連字功能裏面設置以下功能：

| 字符 Character | 组合 Combination 組合 |
| --- | :-- |
| ⸺ `U+2E3A TWO-EM DASH` | U+2014 U+2014 <br> U+2015 U+2015 |
| ⸻ `U+2E3B THREE-EM DASH` | U+2014 U+2014 U+2014 <br> U+2015 U+2015 U+2015 |
| 彩蛋 Special feature | WD-XLlogo; |

请用户在软件内查找并启动 `标准连字` (Standard ligatures) 功能。  
Users are required to find turn on “Standard ligatures”.  
請用戶在軟體內查找並啓動 `標準連字` (Standard ligatures) 功能。

## `dlig` — Discretionary Ligatures

本字体也准备了汉语拼音内的多项缩写，如 `ng` - ŋ `U+014B LATIN SMALL LETTER ENG`，`zh` - ẑ `U+1E91 LATIN SMALL LETTER Z WITH CIRCUMFLEX` 等，但因为避免与其他语言相撞，因此将其设置于 `dlig` 内：  
This font also prepared the short hand form of `ng`, Ŋ `U+014A LATIN CAPITAL LETTER ENG` ang ŋ `U+014B LATIN SMALL LETTER ENG`, but to avoid collision with other languages, the features are set up in discretionary ligatures:  
本字型也準備了漢語拼音內的多項縮寫，如 `ng` - ŋ `U+014B LATIN SMALL LETTER ENG`，`zh` - ẑ `U+1E91 LATIN SMALL LETTER Z WITH CIRCUMFLEX` 等，但因爲避免與其他語言相撞，因此將其設置於 `dlig` 內：

| 字符 Character | 组合 Combination 組合 |
| --- | :-- |
| Ŋ `U+014A LATIN CAPITAL LETTER ENG` | NG |
| ŋ `U+014B LATIN SMALL LETTER ENG` | ng |
| Ẑ `U+1E90 LATIN CAPITAL LETTER Z WITH CIRCUMFLEX` | ZH/Zh |
| ẑ `U+1E91 LATIN SMALL LETTER Z WITH CIRCUMFLEX` | zh |
| Ĉ `U+0108 LATIN CAPITAL LETTER C WITH CIRCUMFLEX` | CH/Ch |
| ĉ `U+0109 LATIN SMALL LETTER C WITH CIRCUMFLEX` | ch |
| Ŝ `U+015C LATIN CAPITAL LETTER S WITH CIRCUMFLEX` | SH/Sh |
| ŝ `U+015D LATIN SMALL LETTER S WITH CIRCUMFLEX` | sh |

请用户在软件内查找并启动 `历史和任意连字` (Historical and discretionary ligatures) 功能。  
Users are required to find turn on “Historical and discretionary ligatures”.  
請用戶在軟體內查找並啓動 `歷史及選擇性連字` (Historical and discretionary ligatures) 功能。

## `smpl` / `trad` — Simplified/Traditional forms

本字体进行了几项技术测试，其中包括简繁字形替换。该功能将会提供用户选择把繁体字转为简体字（`smpl`）或者把简体字转为繁体字（`trad`）。一对多的字符将不会自动替换，用户需要手动选择替换该类字符。 **注意：该功能将会替换文档内的资讯，请妥善保存原文件后才进行测试。** [（参考来源）](https://docs.microsoft.com/en-us/typography/opentype/spec/features_pt)  
This font has included a few technical tests including Simplified/Traditional form exchanging. This feature can provide user options to convert Simplified characters to Traditional characters (`trad`) or Traditional characters to Simplified characters (`simp`). One-to-many characters will not be automatically swapped, instead users are required to manually change the characters. **Warning: the feature will modify information stored in documents, please save the original file in a safe location before testing**. [(Source)](https://docs.microsoft.com/en-us/typography/opentype/spec/features_pt)  
本字型進行了幾項技術測試，其中包括繁簡字形替換。該功能將會提供用戶選擇把簡體字轉爲繁體字 (`trad`) 或者把繁體字轉爲簡體字 (`simp`)。一對多的字符將不會自動替換，用戶需要手動選擇替換該類字符。 **注意：該功能將會替換文檔内的資訊，請妥善保存原文件后才進行測試。** [（參考來源）](https://docs.microsoft.com/en-us/typography/opentype/spec/features_pt)

目前多数软件不支援该功能，仅浏览器可以通过 CSS 设置该功能。（注：Adobe InDesign 可开启 `trad` 而已。）  
Most software do not support this feature, only browsers are able to set this feature through CSS. (Note: Adobe InDesign can turn on `trad` only.)  
目前多數軟體不支援該功能，僅瀏覽器可以通過 CSS 設置該功能。（注：Adobe InDesign 可開啓 `trad` 而已。）

## `locl` — Localized Forms

本字体在 2.000 版中加入了新功能测试，即地域切换字形。2.000 版中 SC 版及 TC 版正式合并成一个字体文件，也允许一个字体内的字符切换成另一个区域内的字符。此功能主要可用于切换简繁不同的字形，如把“骨”系列汉字的上面部件方向切换。  
This font has included new test feature in version 2.000, which is changing forms based on region. In version 2.000, SC and TC are merged into one font file and this allows the character glyphss from one region be able to change to another glyph for another region. This feature is mainly used to change glyphs that differ between SC and TC, such as the top of “骨”.  
本字型在 2.000 版中加入了新功能測試，即地域切換字形。2.000 版中 SC 版及 TC 版正式合併成一個字型文件，也允許一個字型內的字符切換成另一個區域內的字符。此功能主要可用于切換簡繁不同的字形，如把“骨”系列漢字的上面部件方向切換。

目前部分软件支援该功能，若能在软件内标记文本语言，则在部分情况下是可以使用的（如 Word 和 InDesign），且会随语言切换自动切换。浏览器内在相关的标签内加上 `lang="zh-cn"` 或 `lang="zh-tw"` 属性即可使用。  
Currently some software supports this feature, if the software is able to tag the language of the texts then it is probable that this feature is available (such as Word and InDesign), and will automatically be used when changing languages. In browsers adding the language attribute `lang="zh-cn"` or `lang="zh-tw"` to the elements will turn on this feature.  
目前部分軟體支援該功能，若能在軟體內標記文本語言，則在部分情況下是可以使用的（如 Word 和 InDesign），且會隨語言切換自動切換。瀏覽器內在相關的標簽內加上 `lang="zh-cn"` 或 `lang="zh-tw"` 屬性即可使用。

## `aalt` — Access All Alternates

以上所有功能（除了 `liga` 和 `dlig`）皆可通过 `aalt` 功能使用，因此 `smpl`/`trad` 的字符替换选择也可以在 Adobe 系列软件内测试使用。  
All the features above (except `liga`) can be access through `aalt`, thus the character choice from `smpl`/`trad` can still be accessed in Adobe suite through this function.  
以上所有功能（除了 `liga` 和 `dlig`）皆可通過 `aalt` 功能使用，因此 `smpl`/`trad` 的字符替换選擇也可以在 Adobe 系列軟體內測試使用。

## Extra: Ideographic Variation Selector 异体字选择器

本字体为中文标点符号设置了异体字选择器，可以选择调用置左下或置中的标点符号。下面表格内的符号是可以直接复制粘贴使用的。  
This font has preset Ideographic Variation Selector for Chinese punctuations that can be used to choose cornered or centered puncuation. The punctuations in the table below can be directly copy-and-paste and ready to be used.

| 字符 Character | 置左下 Cornered (`U+FE00`) | 置中 Centered (`U+FE01`) |
| :-- | --- | --- |
| 、 `U+3001 IDEOGRAPHIC COMMA` | 、︀ | 、︁ |
| 。 `U+3002 IDEOGRAPHIC FULL STOP` | 。︀ | 。︁ |
| ！ `U+FF01 FULLWIDTH EXCLAMATION MARK` | ！︀ | ！︁ |
| ， `U+FF0C FULLWIDTH COMMA` | ，︀ | ，︁ |
| ． `U+FF0E FULLWIDTH FULL STOP` | ．︀ | ．︁ |
| ： `U+FF1A FULLWIDTH COLON` | ：︀ | ：︁ |
| ； `U+FF1B FULLWIDTH SEMICOLON` | ；︀ | ；︁ |
| ？ `U+FF1F FULLWIDTH QUESTION MARK` | ？︀ | ？︁ |