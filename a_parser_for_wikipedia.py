import textwrap
import requests
from bs4 import BeautifulSoup


class Reading:
    def __init__(self, url):
        self.url = url

    def reading(self):
        all_info = []
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, "lxml")
        body = soup.find("body")
        article_name = body.find("h1").text
        article_content = body.find("div", class_="mw-content-ltr mw-parser-output")
        tags = article_content.find_all("p")
        for t in tags:
            info = t.text
            all_info.append(info)
        return [article_name, all_info]


class Writer:
    def __init__(self, url, name_file):
        self.url = url
        self.name_file = name_file

    def parser(self):
        reader = Reading(self.url)
        with open(self.name_file, "w", encoding="utf-8", errors='ignore') as file:
            for line in reader.reading():
                file.write("\n\n" + textwrap.fill(line).replace(" ", ""), width=100)
