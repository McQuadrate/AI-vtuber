def par(str):
  dic = {}
  str = str.split()
  
  for i in range(0,len(str),2):
    dic[str[i+1]] = str[i]

  return dic

def dictionaryRU_JP():
  return  par(
    "ア а イ и ウ у エ э オ о ャ я ュ ю ョ ё" + " イ ы" +
    " カ ка キ ки ク ку ケ кэ コ ко キャ кя キュ кю キョ кё" + " ク к" + 
    " サ са	シ си	ス су	セ сэ	ソ со	シャ ся	シュ сю	ショ сё" + " ス с" + " ス з" +
    " タ та	チ ти	ツ цу	テ тэ	ト то	チャ тя	チュ тю	チョ тё" + " チ т" +
    " ナ на ニ ни ヌ ну ネ нэ ノ но ニャ ня ニュ ню ニョ нё" +
    " ハ ха ヒ хи フ фу ヘ хэ ホ хо ヒャ хя ヒュ хю ヒョ хё" + " ヒュ х" + " フ ф" +
    " マ ма ミ ми ム му メ мэ モ мо ミャ мя ミュ мю ミョ мё" +  " ム м" +
    " ヤ я ユ ю イェ е ヨ ё" + " イ й" +
    " ラ ра リ ри ル ру レ рэ ロ ро リャ ря リュ рю リョ рё" + " ル лу" + " ル л" + " ル р" +
    
    " ワ ва ウィ ви 于 ву ウェ вэ ヲ о" + " ン н" + " 于 в" +
    " ガ га ギ ги グ гу ゲ гэ ゴ го ギャ гя ギュ гю ギョ гё" + " グ г" +
    " ザ дза ジ дзи ズ дзу ゼ дзэ ゾ дзо ジャ дзя ジュ дзю ジョ дзё" +
    " ダ да	ヂ ди	ヅ ду	デ дэ	ド до	ヂャ дя	ヂュ дю	ヂョ дё" + " デ д" + " デ де" +
    " バ ба ビ би ブ бу ベ бэ ボ бо ビャ бя ビュ бю ビョ бё" + " ブ б"+
    " パ па ピ пи プ пу ペ пэ ポ по ピャ пя ピュ пю ピョ пё" + " プ п"
    " ヴォ во ヴャ вя ヴュ вю ヴョ вё" + " シェ се" + " ジェ дзе" + " チェ те" +
    " スィ сы" + " ズィ дзы" +
    " ティ ти ティ ты" + " トゥ ту" + " テャ тя" + " テュ тю" + " テョ тё" +
    " ディ ди ディ ды" + " ドゥ ду" + " デャ дя" + " デュ дю" + " デョ дё" +
    " ツァ ца ツィ ци ツェ цэ ツォ цо" +
    " ファ фа フィ фи ホゥ ху フェ фэ フォ фо フャ фя フュ фю フョ фё" + " リェ ре" +
    " クァ ква" + " クィ кви" + " クゥ кву" + " クェ квэ" + " クォ кво" +
    " グァ гва" + " グィ гви" + " グゥ гву" + " グェ гвэ グォ гво" +
    " ㇱ си ㇲ су"
    )

def keyval(dic):
 mk = list(dic.keys())
 mv = list(dic.values())

 
 mkn = []
 mvn = []

 for i in range(len(mk)):
   if len(mk[i]) > 1 and mk[i][len(mk[i])-1] == 'э':
     mkn.append(mk[i].replace('э', 'е'))
     mvn.append(mv[i])
   if mk[i][0] == 'т':
     mkn.append(mk[i].replace('т', 'ч'))
     mvn.append(mv[i])
   if len(mk[i]) > 1 and mk[i][1] == 'и':
     mkn.append(mk[i].replace('и', 'ы'))
     mvn.append(mv[i])
   if mk[i][0] == 'с':
     mkn.append(mk[i].replace('с', 'з'))
     mvn.append(mv[i])
     mkn.append(mk[i].replace('с', 'ш'))
     mvn.append(mv[i])
   if mk[i][0] == 'з' or (len(mk[i]) > 1 and mk[i][1] == 'з'):
     mkn.append(mk[i].replace('з', 'ж'))
     mvn.append(mv[i])

 for i in range(len(mkn)):
   mk.append(mkn[i])
   mv.append(mvn[i])

 for i in range (0, len(mk) - 1,1):
   for j in range(i + 1, len(mk),1):
     if(len(mk[i]) <= len(mk[j])):
       mk[i], mk[j] = mk[j],mk[i]
       mv[i], mv[j] = mv[j], mv[i]
 return mk, mv

def translit(text,mk,mv):
  text = text.lower()
  text = text.replace('ъ','')
  text = text.replace('ь','')
  for i in range(len(mk)):
    text = text.replace(mk[i], mv[i])
  return text