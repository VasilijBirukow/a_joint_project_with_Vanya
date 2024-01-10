import textwrap
import requests
from bs4 import BeautifulSoup

url = input("Введите адрес URL сайта википедии : ")
name_file = input("Введите имя файла для записи статьи : ")
try:
    with open(name_file, "w", encoding="utf-8", errors='ignore') as file:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        body = soup.find("body")
        name_article = body.find("h1").text
        print_name_article = f"\n\nНазвание статьи : {name_article}"
        file.write(print_name_article)
        content = body.find("div", class_="mw-content-ltr mw-parser-output")
        teg_num_p = 0
        for teg in content.find_all("p"):
            if teg.name == "p":
                teg_num_p += 1
        for i in range(teg_num_p):
            info = content.find_all("p")[i].text
            file.write("\n\n" + textwrap.fill(info.replace(" ", ""), width = 100))
    print("Запись прошла успешно")
except requests.exceptions.MissingSchema:
    print("Необходимо ввести адрес URL ссылки!")
except requests.exceptions.InvalidSchema:
    print("Необходимо ввести адрес URL ссылки!")
except AttributeError:
    print("\n\nДанная URL ссылка не относиться к википедии")
except FileNotFoundError:
    print("Данный файл не существует")
