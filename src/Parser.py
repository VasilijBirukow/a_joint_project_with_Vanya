import requests
from bs4 import BeautifulSoup


class Parser:
    url = None
    text = None
    article = None

    def __init__(self, url):
        self.url = url
        self.make_article_string()

    def make_article_string(self):
        self.text = self.get_response()
        if self.text is not None:
            self.article = self.parse_text()

    def get_response(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            print(f'Не удалось обратиться по адресу {self.url}')
            return None

    def parse_text(self):
        soup = BeautifulSoup(self.text, "html.parser")
        body = soup.find("body")

        full_text = []

        article_name = body.find("h1").text
        full_text.append(f"<h2>{article_name}</h2>")

        article_content = body.find("div", class_="mw-content-ltr mw-parser-output")

        tags = article_content.find_all("p")

        for tag in tags:
            info = tag.text
            full_text.append(f"<p>{info}</p>")

        return "\n".join(full_text)
