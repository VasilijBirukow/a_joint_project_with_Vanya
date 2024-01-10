import requests
from bs4 import BeautifulSoup


def parse_article(url):
    res = requests.get(url)
    # Проверяем статус ответа
    if res.status_code == 200:
        # Преобразуем текст ответа в HTML объект
        soup = BeautifulSoup(res.text, "html.parser")
        # Находим заголовок статьи
        title = soup.find("h1").text
        # Находим основной контент статьи
        content = soup.find("div", class_="mw-content-ltr mw-parser-output")
        # Находим все абзацы в контенте
        paragraphs = content.find_all("p")
        # Создаем список для хранения текста абзацев
        text = [f"<h2>{title}</h2>"]
        # Для каждого абзаца в контенте
        for p in paragraphs:
            # Получаем текст абзаца
            p_text = p.text
            # Заменяем неразрывные пробелы на обычные
            p_text = p_text.replace("\xa0", " ")
            # Оборачиваем текст абзаца в тег <p>
            p_text = f"<p>{p_text}</p>"
            # Добавляем текст абзаца в список
            text.append(p_text)
        # Соединяем список в одну строку с переносами
        return "\n".join(text)
    else:
        return f"Не удалось получить статью с википедии по URL {url}"
