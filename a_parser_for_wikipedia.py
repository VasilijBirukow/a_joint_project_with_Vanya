import textwrap
import requests
from bs4 import BeautifulSoup

url = "https://ru.wikipedia.org/wiki/Тобольск"
try:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    body = soup.find("body")
    article_name = body.find("h1").text
    article_content = body.find("div", class_="mw-content-ltr mw-parser-output")

    print(f"\n\nНазвание статьи : {article_name}")
    tags = article_content.find_all("p")
    for t in tags:
        info = t.text
        print("\n\n" + textwrap.fill(info.replace(" ", ""), width=100))

except requests.exceptions.InvalidSchema:
    print("Необходимо ввести адрес URL ссылки!")
except AttributeError:
    print("\n\nДанная URL ссылка не относиться к википедии")
except FileNotFoundError:
    print("Данный файл не существует")
