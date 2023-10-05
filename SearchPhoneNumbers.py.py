"""Поиск_номеров_телефонов.ipynb

##Ивенкова Л.В.
"""

import re
import urllib.request
import requests
import glob

url = "https://hands.ru/company/about/"

slashs = [m.start() for m in re.finditer(r'/', url)]

print(slashs)

if (len(slashs) < 3):
    folder_name = url[slashs[1]+1:]
else:
    folder_name = url[slashs[1]+1:slashs[2]]
print(folder_name)

"""Далее можно загружать или только файлы с расширениями js, html, txt - где вероятнее всего обнаружится номер. Или же можно загружать все файлы, убрав флаги, тогда будут просматриваться все файлы, но и время их загрузки увеличится."""

!wget -p -A js,html,txt -c --convert-links https://hands.ru/company/about/

files = glob.glob(folder_name + '/**/*.js', recursive=True)
files += glob.glob(folder_name + '/**/*.html', recursive=True)
files += glob.glob(folder_name + '/**/*.txt', recursive=True)

print(files)

list_numbers = []

for file in files:
    with open(file, "r", errors='ignore') as fl:
        text = fl.read()
        text = re.sub(r"<path[^>]*>", "", text)
        list_numbers += re.findall(r'[:"](?:(?:\+7|8|)[-— ]?\(?[348]\d{2}\)?[-— ]?)?\d{3}(?:[-— ]?\d{2}){2}["]', text)

print(list_numbers)

res_list = []
[res_list.append(x) for x in list_numbers if x not in res_list]
print(res_list)

for i in range(len(res_list)):
    no = re.sub(r"\W", "", res_list[i])
    res_list[i] = no
    if(len(res_list[i]) == 7):
        tmp = "8495" + res_list[i]
        res_list[i] = tmp
    else:
        if (len(res_list[i]) == 10):
            tmp = "8" + res_list[i]
            res_list[i] = tmp

print(res_list)

