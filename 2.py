import pymorphy2
from pymystem3 import Mystem
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    Doc
)
import re

# сначала поработаю с русским
text_ru = 'К счастью, больной был прооперирован удачно. Новый факультет, образованный в институте по приказу министерства, пользуется большой популярностью. Девушка очень образованна. Больной котенок нашел дом и выздоровел! Морозна ночь, все небо ясно. Он не заметил нас и прошел мимо, хотя вокруг было относительно светло, и мне стало всё ясно. Мой друг снова прошел мимо меня, не поздоровавшись, зато новые друзья были мне рады. Что же ты стоишь? Что ты будешь делать? Он сказал мне, что не приедет. Он ушел, как стемнело. Она обратила внимание на то, как стало темно. У меня в руках была ручная пила. Три дня я пила только воду.'
text_ru = text_ru.lower()  # так будет удобнее сравнивать рез-ты, потому что pymorphy сам приводит всё к нижнему регистру

# чищу и токенизирую для pymorphy и mystem
ru_text_clean = re.sub('[₽#&-;\*\(\(,.!?\d]', ' ', text_ru)
ru_text_split = ru_text_clean.split()

ru_pymorphy_raw = []  # использую pymorphy
morph = pymorphy2.MorphAnalyzer()
for i in range(len(ru_text_split)):
    ru_pymorphy_raw.append(morph.parse(ru_text_split[i]))
ru_pymorphy_str = str(ru_pymorphy_raw)
# привожу к единому стандарту. не стала делать функцию, тк у всех теггеров разные теги…
ru_pymorphy_str = re.sub('ADJ[SF]', 'ADJ', ru_pymorphy_str)
ru_pymorphy_str = re.sub('PRT[SF]', 'VERB', ru_pymorphy_str)
ru_pymorphy_str = re.sub('GRND', 'VERB', ru_pymorphy_str)
ru_pymorphy_str = re.sub('INFN', 'VERB', ru_pymorphy_str)
ru_pymorphy_str = re.sub('ADVB', 'ADV', ru_pymorphy_str)
ru_pymorphy_str = re.sub('PRCL', 'PTLC', ru_pymorphy_str)
ru_pymorphy_str = re.sub('NPRO', 'PRO', ru_pymorphy_str)
ru_pymorphy_str = re.sub('NUMR', 'NUM', ru_pymorphy_str)
ru_pymorphy = re.findall('\[Parse\(word=\'([а-яё]+)\',\stag=OpencorporaTag\(\'([A-Z]+)', ru_pymorphy_str)

m = Mystem()  # использую mystem
ru_text_str = str(ru_text_split)
ru_mystem_raw = m.analyze(ru_text_str)
ru_mystem_str = str(ru_mystem_raw)
ru_mystem_str = re.sub('S', 'NOUN', ru_mystem_str)  # привожу к единому стандарту
ru_mystem_str = re.sub('A', 'ADJ', ru_mystem_str)
ru_mystem_str = re.sub('PR', 'PREP', ru_mystem_str)
ru_mystem_str = re.sub('V', 'VERB', ru_mystem_str)
ru_mystem_str = re.sub('[AS]PRO', 'PRO', ru_mystem_str)
ru_mystem_str = re.sub('PART', 'PTCL', ru_mystem_str)
ru_mystem = re.findall('text\':\s\'([а-яА-Яё]+)\',\s\'[a-z]+\':\s\[\{\'wt\':\s[\d\.]+,\s\'lex\':\s\'[а-яё]+\',\s\'gr\':\s\'([A-Z]+)', ru_mystem_str)
print(ru_mystem)

segmenter = Segmenter()  # использую natasha
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
doc = Doc(text_ru)
doc.segment(segmenter)
doc.tag_morph(morph_tagger)
ru_natasha_raw = doc.tokens
ru_natasha_str = str(ru_natasha_raw)
ru_natasha_str = re.sub('ADP', 'PREP', ru_natasha_str)  # привожу к единому стандарту
ru_natasha_str = re.sub('AUX', 'VERB', ru_natasha_str)
ru_natasha_str = re.sub('CCONJ', 'CONJ', ru_natasha_str)
ru_natasha_str = re.sub('SCONJ', 'CONJ', ru_natasha_str)
ru_natasha_str = re.sub('PRON', 'PRO', ru_natasha_str)
ru_natasha_str = re.sub('PART', 'PTCL', ru_natasha_str)
ru_natasha = re.findall('text=\'([а-яА-Яё]+)\',\spos=\'([A-Z]+)', ru_natasha_str)

#теперь ручная разметка
ru_manually_raw = 'к PREP счастью NOUN больной NOUN был VERB прооперирован VERB удачно ADV новый ADJ факультет NOUN образованный VERB в PREP институте NOUN по PREP приказу NOUN министерства NOUN пользуется VERB большой ADJ популярностью NOUN девушка NOUN очень ADV образованная ADJ больной ADJ котенок NOUN нашел VERB дом NOUN и CONJ выздоровел VERB морозна ADJ ночь NOUN все ADJ небо NOUN ясно ADJ он PRO не PTCL заметил VERB нас PRO и CONJ прошел VERB мимо ADV хотя CONJ вокруг PREP было VERB относительно ADV светло ADV и CONJ мне PRO стало VERB всё NOUN ясно ADV мой PRO друг NOUN снова ADV прошел VERB мимо PREP меня PRO не PTCL поздоровавшись VERB зато CONJ новые ADJ друзья NOUN были VERB мне PRO рады ADJ что ADV же PTCL ты PRO стоишь VERB что PRO ты PRO будешь VERB делать VERB он PRO сказал VERB мне PRO что CONJ не PTCL приедет VERB он PRO ушел VERB как CONJ стемнело VERB она PRO обратила VERB внимание NOUN на PREP то PRO как PRO стало VERB темно ADV у PREP меня PRO в PREP руках NOUN была VERB ручная ADJ пила NOUN три NUM дня NOUN я PRO пила VERB только ADV воду NOUN'


def manually_into_list(string_raw):  # преобразовываю ручную разметку в годный для сравненеия вид
    string_raw = string_raw.split()
    list = []
    for k in range(len(string_raw)):
        if (k != 0 and k % 2 == 1):
            pass
        else:
            list.append((string_raw[k], string_raw[k + 1]))
    return list


ru_manually = manually_into_list(ru_manually_raw)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return len(lst3)


def accuracy_check(list1, list2):  # функция вычисления точности
    accuracy = round((intersection(list1, list2)/101), 2)
    return accuracy


pymorphy_accuracy = accuracy_check(ru_pymorphy, ru_manually)  # считаю
mystem_accuracy = accuracy_check(ru_mystem, ru_manually)
natasha_accuracy = accuracy_check(ru_natasha, ru_manually)

if pymorphy_accuracy > mystem_accuracy:  # находит и объявляет самый точный русский теггер
    if pymorphy_accuracy > natasha_accuracy:
        print('pymorphy самый точный из русских:', pymorphy_accuracy, ' vs ', mystem_accuracy, ' и ', natasha_accuracy)
    else:
        print('natasha самая точная из русских:', natasha_accuracy, ' vs ', pymorphy_accuracy, ' и ', mystem_accuracy)
elif pymorphy_accuracy < mystem_accuracy:
    if mystem_accuracy > natasha_accuracy:
        print('mystem самый точный из русских:', mystem_accuracy, ' vs ', pymorphy_accuracy, ' и ', natasha_accuracy)
    else:
        print('natasha самая точная из русских:', natasha_accuracy, ' vs ', pymorphy_accuracy, ' и ', mystem_accuracy)
else:
    if pymorphy_accuracy > natasha_accuracy:
        print('pymorphy и mystem самые точные из русских:', pymorphy_accuracy, ' и ', mystem_accuracy, ' vs ', natasha_accuracy)
    else:
        print('natasha самая точная из русских:', natasha_accuracy, ' vs ', pymorphy_accuracy, ' и ', mystem_accuracy)


# перейдём к английскому
text_en = 'Back up and give me an answer. Stop and answer my question. He wants to frame me for stealing the gold frame. If you set us on fire the boss will definitely fire you. I saw a giant saw outside the shelter, it destroyed the tree that was about to flower. Why did you fool me into believing that this function would work? Could you please iron my suit? Did I tell you that they paid me a visit the other night when I was trying to finally get some sleep? Email me later and we will discuss that email. Can you guess what type of glue I used to do this object? Wake up and help me to find my watch!'
en_manually_raw = 'Back VERB up ADV and CONJ give VERB me PRO an ART answer NOUN Stop VERB and CONJ answer VERB my PRO question NOUN He PRO wants VERB to PREP frame VERB me PRO for PREP stealing VERB the ART gold ADJ frame NOUN If CONJ you PRO set VERB us PRO on PREP fire NOUN the ART boss NOUN will VERB definitely ADV fire VERB you PRO I PRO saw VERB a ART giant ADJ saw NOUN outside ADV the ART shelter NOUN it PRO destroyed VERB the ART tree NOUN that CONJ was VERB about PREP to PREP flower VERB Why ADV did VERB you PRO fool VERB me PRO into PREP believing VERB that CONJ this ART function NOUN would VERB work VERB Could VERB you PRO please ADV iron VERB my PRO suit NOUN Did VERB I PRO tell VERB you PRO that CONJ they PRO paid VERB me PRO a ART visit NOUN the ART other ADJ night NOUN when ADV I PRO was VERB trying VERB to PREP finally ADV get VERB some ADJ sleep NOUN Email VERB me PRO later ADV and CONJ we PRO will VERB discuss VERB that ART email NOUN Can VERB you PRO guess VERB what ADJ type NOUN of PREP glue NOUN I PRO used VERB to PREP do VERB this ART object NOUN Wake VERB up ADV and CONJ help VERB me PRO to PREP find VERB my PRO watch NOUN'

en_manually = manually_into_list(en_manually_raw)
