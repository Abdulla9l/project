import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

url = 'https://hajjmision.ru/bjk/11694453d63d91f5a671899dfa_ar.html'
response = requests.get(url)

if response.status_code == 200:
    page_content = response.content
    soup = BeautifulSoup(page_content, 'html.parser')

    # Сохранение HTML страницы
    with open('page.html', 'wb') as file:
        file.write(soup.prettify('utf-8'))

    # Получение базового URL
    base_url = response.url

    # Дополнительно: сохранение CSS, JS и изображений
    for i, link in enumerate(soup.find_all('link', {'rel': 'stylesheet'})):
        css_url = link.get('href')
        # Формирование абсолютного URL, если он не задан явно
        if not urlparse(css_url).scheme:
            css_url = urljoin(base_url, css_url)
        # Извлечение имени файла из URL
        filename = os.path.basename(urlparse(css_url).path).strip()
        css_response = requests.get(css_url)
        with open(filename, 'wb') as file:
            file.write(css_response.content)

    for i, script in enumerate(soup.find_all('script', {'src': True})):
        js_url = script.get('src')
        # Формирование абсолютного URL, если он не задан явно
        if not urlparse(js_url).scheme:
            js_url = urljoin(base_url, js_url)
        # Извлечение имени файла из URL
        filename = os.path.basename(urlparse(js_url).path).strip()
        js_response = requests.get(js_url)
        with open(filename, 'wb') as file:
            file.write(js_response.content)

    for i, img in enumerate(soup.find_all('img', {'src': True})):
        img_url = img.get('src')
        # Формирование абсолютного URL, если он не задан явно
        if not urlparse(img_url).scheme:
            img_url = urljoin(base_url, img_url)
        # Извлечение имени файла из URL
        filename = os.path.basename(urlparse(img_url).path).strip()
        img_response = requests.get(img_url)
        with open(filename, 'wb') as file:
            file.write(img_response.content)

else:
    print('Failed to retrieve the page')
