import urllib.request
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def parcer(url):
    page = urllib.request.urlopen(url)
    text = page.read().decode('utf-8')
    otzyv = re.findall('ratingValue\">(\d+).+\n.+\n.+\n.+\n.+\n.+\n.+\n.+\n.+\n.+\n.+\n.+\n.+reviewBody\".(.+)<\/p>',
                       text)
    return otzyv


urls = ['https://www.wildberries.ru/catalog/13546428/otzyvy', 'https://www.wildberries.ru/catalog/12053381/otzyvy',
        'https://www.wildberries.ru/catalog/13301512/otzyvy', 'https://www.wildberries.ru/catalog/12370161/otzyvy',
        'https://www.wildberries.ru/catalog/14180209/otzyvy']
reviews_good = []
reviews_bad = []
good_reviews = ''
bad_reviews = ''
for i in range(5):
    url = urls[i]
    otzyv = parcer(url)
    for k in range(len(otzyv)):
        if int(otzyv[k][0]) < 3:
            reviews_bad.append(otzyv[k][1])
        elif int(otzyv[k][0]) > 3:
            reviews_good.append(otzyv[k][1])
        else:
            pass

for l in range(len(reviews_bad)):  # это чтобы положительных и отрицательных было поровну
    good_reviews = good_reviews + ' ' + reviews_good[l]
    bad_reviews = bad_reviews + ' ' + reviews_bad[l]

good_reviews = re.sub('[₽#&-;\*\(\(,.!?\d]', ' ', good_reviews)  # чистим и токенизируем
good_reviews = re.sub('&#xA;', '', good_reviews)
good_reviews = re.sub('&quot;', '', good_reviews)
good_reviews = re.sub('[a-zA-Z]', '', good_reviews)
good_reviews = re.sub('\s\s+', ' ', good_reviews)
# good_reviews = re.sub(r'([а-я])([А-Я])', r'\1 \2', good_reviews)
good_data = good_reviews.split()

bad_reviews = re.sub('[₽#&-;\*\(\(,.!?\d]', ' ', bad_reviews)  # чистим и токенизируем
bad_reviews = re.sub('&#xA;', '', bad_reviews)
bad_reviews = re.sub('&quot;', '', bad_reviews)
bad_reviews = re.sub('[a-zA-Z]', '', bad_reviews)
# bad_reviews = re.sub(r'([а-я])([А-Я])', r'\1 \2', bad_reviews)
bad_reviews = re.sub('\s\s+', ' ', bad_reviews)
bad_data = bad_reviews.split()

for c in range(len(bad_data)):  # приводим к одному регистру
    bad_data[c] = bad_data[c].lower()
for d in range(len(good_data)):
    good_data[d] = good_data[d].lower()

for e in range(len(bad_data)):  # приводим к начальной форме
    bad_data[e] = str(morph.parse(bad_data[e]))
    bad_data[e] = re.findall('normal_form=\'([а-я]+)', bad_data[e])[0]
for f in range(len(good_data)):
    good_data[f] = str(morph.parse(good_data[f]))
    good_data[f] = re.findall('normal_form=\'([а-я]+)', good_data[f])[0]

bad_data = list(dict.fromkeys(bad_data))  # убираем повторения
good_data = list(dict.fromkeys(good_data))


for x in bad_data:  # оставляем только уникальные слова — такие, каких нет в другом множестве
    for y in good_data:
        if x == y:
            bad_data.remove(x)
            good_data.remove(y)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return len(lst3)


check_otzyv = parcer('https://www.wildberries.ru/catalog/14180209/otzyvy')  # берем отзывы для проверки


def label(check_text, check_text_new, good_text, bad_text, check_text_item):
    good = intersection(check_text_new, good_text)  # считаем совпадения
    bad = intersection(check_text_new, bad_text)
    check_review_new = list(check_text_item)
    if good >= bad:
        check_review_new.append('good')  # маркируем отзыв в соответствии с тем, что посчитали
    else:
        check_review_new.append('bad')
    good = intersection(check_review, good_data)  # считаем совпадения
    bad = intersection(check_review, bad_data)
    check_review_new = list(check_otzyv[m])
    if good >= bad:
        check_review_new.append('good')  # маркируем отзыв в соответствии с тем, что посчитали
    else:
        check_review_new.append('bad')
    return check_review_new


for m in range(len(check_otzyv)):
    check_review = str(check_otzyv[m][1])

    check_review = re.sub('[₽#&-;\*\(\(,.!?\d]', ' ', check_review)  # чистим и токенизируем
    check_review = re.sub('\[\]', '', check_review)
    check_review = re.sub('&#xA;', '', check_review)
    check_review = re.sub('&quot;', '', check_review)
    check_review = re.sub('[a-zA-Z]', '', check_review)
    check_review = re.sub('\s\s+', ' ', check_review)
    check_review = re.sub(r'([а-я])([А-Я])', r'\1 \2', check_review)
    check_review = check_review.split()

    for r in range(len(check_review)):  # приводим к одному регистру
        check_review[r] = check_review[r].lower()

        check_review[r] = str(morph.parse(check_review[r]))  # приводим к начальной форме
        check_review[r] = re.findall('normal_form=\'([а-я]+)', check_review[r])[0]

label(check_otzyv, check_review, good_data, bad_data, check_otzyv[m])

sup = []
if check_review_new[2] == 'good':  # оцениваем точность
    if int(check_review_new[0]) > 3:
        sup.append(1)
    else:
        sup.append(0)
if check_review_new[2] == 'bad':
    if int(check_review_new[0]) < 3:
        sup.append(1)
    else:
        sup.append(0)
accuracy = sum(sup) / len(sup)  # вычисляем точность
print('accuracy =', round(accuracy, 2))



