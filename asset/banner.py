from rich.console import Console
from rich.text import Text
from rich.table import Table

console = Console()

alter = """
                      [#019bff]%,[/#019bff]
                    [#019bff]^WWWw[/#019bff]
                   [#019bff]'wwwwww[/#019bff]
                  [#019bff]!wwwwwwww[/#019bff]
                 [#019bff]#`wwwwwwwww[/#019bff]
                [#019bff]@wwwwwwwwwwww[/#019bff]
               [#019bff]wwwwwwwwwwwwwww[/#019bff]
              [#019bff]wwwwwwwwwwwwwwwww[/#019bff]
             [#019bff]wwwwwwwwwwwwwwwwwww[/#019bff]
            [#019bff]wwwwwwwwwwwwwwwwwwww,[/#019bff]
           [#015598]w~1i.[/#015598][#019bff]wwwwwwwwwwwwwwwww,[/#019bff]
         [#006ffe]3~:~[/#006ffe][#015598]1lli.[/#015598][#019bff]wwwwwwwwwwwwwwww.[/#019bff]
        [#006ffe]:~~:~[/#006ffe][#015598]?ttttz[/#015598][#019bff]wwwwwwwwwwwwwwww[/#019bff]
       [#006ffe]#<~:~~~~[/#006ffe][#015598]?llllltO-.[/#015598][#019bff]wwwwwwwwwww[/#019bff]
      [#006ffe]#~:~~:~:~~[/#006ffe][#015598]?ltlltlttO-.[/#015598][#019bff]wwwwwwwww[/#019bff]
     [#006ffe]@~:~~:~:~:~~[/#006ffe][#015598](zttlltltlOda.[/#015598][#019bff]wwwwwww[/#019bff]
    [#006ffe]@~:~~: ~:~~:~:[/#006ffe][#015598](zltlltlO[/#015598]    a,[#019bff]wwwwww[/#019bff]
   [#006ffe]8~~:~~:~~~~:~~~~_[/#006ffe][#015598]1ltltu[/#015598]          [#019bff],www[/#019bff]
  [#006ffe]5~~:~~:~~:~~:~~:~~~[/#006ffe][#015598]_1ltq[/#015598]             [#019bff]N,,[/#019bff]
 [#006ffe]g~:~~:~~~:~~:~~:~:~~~~[/#006ffe][#015598]1q[/#015598]                [#019bff]N,[/#019bff]
"""
altercolor = {
  0:  "#1B1D1E",
  1:  "#AF3A03",
  2:  "#5F875F",
  3:  "#DFAF5F",
  4:  "#5F5FAF",
  5:  "#AF5FAF",
  6:  "#5FAFAF",
  7:  "#D0D0D0",
  8:  "#505050",
  9:  "#FF5F00",
  10: "#AFFF5F",
  11: "#FFFF5F",
  12: "#5F87FF",
  13: "#FF5FFF",
  14: "#5FFFFF",
  15: "#FFFFFF",
}


anarchy = """
                         ++
                        ++
                      +++
                    :+++.
              .:::##++++#::.
          .:#######++++#######:.
       .##########+++++##########:.
     .###########+++++++#############.
    ############+++++++++############:
   ###########++++++#++++##############
  ############+++++###++++##############
 :############++++####++++##############:
 ###########+++++#####+++++#####+++######
.##########++++++#####++++++++++++#######.
.##########+++++++++++++++++++###########.
 #####++++++++++++++###++++++++##########
 :###++++++++++#########+++++++#########:
  #######+++++##########++++++++########
   #####+++++###########+++++++++######
    :##++++++############++++++++++##:
     .++++++#############+++++++++++.
      +++++###############+++++++::
     .++. .:###############+++++++..
     +++      ..::######::..:+++++.
     +                       .:+++.
                                +++
                                   ++
                                    ++
"""
anarchycolor = {
  0:  "#1E1E1E",
  1:  "#B22222",
  2:  "#228B22",
  3:  "#DAA520",
  4:  "#1E90FF",
  5:  "#8A2BE2",
  6:  "#20B2AA",
  7:  "#D3D3D3",
  8:  "#696969",
  9:  "#FF4500",
  10: "#7FFF00",
  11: "#FFFF00",
  12: "#00BFFF",
  13: "#FF00FF",
  14: "#00FFFF",
  15: "#FFFFFF",
}


anarchyi = Text(anarchy)

for i, char in enumerate(anarchy):
    if char == '+':
        anarchyi.stylize("red", i, i + 1)



androidbn = """
         -o          o-
          +hydNNNNdyh+
        +mMMMMMMMMMMMMm+
      `dMMm:NMMMMMMN:mMMd`
      hMMMMMMMMMMMMMMMMMMh
  ..  yyyyyyyyyyyyyyyyyyyy  ..
.mMMm`MMMMMMMMMMMMMMMMMMMM`mMMm.
:MMMM-MMMMMMMMMMMMMMMMMMMM-MMMM:
:MMMM-MMMMMMMMMMMMMMMMMMMM-MMMM:
:MMMM-MMMMMMMMMMMMMMMMMMMM-MMMM:
:MMMM-MMMMMMMMMMMMMMMMMMMM-MMMM:
-MMMM-MMMMMMMMMMMMMMMMMMMM-MMMM-
 +yy+ MMMMMMMMMMMMMMMMMMMM +yy+
      mMMMMMMMMMMMMMMMMMMm
      `/++MMMMh++hMMMM++/`
          MMMMo  oMMMM
          MMMMo  oMMMM
          oNMm-  -mMNs
"""

androidcolor = {
  0:  "#000000",
  1:  "#0F9D58",
  2:  "#34A853",
  3:  "#A4C639",
  4:  "#4285F4",
  5:  "#669DF6",
  6:  "#00BCD4",
  7:  "#E0E0E0",
  8:  "#616161",
  9:  "#EA4335",
  10: "#00C853",
  11: "#FFEB3B",
  12: "#8AB4F8",
  13: "#FF4081",
  14: "#00BCD4",
  15: "#FFFFFF",
}


android = Text(androidbn, style="#3cdb85")

archbn = """
                  -`
                 .o+`
                `ooo/
               `+oooo:
              `+oooooo:
              -+oooooo+:
            `/:-:++oooo+:
           `/++++/+++++++:
          `/++++++++++++++:
         `/+++ooooooooooooo/`
        ./ooosssso++osssssso+`
       .oossssso-````/ossssss+`
      -osssssso.      :ssssssso.
     :osssssss/        osssso+++.
    /ossssssss/        +ssssooo/-
  `/ossssso+/:-        -:/+osssso+-
 `+sso+:-`                 `.-/+oso:
`++:.                           `-/+/
.`                                 `/
"""

archcolor = {
  0:  "#1C1C1C",
  1:  "#CC0000",
  2:  "#4E9A06",
  3:  "#C4A000",
  4:  "#3465A4",
  5:  "#75507B",
  6:  "#06989A",
  7:  "#D3D7CF",
  8:  "#555753",
  9:  "#EF2929",
  10: "#8AE234",
  11: "#FCE94F",
  12: "#729FCF",
  13: "#AD7FA8",
  14: "#34E2E2",
  15: "#EEEEEC",
}


arch = Text(archbn, style="#0086ff")

archbn2 = """
                  ▄
                 ▟█▙
                ▟███▙
               ▟█████▙
              ▟███████▙
             ▂▔▀▜██████▙
            ▟██▅▂▝▜█████▙
           ▟█████████████▙
          ▟███████████████▙
         ▟█████████████████▙
        ▟███████████████████▙
       ▟█████████▛▀▀▜████████▙
      ▟████████▛      ▜███████▙
     ▟█████████        ████████▙
    ▟██████████        █████▆▅▄▃▂
   ▟██████████▛        ▜█████████▙
  ▟██████▀▀▀              ▀▀██████▙
 ▟███▀▘                       ▝▀███▙
▟▛▀                               ▀▜▙
"""

arch2 = Text(archbn2, style="#0086ff")

Aperturebn = f"""
              .,-:;//;:=,
          . :H@@@MM@M#H/.,+%;,
       ,/X+ +M@@M@MM%=,-%HMMM@X/,
     -+@MM; $M@@MH+-,;XMMMM@MMMM@+-
    ;@M@@M- XM@X;. -+XXXXXHHH@M@M#@/.
  ,%MM@@MH ,@%=             .---=-=:=,.
  =@#@@@MX.,                -%HX$$%%%:;
 =-./@M@M$                   .;@MMMM@MM:
 X@/ -$MM/                    . +MM@@@M$
,@M@H: :@:                    . =X#@@@@-
,@@@MMX, .                    /H- ;@M@M=
.H@@@@M@+,                    %MM+. %#$.
 /MMMM@MMH/.                  XM@MH; =;
  /%+%$XHH@$=              , .H@@@@MX,
   =----------.          -%H.,@@@@@MX,
   .%MM@@@HHHXX$$$%+- .:$MMX =M@@MM%.
     =XMMM@MM@MM#H;,-+HMM@M+ /MMMX=
       =%@M@M#@$-.=$@MM@@@M; %M%=
         ,:+$+-,/H#MMMMMMM@= =,
               =++%%%%+/:-.
"""

Aperturecolor = {
  0:  "#000000",
  1:  "#3A3A3A",
  2:  "#7D7D7D",
  3:  "#BFBFBF",
  4:  "#FFFFFF",
  5:  "#1C3F66",
  6:  "#3A7BD5",
  7:  "#A3C4F3",
  8:  "#BF5A1E",
  9:  "#FF7F32",
  10: "#FFA64D",
  11: "#008B8B",
  12: "#00CED1",
  13: "#66E0E0",
  14: "#8A2BE2",
  15: "#F0F0F0"
}


Aperture = Text(Aperturebn, style="#019bff")

Debian = f"""
        _,met$$$$$gg.
     ,g$$$$$$$$$$$$$$$P.
   ,g$$P""       ""Y$$.".
  ,$$P'              `$$$.
',$$P       ,ggs.     `$$b:
`d$$'     ,$P"'   .    $$$
 $$P      d$'     ,    $$P
 $$:      $$.   -    ,d$$'
 $$;      Y$b._   _,d$P'
 Y$$.    `.`"Y$$$$P"'
 `$$b      "-.__
  `Y$$b
   `Y$$.
     `$$b.
       `Y$$b.
         `"Y$b._
             `"""

debiancolor = {
  0:  "#000000",
  1:  "#A40000",
  2:  "#00A600",
  3:  "#A6A600",
  4:  "#0000A6",
  5:  "#A600A6",
  6:  "#00A6A6",
  7:  "#AAAAAA",
  8:  "#555555",
  9:  "#FF5555",
  10: "#55FF55",
  11: "#FFFF55",
  12: "#5555FF",
  13: "#FF55FF",
  14: "#55FFFF",
  15: "#FFFFFF"
}


Debianbn2 = f"""
        _,met$$$$$gg.
     ,g$$$$$$$$$$$$$$$P.
   ,g$$P""       ""Y$$.".
  ,$$P'              `$$$.
',$$P       ,ggs.     `$$b:
`d$$'     ,$P"'   .    $$$
 $$P      d$'     ,    $$P
 $$:      $$.   -    ,d$$'
 $$;      Y$b._   _,d$P'
 Y$$.    `.`"Y$$$$P"'
 `$$b      "-.__
  `Y$$b
   `Y$$.
     `$$b.
       `Y$$b.
         `"Y$b._
             `"""

Debian2 = Text(Debianbn2, style="#a80031")

Deepinbn = """
             ............
         .';;;;;.       .,;,.
      .,;;;;;;;.       ';;;;;;;.
    .;::::::::'     .,::;;,''''',.
   ,'.::::::::    .;;'.          ';
  ;'  'cccccc,   ,' :: '..        .:
 ,,    :ccccc.  ;: .c, '' :.       ,;
.l.     cllll' ., .lc  :; .l'       l.
.c       :lllc  ;cl:  .l' .ll.      :'
.l        'looc. .   ,o:  'oo'      c,
.o.         .:ool::coc'  .ooo'      o.
 ::            .....   .;dddo      ;c
  l:...            .';lddddo.     ,o
   lxxxxxdoolllodxxxxxxxxxc      :l
    ,dxxxxxxxxxxxxxxxxxxl.     'o,
      ,dkkkkkkkkkkkkko;.    .;o;
        .;okkkkkdl;.    .,cl:.
            .,:cccccccc:,.
"""

deepincolor = {
  0:  "#000000",
  1:  "#C46C6C",
  2:  "#7FC06D",
  3:  "#D0D26C",
  4:  "#6C8ED0",
  5:  "#D26CD0",
  6:  "#6CD2D2",
  7:  "#D0D0D0",
  8:  "#7F7F7F",
  9:  "#FF8C8C",
  10: "#8CFF8C",
  11: "#FFFF8C",
  12: "#8C8CFF",
  13: "#FF8CFF",
  14: "#8CFFFF",
  15: "#FFFFFF"
}

Deepin = Text(Deepinbn, style="#2ec6fe")

Devuanbn = """
   ..,,;;;::;,..
           `':ddd;:,.
                 `'dPPd:,.
                     `:b$$b`.
                        'P$$$d`
                         .$$$$$`
                         ;$$$$$P
                      .:P$$$$$$`
                  .,:b$$$$$$$;'
             .,:dP$$$$$$$$b:'
      .,:;db$$$$$$$$$$Pd'`
 ,db$$$$$$$$$$$$$$b:'`
:$$$$$$$$$$$$b:'`
 `$$$$$bd:''`
   `'''`
"""

devuancolor = {
  0:  "#1C1C1C",
  1:  "#A80000",
  2:  "#008000",
  3:  "#A85600",
  4:  "#003366",
  5:  "#800080",
  6:  "#008080",
  7:  "#C0C0C0",
  8:  "#606060",
  9:  "#FF0000",
  10: "#00FF00",
  11: "#FFB000",
  12: "#3399FF",
  13: "#FF55FF",
  14: "#00FFFF",
  15: "#FFFFFF"
}

Devuan = Text(Devuanbn)

eurolinuxbn = """
                __
         -wwwWWWWWWWWWwww-
        -WWWWWWWWWWWWWWWWWWw-
          \WWWWWWWWWWWWWWWWWWW-
  _Ww      `WWWWWWWWWWWWWWWWWWWw
 -WEWww                -WWWWWWWWW-
_WWUWWWW-                _WWWWWWWW
_WWRWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW-
wWWOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWLWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWw
WWWIWWWWWWWWWWWWWWWWWWWWWWWWWWWWww-
wWWNWWWWw
 WWUWWWWWWw
 wWXWWWWWWWWww
   wWWWWWWWWWWWWWWWw
    wWWWWWWWWWWWWWWWw
       WWWWWWWWWWWWWw
           wWWWWWWWw
"""

eurobn = Text(eurolinuxbn)

colored_chars = {"W", "w", "-", "_", "\\", "`"}

for i, char in enumerate(eurolinuxbn):
    if char in colored_chars:
        eurobn.stylize("#0a61ab", i, i + 1)

eurolinux = eurobn

eurolinuxcolor = {
  0:  "#000000",
  1:  "#003366",
  2:  "#004C99",
  3:  "#336699",
  4:  "#003366",
  5:  "#3366CC",
  6:  "#6699CC",
  7:  "#CCCCCC",
  8:  "#666666",
  9:  "#003399",
  10: "#0066CC",
  11: "#3399FF",
  12: "#FFCC00",
  13: "#FFDD33",
  14: "#FFFF66",
  15: "#FFFFFF"
}

Fedorabn = """
             .[#243e72]',;::::;,'.[/#243e72]
         .';:cccccccccccc:;,.
      .;cccccccccccccccccccccc;.
    .:cccccccccccccccccccccccccc:.
  .;ccccccccccccc;.[#243e72]:dddl:.[/#243e72];ccccccc;.
 .:ccccccccccccc;[#243e72]OWMKOOXMWd[/#243e72];ccccccc:.
.:ccccccccccccc;[#243e72]KMMc[/#243e72];cc;[#243e72]xMMc[/#243e72];ccccccc:.
,cccccccccccccc;[#243e72]MMM.[/#243e72];cc;;[#243e72]WW:[/#243e72];cccccccc,
:cccccccccccccc;[#243e72]MMM.[/#243e72];cccccccccccccccc:
:ccccccc;[#243e72]oxOOOo[/#243e72];[#243e72]MMM000k.[/#243e72];cccccccccccc:
cccccc;[#243e72]0MMKxdd[/#243e72]:;[#243e72]MMMkddc.[/#243e72];cccccccccccc;
ccccc;[#243e72]XMO'[/#243e72];cccc;[#243e72]MMM.[/#243e72];cccccccccccccccc'
ccccc;[#243e72]MMo[/#243e72];ccccc;[#243e72]MMW.[/#243e72];ccccccccccccccc;
ccccc;[#243e72]0MNc.[/#243e72]ccc.[#243e72]xMMd[/#243e72];ccccccccccccccc;
cccccc;[#243e72]dNMWXXXWM0:[/#243e72];cccccccccccccc:,
cccccccc;[#243e72].:odl:.[/#243e72];cccccccccccccc:,.
ccccccccccccccccccccccccccccc:'.
:ccccccccccccccccccccccc:;,..
 ':cccccccccccccccc::;,.
"""

Fedora = Fedorabn

fedoracolor = {
  0:  "#000000",
  1:  "#A40000",
  2:  "#00A600",
  3:  "#C4A000",
  4:  "#3465A4",
  5:  "#75507B",
  6:  "#06989A",
  7:  "#D3D7CF",
  8:  "#555753",
  9:  "#EF2929",
  10: "#8AE234",
  11: "#FCE94F",
  12: "#729FCF",
  13: "#AD7FA8",
  14: "#34E2E2",
  15: "#EEEEEC"
}

skull = """
              xSSSSSSSSSSSx:
          XSSSSSSSSSSSSSSSSSSSSX
       xSSSSSSSSSSSSSSSSSSSSSSSxSSX
     xSSSSSSSSSSSSSSSSSSSSSSSSSSSSXSS
    SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSXXXS;
  +SSSSSSx++SSSSSSSSSSSSSSSSSSSSSSSSSXSX
  SSSSS:::::::SSSSSSSSSSSSSXSSSSSSSSSS+S+
 XSSSX::::::::XxSSSSSSSSXSx;::xSSSSSSSSSS
;SSSS:::::::::XSSSSSSSSS+:::::::xSSSSSSSS;
+SSSSx::::::::SSSSSSSSS;:::::::::XSSSSSSSX
 SSSSXSx:::::SSSSxXSSSS::::::::::XSSSSSSSX
 xSSSSSSSSSSSS:::::SSSX::::::::::XSSSSSSS;
  +SSSSSSSSSSSSSSX:SSSSS;:::::::SxSSSSSSS
    +SSSSSSSSSSSSSSSSSSSSSSSSSXSSxSSSSSS
       xxSSSSSSSSSSSSSSSSSSSSSSSSSSSSSx
        SSSSSSSSSSSSSSSSSSSSSSSSSSSX
        xXSSSSSSSSSSSSX
        SSS +SSSxSSSSS
             ;x  xSSx
"""

kali = """
..............
            ..,;:ccc,.
          ......''';lxO.
.....''''..........,:ld;
           .';;;:::;,,.x,
      ..'''.            0Xxoc:,.  ...
  ....                ,ONkc;,;cokOdc',.
 .                   OMo           ':ddo.
                    dMc               :OO;
                    0M.                 .:o.
                    ;Wd
                     ;XO,
                       ,d0Odlc;,..
                           ..',;:cdOOd::,.
                                    .:d;.':;.
                                       'd,  .'
                                         ;l   ..
                                          .o
                                            c
                                            .'
                                             .
"""

kalicolor = {
  0:  "#0B0C10",
  1:  "#C30771",
  2:  "#10A778",
  3:  "#F2F2F2",
  4:  "#1F2833",
  5:  "#6F2232",
  6:  "#1D9BF0",
  7:  "#E7DFDD",
  8:  "#323C44",
  9:  "#FF4D6D",
  10: "#42F58C",
  11: "#FFE66D",
  12: "#4D5BCE",
  13: "#FF77FF",
  14: "#1DE9B6",
  15: "#FFFFFF"
}

mintbn = """
             ...-:::::-...
          .-MMMMMMMMMMMMMMM-.
      .-MMMM`..-:::::::-..`MMMM-.
    .:MMMM.:MMMMMMMMMMMMMMM:.MMMM:.
   -MMM-M---MMMMMMMMMMMMMMMMMMM.MMM-
 `:MMM:MM`  :MMMM:....::-...-MMMM:MMM:`
 :MMM:MMM`  :MM:`  ``    ``  `:MMM:MMM:
.MMM.MMMM`  :MM.  -MM.  .MM-  `MMMM.MMM.
:MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM-MMM:
:MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM:MMM:
:MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM-MMM:
.MMM.MMMM`  :MM:--:MM:--:MM:  `MMMM.MMM.
 :MMM:MMM-  `-MMMMMMMMMMMM-`  -MMM-MMM:
  :MMM:MMM:`                `:MMM:MMM:
   .MMM.MMMM:--------------:MMMM.MMM.
     '-MMMM.-MMMMMMMMMMMMMMM-.MMMM-'
       '.-MMMM``--:::::--``MMMM-.'
            '-MMMMMMMMMMMMM-'
               ``-:::::-``
"""

mintcolor = {
    0:  "#0C0C0C",
    1:  "#FF6C6B",
    2:  "#98BE65",
    3:  "#ECBE7B",
    4:  "#51AFEF",
    5:  "#C678DD",
    6:  "#46D9FF",
    7:  "#DFDFDF",
    8:  "#5B6268",
    9:  "#EC5f67",
    10: "#B9CA4A",
    11: "#EBCB8B",
    12: "#4DB5BD",
    13: "#B877DB",
    14: "#61D6D6",
    15: "#FFFFFF"
}

mint = Text(mintbn, style="#69b73c")

linuxbn = """
              ..;:::::::;.
           .0X''''''''''''''N:
         :Xd,.'''''''''''''''lKx
       .0o'.''''''''''''''''''':K;
      .O;.'okOx:''''''''',dOOx:''O;
      xc.'xXl kX;''[#f6d83e]:cc;[/#f6d83e]''kXl OX;''k.
     'x..':0X0Xx'[#f6d83e],OOOOOd,[/#f6d83e]:0X0Xx'''o:
     ::..'[#f6d83e],clollxOOOOOOOOdlddlc[/#f6d83e]''''d
     l'..[#f6d83e]':kkkkOOOOOOOOOOOOkkkx,[/#f6d83e]'''x
     o...''''',[#f6d83e]codxkkxxxdl[/#f6d83e]:''''''''d.
     d...''''''''''''''''''''''''''o.
     d..'''',loc,'''''''';os:,'''''d'
    :d..',dKXXXXX0kxxxk0XXXXXX0l''',O.
   'O..'cKXXXXXXXXXXXXXXXXXXXXXXk'''ck
  'O'.'cXXXXXXXXXXXXXXXXXXXXXXXXXO'''od
 .O,.''0XXXXXXXXXXXXXXXXXXXXXXXXXXo'''k;
 cc..''XXXXXXXXXXXXXXXXXXXXXXXXXXXk''''k
 l...',XXXXXXXXXXXXXXXXXXXXXXXXXXXO''''d.
"""
linux = linuxbn.replace("'", "[#243e72]’[/#243e72]")

linuxcolor = {
  0:  "#000000",
  1:  "#CC0000",
  2:  "#4E9A06",
  3:  "#C4A000",
  4:  "#3465A4",
  5:  "#75507B",
  6:  "#06989A",
  7:  "#D3D7CF",
  8:  "#555753",
  9:  "#EF2929",
  10: "#8AE234",
  11: "#FCE94F",
  12: "#729FCF",
  13: "#AD7FA8",
  14: "#34E2E2",
  15: "#EEEEEC"
}

macos = """
                     ..'
                 ,xNMM.
               .OMMMMo
               lMM"
     .;loddo:.  .olloddol;.
   cKMMMMMMMMMMNWMMMMMMMMMM0:
 .KMMMMMMMMMMMMMMMMMMMMMMMWd.
 XMMMMMMMMMMMMMMMMMMMMMMMX.
;MMMMMMMMMMMMMMMMMMMMMMMM:
:MMMMMMMMMMMMMMMMMMMMMMMM:
.MMMMMMMMMMMMMMMMMMMMMMMMX.
 kMMMMMMMMMMMMMMMMMMMMMMMMWd.
 'XMMMMMMMMMMMMMMMMMMMMMMMMMMk
  'XMMMMMMMMMMMMMMMMMMMMMMMMK.
    kMMMMMMMMMMMMMMMMMMMMMMd
     ;KMMMMMMMWXXWMMMMMMMk.
       "cooc*"    "*coo'"
"""
macoscolor = {
  0:  "#1C1C1C",
  1:  "#FF3B30",
  2:  "#34C759",
  3:  "#FFD60A",
  4:  "#007AFF",
  5:  "#AF52DE",
  6:  "#5AC8FA",
  7:  "#F2F2F7",
  8:  "#8E8E93",
  9:  "#FF375F",
  10: "#32D74B",
  11: "#FFD60A",
  12: "#0A84FF",
  13: "#BF5AF2",
  14: "#64D2FF",
  15: "#FFFFFF"
}

manjarobn = """
██████████████████  ████████
██████████████████  ████████
██████████████████  ████████
██████████████████  ████████
████████            ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
"""

manjaro = Text(manjarobn, style="#33c05d")

manjarocolor = {
  0:  "#0C0C0C",
  1:  "#E95454",
  2:  "#8AE234",
  3:  "#FCE94F",
  4:  "#729FCF",
  5:  "#AD7FA8",
  6:  "#34E2E2",
  7:  "#EEEEEC",
  8:  "#555753",
  9:  "#FF5555",
  10: "#55FF55",
  11: "#FFFF55",
  12: "#5555FF",
  13: "#FF55FF",
  14: "#55FFFF",
  15: "#FFFFFF"
}

netbsd = """
                     [#f26613]`-/oshdmNMNdhyo+:-`[/#f26613]
y[#f26613]/s+:-``    `.-:+oydNMMMMNhs/-``[/#f26613]
-m+[#f26613]NMMMMMMMMMMMMMMMMMMMNdhmNMMMmdhs+/-`[/#f26613]
 -m+[#f26613]NMMMMMMMMMMMMMMMMMMMMmy+:`[/#f26613]
  -N/[#f26613]dMMMMMMMMMMMMMMMds:`[/#f26613]
   -N/[#f26613]hMMMMMMMMMmho:`[/#f26613]
    -N/[#f26613]-:/++/:.`[/#f26613]
     :M+
      :Mo
       :Ms
        :Ms
         :Ms
          :Ms
           :Ms
            :Ms
             :Ms
              :Ms
"""

netbsdcolor = {
  0:  "#000000",
  1:  "#C31B00",
  2:  "#007F4F",
  3:  "#C77F00",
  4:  "#0047AB",
  5:  "#7F3FBF",
  6:  "#00BFAF",
  7:  "#D0D0D0",
  8:  "#505050",
  9:  "#FF4F3F",
  10: "#00FF9F",
  11: "#FFD27F",
  12: "#5F9FFF",
  13: "#BF7FFF",
  14: "#3FFFD2",
  15: "#FFFFFF"
}


raspberry = """
   [#47ae4a]`.::///+:/-.        --///+//-:`[/#47ae4a]
 [#47ae4a]`+oooooooooooo:   `+oooooooooooo:[/#47ae4a]
  [#47ae4a]/oooo++//ooooo:  ooooo+//+ooooo.[/#47ae4a]
  [#47ae4a]`+ooooooo:-:oo-  +o+::/ooooooo:[/#47ae4a]
   [#47ae4a]`:oooooooo+``    `.oooooooo+-[/#47ae4a]
     [#47ae4a]`:++ooo/.        :+ooo+/.`[/#47ae4a]
        [#ce1d57]...`  `.----.` ``..[/#ce1d57]
     [#ce1d57].::::-``:::::::::.`-:::-`[/#ce1d57]
    [#ce1d57]-:::-`   .:::::::-`  `-:::-[/#ce1d57]
   [#ce1d57]`::.  `.--.`  `` `.---.``.::`[/#ce1d57]
       [#ce1d57].::::::::`  -::::::::` `[/#ce1d57]
 [#ce1d57].::` .:::::::::- `::::::::::``::.[/#ce1d57]
[#ce1d57]-:::` ::::::::::.  ::::::::::.`:::-[/#ce1d57]
[#ce1d57]::::  -::::::::.   `-::::::::  ::::[/#ce1d57]
[#ce1d57]-::-   .-:::-.``....``.-::-.   -::-[/#ce1d57]
 [#ce1d57].. ``       .::::::::.     `..`..[/#ce1d57]
   [#ce1d57]-:::-`   -::::::::::`  .:::::`[/#ce1d57]
   [#ce1d57]:::::::` -::::::::::` :::::::.[/#ce1d57]
   [#ce1d57].:::::::  -::::::::. ::::::::[/#ce1d57]
    [#ce1d57]`-:::::`   ..--.`   ::::::.[/#ce1d57]
      [#ce1d57]`...`  `...--..`  `...`[/#ce1d57]
            [#ce1d57].::::::::::[/#ce1d57]
             [#ce1d57]`.-::::-`[/#ce1d57]
"""

raspberrycolor = {
  0:  "#2C001E",
  1:  "#D32F2F",
  2:  "#388E3C",
  3:  "#FBC02D",
  4:  "#1976D2",
  5:  "#7B1FA2",
  6:  "#0097A7",
  7:  "#E0E0E0",
  8:  "#424242",
  9:  "#FF5252",
  10: "#69F0AE",
  11: "#FFF176",
  12: "#64B5F6",
  13: "#EA80FC",
  14: "#1DE9B6",
  15: "#FFFFFF"
}

redhatbn = """
           .MMM..:MMMMMMM
          MMMMMMMMMMMMMMMMMM
          MMMMMMMMMMMMMMMMMMMM.
         MMMMMMMMMMMMMMMMMMMMMM
        ,MMMMMMMMMMMMMMMMMMMMMM:
        MMMMMMMMMMMMMMMMMMMMMMMM
  .MMMM'  MMMMMMMMMMMMMMMMMMMMMM
 MMMMMM    `MMMMMMMMMMMMMMMMMMMM.
MMMMMMMM      MMMMMMMMMMMMMMMMMM .
MMMMMMMMM.       `MMMMMMMMMMMMM' MM.
MMMMMMMMMMM.                     MMMM
`MMMMMMMMMMMMM.                 ,MMMMM.
 `MMMMMMMMMMMMMMMMM.          ,MMMMMMMM.
    MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
      MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM:
         MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
            `MMMMMMMMMMMMMMMMMMMMMMMM:
                ``MMMMMMMMMMMMMMMMM'
"""

redhat = Text(redhatbn, style="#ee0001")

redhatcolor = {
  0:  "#000000",
  1:  "#CC0000",
  2:  "#00CC00",
  3:  "#CCCC00",
  4:  "#0000CC",
  5:  "#CC00CC",
  6:  "#00CCCC",
  7:  "#CCCCCC",
  8:  "#666666",
  9:  "#FF3333",
  10: "#33FF33",
  11: "#FFFF33",
  12: "#3333FF",
  13: "#FF33FF",
  14: "#33FFFF",
  15: "#FFFFFF"
}

redhat2 = """
             [#ee0001]`.-..........`[/#ee0001]
            [#ee0001]`////////::.`-/.[/#ee0001]
            [#ee0001]-: ....-////////.[/#ee0001]
            [#ee0001]//:-::///////////`[/#ee0001]
     [#ee0001]`--::: `-://////////////:[/#ee0001]
     [#ee0001]//////-    ``.-:///////// .`[/#ee0001]
     [#ee0001]`://////:-.`    :///////::///:`[/#ee0001]
       [#ee0001].-/////////:---/////////////:[/#ee0001]
          [#ee0001].-://////////////////////.[/#ee0001]
         yMN+`.-[#ee0001]::///////////////-`[/#ee0001]
      .-`:NMMNMs`  `..-------..`
       [#243e72]MN+/mMMMMMhoooyysshsss[/#243e72]
MMM    [#243e72]MMMMMMMMMMMMMMyyddMMM+[/#243e72]
 MMMM   [#243e72]MMMMMMMMMMMMMNdyNMMh`     hyhMMM[/#243e72]
  MMMMMMMMMMMMMMMMyoNNNMMM+.   MMMMMMMM
   MMNMMMNNMMMMMNM+ mhsMNyyyyMNMMMMsMM
"""

steam = """
                 ++ 
         ++onNMMMMMNNnn+++
     ooNMANKMMMMMMMMMMMNNn+o
   o+ANMMMMMMMXKNNWWWPFFWNNMNno
  ONNMMMMMMMMMMNWW'' ,.., 'WMMM+
 +NMMMMV+##+VNWWW' .*;'':x, 'WMW+
+VNNWP+######+WW,  *:    :*, +MMM+
'+#############,   *.    ,*' +NMMM
  '*#########*'     '*,,x' .+NMMMM
     `'*###*'          ,.,;###+WNM
         .,;;,      .;##########+W
,',.         ';  ,x##############'
 '###x. :,. .,; ,###############'
  '####.. `'' .,###############'
    '#####xxx################'
      '*##################*'
         ''*##########*''
              ''''''
"""

steamos = Text(steam)

colored_chars = {"O", "n", "m", "M", "N", "P", "F", "W", "V", "+", "X", "K", "A", "o"}

for i, char in enumerate(steam):
    if char in colored_chars:
        steamos.stylize("blue", i, i + 1)

steamoscolor = {
  0:  "#0B0C10",
  1:  "#E84393",
  2:  "#00B894",
  3:  "#FDCB6E",
  4:  "#0984E3",
  5:  "#6C5CE7",
  6:  "#00CEC9",
  7:  "#DADADA",
  8:  "#2D3436",
  9:  "#FF6B6B",
  10: "#55efc4",
  11: "#FFEAA7",
  12: "#74B9FF",
  13: "#A29BFE",
  14: "#81ECEC",
  15: "#FFFFFF"
}

steamos2 = """
           .xXK0kdc'..
           .OMMMMWNK0Odc'.
           .OMMMMMMMMMMWNOl'.
           .OMMMMMMMMMMMMMWXx;.
           .:ddk0XWMMMMMMMMMMNx'
                ..;oxONMMMMMMMWKc.
      [blue]..,;::::;,'.[/blue]   .;xXMMMMMMMNo.
   [blue].':looooooooool:,..[/blue] .;OWMMMMMMNl.
  [blue].:oooooooooooooooooc'[/blue]  .xWMMMMMMK:
 [blue]'coooooooooooooooooool,[/blue]  [#243e72]'OMMMMMMWx.[/#243e72]
[blue].coooooooooooooooooooool.[/blue]  cNMMMMMM0,
[blue]'loooooooooooooooooooooo,[/blue]  ,KMMMMMMX:
[blue]'loooooooooooooooooooooo,[/blue]  ,KMMMMMMX:
[blue].:oooooooooooooooooooooc.[/blue]  lNMMMMMM0,
 [blue].coooooooooooooooooool'[/blue]  ,0MMMMMMWd.
  [blue].:looooooooooooooolc.[/blue]  'OWMMMMMMK;
   [blue]..;cloooooooooc;'..[/blue] .c0WMMMMMMXc.
      [blue]..',;;;;,'..[/blue]  ..cONMMMMMMMXc.
               ..,cxOKWMMMMMMMW0;.
           .cxk0KNWMMMMMMMMMWXo.
           .OMMMMMMMMMMMMMWKo'
           .OMMMMMMMMMMWKx:.
           .OMMMWNX0Oxl;.
           .o0Oxoc,..
"""

ubuntubn = """
                             ....
              .',:clooo:  .:looooo:.
           .;looooooooc  .oooooooooo'
        .;looooool:,''.  :ooooooooooc
       ;looool;.         'oooooooooo,
      ;clool'             .cooooooc.  ,,
         ...                ......  .:oo,
  .;clol:,.                        .loooo'
 :ooooooooo,                        'ooool
'ooooooooooo.                        loooo.
'ooooooooool                         coooo.
 ,loooooooc.                        .loooo.
   .,;;;'.                          ;ooooc
       ...                         ,ooool.
    .cooooc.              ..',,'.  .cooo.
      ;ooooo:.           ;oooooooc.  :l.
       .coooooc,..      coooooooooo.
         .:ooooooolc:. .ooooooooooo'
           .':loooooo;  ,oooooooooc
               ..';::c'  .;loooo:'
"""

ubuntu = Text(ubuntubn, style="#e8510d")

ubuntucolor = {
  0:  "#300A24",
  1:  "#CC241D",
  2:  "#98971A",
  3:  "#D79921",
  4:  "#458588",
  5:  "#B16286",
  6:  "#689D6A",
  7:  "#A89984",
  8:  "#928374",
  9:  "#FB4934",
  10: "#B8BB26",
  11: "#FABD2F",
  12: "#83A598",
  13: "#D3869B",
  14: "#8EC07C",
  15: "#EBDBB2"
}

vanillabn = r"""
              .
            x/A\x
           Z#@#?P`.
          /@$R/.:.',
     _    ($@`.:::.)    _
_-=t'''`-.g$(.::::.!-aZ#$#Kko,
V$#6..::::.~l.::.<&#p***q##$p'
'9#$b,:::::::::.%P~'.:::.`~v'
 "<#$&b,.':::'./'.:::::::.>'
   `~*q@#&b+=- -=+x.,''_.'
     z+'.:::',).:.`~q@6x,
    /.:::::',Z!.:::.`*q&x
   i'.:::',<J?`.':::.\#$&,
   lo._,xd$#%' \'::::.@$#)
   V@#$##@%P'   ~+,''/#$#!
   `~***~^'       `'"**** 
""" 

vanilla = Text(vanillabn, style="#fabc4e")

vanillacolor = {
  0:  "#1B1B1B",
  1:  "#D9534F",
  2:  "#5CB85C",
  3:  "#F0AD4E",
  4:  "#5BC0DE",
  5:  "#9164C1",
  6:  "#5D9CEC",
  7:  "#F7F7F7",
  8:  "#555555",
  9:  "#E74C3C",
  10: "#27AE60",
  11: "#F1C40F",
  12: "#3498DB",
  13: "#9B59B6",
  14: "#1ABC9C",
  15: "#FFFFFF"
}


windowsserverbn = r"""
      ##%%%%%%%%%  %%%%%%%%%##
    ###%%%%%%%%%%  %%%%%%%%%%###
  ####%%%%%%%%%%%  %%%%%%%%%%%####
 ##%%%%%%%%%%%%%%  %%%%%%%%%%%%%%##
#%%%%%%%%%%%%%%%%  %%%%%%%%%%%%%%%%#
%%%%%%%%%%%%%%%%%  %%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%  %%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%  #%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%  #%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%  %%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%  %%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%  %%%%%%%%%%%%%%%%#
 ###%%%%%%%%%%%%%  %%%%%%%%%%%%%%%##
  ####%%%%%%%%%%%  %%%%%%%%%%%#%####
    ##%#%%%%%%%%%  %%%%%%%%%%%######
      ##%%%%%%%%%  %%%%%%%%%########
"""

windowsserver = Text(windowsserverbn, style="#1384c2")

windowsservercolor = {
  0:  "#000000",
  1:  "#A31515",
  2:  "#008000",
  3:  "#808000",
  4:  "#000080",
  5:  "#800080",
  6:  "#008080",
  7:  "#C0C0C0",
  8:  "#808080",
  9:  "#FF0000",
  10: "#00FF00",
  11: "#FFFF00",
  12: "#0000FF",
  13: "#FF00FF",
  14: "#00FFFF",
  15: "#FFFFFF"
}

windowsbn = """
        [red],.=:!!t3Z3z.,
       [red]:tt:::tt333EE3
       [red]Et:::ztt33EEEL [green]@Ee.,      ..,
      [red];tt:::tt333EE7 [green];EEEEEEttttt33#
     [red]:Et:::zt333EEQ. [green]$EEEEEttttt33QL
     [red]it::::tt333EEF [green]@EEEEEEttttt33F
    [red];3=*^```"*4EEV [green]:EEEEEEttttt33@.
    [#1797e7],.=::::!t=.,   [green]@EEEEEEtttz33QF
   [#1797e7];::::::::zt33)   [green]"4EEEtttji3P*
  [#1797e7]:t::::::::tt33.[#fbe91c]:Z3z..  .. ,..g.
  [#1797e7]i::::::::zt33F [#fbe91c]AEEEtttt::::ztF
 [#1797e7];:::::::::t33V [#fbe91c];EEEttttt::::t3
 [#1797e7]E::::::::zt33L [#fbe91c]@EEEtttt::::z3F
[#1797e7]{3=*^```"*4E3) [#fbe91c];EEEtttt:::::tZ`
             [#1797e7]` [#fbe91c]:EEEEtttt::::z7
                 [#fbe91c]"VEzjt:;;z>*`
"""

windows = windowsbn

windowscolor = {
0: "#000000",
1: "#800000",
2: "#008000",
3: "#808000",
4: "#000080",
5: "#800080",
6: "#008080",
7: "#C0C0C0",
8: "#808080",
9: "#FF0000",
10: "#00FF00",
11: "#FFFF00",
12: "#0000FF",
13: "#FF00FF",
14: "#00FFFF",
15: "#FFFFFF"
}


normalbn = r"""
 ██████╗ ██████╗ ███████╗███╗   ██╗██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██║   ██║██████╔╝█████╗  ██╔██╗ ██║██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
╚██████╔╝██║     ███████╗██║ ╚████║██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
"""

normalbn2 = """
      o__ __o                                           o__ __o                                                     
     /v     v\                                         <|     v\                                                    
    />       <\                                        / \     <\                                                   
  o/           \o   \o_ __o      o__  __o   \o__ __o   \o/     o/      o__  __o       __o__    o__ __o    \o__ __o  
 <|             |>   |    v\    /v      |>   |     |>   |__  _<|      /v      |>     />  \    /v     v\    |     |> 
  \\           //   / \    <\  />      //   / \   / \   |       \    />      //    o/        />       <\  / \   / \ 
    \         /     \o/     /  \o    o/     \o/   \o/  <o>       \o  \o    o/     <|         \         /  \o/   \o/ 
     o       o       |     o    v\  /v __o   |     |    |         v\  v\  /v __o   \\         o       o    |     |  
     <\__ __/>      / \ __/>     <\/> __/>  / \   / \  / \         <\  <\/> __/>    _\o__</   <\__ __/>   / \   / \ 
                    \o/                                                                                             
                     |                                                                                              
                    / \                                                                                             
"""

normalbn3 = """
 .----------------.  .----------------.  .----------------.  .-----------------. .----------------.  .----------------.  .----------------.  .----------------.  .-----------------.
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |     ____     | || |   ______     | || |  _________   | || | ____  _____  | || |  _______     | || |  _________   | || |     ______   | || |     ____     | || | ____  _____  | |
| |   .'    `.   | || |  |_   __ \   | || | |_   ___  |  | || ||_   \|_   _| | || | |_   __ \    | || | |_   ___  |  | || |   .' ___  |  | || |   .'    `.   | || ||_   \|_   _| | |
| |  /  .--.  \  | || |    | |__) |  | || |   | |_  \_|  | || |  |   \ | |   | || |   | |__) |   | || |   | |_  \_|  | || |  / .'   \_|  | || |  /  .--.  \  | || |  |   \ | |   | |
| |  | |    | |  | || |    |  ___/   | || |   |  _|  _   | || |  | |\ \| |   | || |   |  __ /    | || |   |  _|  _   | || |  | |         | || |  | |    | |  | || |  | |\ \| |   | |
| |  \  `--'  /  | || |   _| |_      | || |  _| |___/ |  | || | _| |_\   |_  | || |  _| |  \ \_  | || |  _| |___/ |  | || |  \ `.___.'\  | || |  \  `--'  /  | || | _| |_\   |_  | |
| |   `.____.'   | || |  |_____|     | || | |_________|  | || ||_____|\____| | || | |____| |___| | || | |_________|  | || |   `._____.'  | || |   `.____.'   | || ||_____|\____| | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
"""

normalbn4 = """
 _________        .---"----------"---.              
:______.-':      :  .--------------.  :             
| ______  |      | :                : |             
|:______D:|      | |                | |             
|:______D:|      | |                | |             
|:______o:|      | |   OpenRecon    | |             
|         |      | |                | |             
|:_____:  |      | |                | |             
|    ==   |      | :                : |             
|       O |      :  '--------------'  :             
|       o |      :'---...______...---'              
|       o |-._.-i___/'             \._              
|'-.____o_|   '-.   '-...______...-'  `-._          
:_________:      `.____________________   `-.___.-. 
                 .'.eeeeeeeeeeeeeeeeee.'.      |___|
               .'.eeeeeeeeeeeeeeeeeeeeee.'.         
              :____________________________:
"""

#randomize this as normal
starsbn = r"""                  
                         +          +     '                     '         .   + 
             +                      '                                           
        .    .             |                   .                                
                .        --o--    o                    '                    +~~ 
                  |   .    |                                                    
       +    o   - o -                       |                                + o
               +  |           +        *   -+-     +~~                          
     .._  +       |            .         +  |                     +             
   .' .-'`      --o--                                         . .         *     
  /  /            |       '       OpenRecon                                              
  |  |         .    o .  '                    '                             +   
  \  \       '                        .                  '      .            o  
   '._'-._            +~~           .     ' o                           +    .  
      ```                                                     *       *         
               +                        +  |  +           .     oo      .       
 *                                        -+-                         |         
    |                             '        |                        --o--       
   -+-      .                                                         | .       
    |               '                                   '     .         .       
*     .   '                   *      . +      .                        . .     o
"""

Camalbn = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣄⣀⡀
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠙⢶⣄
⠀⣠⣴⠖⠒⠺⣿⣯⠟⢿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠜⠁⠀⠀⠀⠀⠀⠀⠀⠙⠳⣄⡀
⣾⣭⣿⠃⠀⠀⠈⠁⢀⡎⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠒⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲⣄⡀
⠀⠛⠉⠉⠓⠲⣶⠴⠚⠀⠀⢷⠀⠀⠀⠀⠀⠀⠀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀
⠀⠀⠀⠀⠀⠀⠈⣦⠀⠀⠀⠈⢧⡀⠀⠀⢀⣠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠱⡄
⠀⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠉⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡆⠀⠀⠀⢸⣿⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⡇⠀⠀⠀⢸⡿⣧
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠸⣄⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠁⠀⢻⠀⠀⠀⠘⡇⢩⠑⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠒⠀⠀⠒⢲⠛⢦⣀⠀⠀⠀⠹⡆⢀⣀⣀⣀⣠⠴⠋⢸⡇⠀⠀⢘⡇⠀⠀⠀⣧⠘⢦⡏
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡎⠀⢀⡟⠙⡄⠀⠀⡏⠉⠁⠀⠀⠀⠀⠀⠈⢧⠀⠀⡾⠻⣄⠀⠀⠘⣆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⡾⠀⠀⢱⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠘⡆⠀⣧⠀⠈⢳⣄⠀⠘⢦
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠀⢸⠁⠀⠀⠈⡇⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠀⠸⡄⠀⠀⠘⢷⡀⠈⢳⡄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⡜⠀⠀⠀⠀⢳⠀⠘⡆⠀⠀⠀⠀⠀⠀⠀⢀⡏⠀⣰⠃⠀⠀⠀⠀⢹⡀⢸⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⡼⠁⠀⠀⠀⠀⠈⢧⠀⣷⠀⠀⠀⠀⠀⠀⠀⢸⠁⣰⠃⠀⠀⠀⠀⠀⠀⢇⠈⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠁⡼⠀⠀⠀⠀⠀⠀⠀⠘⡄⢻⠀⠀⠀⠀⠀⠀⠀⡈⢀⠇⠀⠀⠀⠀⠀⠀⠀⠈⡄⢷
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡏⢰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠃⠸⡄⠀⠀⠀⠀⠀⠀⡇⢸⡀⠀⠀⠀⠀⠀⠀⠀⢰⠃⠈⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⢀⡶⠠⣇⠀⠀⠀⠀⢀⣼⠁⢸⡇⠀⠀⠀⠀⠀⠀⠀⡼⠂⠀⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡯⡦⠤⠞⠁⠀⠀⠀⠀⠀⠀⢰⣯⣦⡤⢽⠃⠀⠀⠀⢛⣛⠒⠖⠋⠀⠀⠀⠀⠀⠀⢸⡡⣦⠤⠞
"""

normalcolor = {
  0:  "#0A0F1C",
  1:  "#131C2B",
  2:  "#1E2F47",
  3:  "#22384F",
  4:  "#1B6C73",
  5:  "#00A3A3",
  6:  "#00C8C8",
  7:  "#05FFD2",
  8:  "#15FF75",
  9:  "#FFD700",
  10: "#FF8800",
  11: "#FF003C",
  12: "#B30059",
  13: "#8C1AFF",
  14: "#C6F5FF",
  15: "#FFFFFF"
}