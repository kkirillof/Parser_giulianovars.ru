import os
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver

projects = int(input('Сколько проектов пройти? \n Введите значение: ')) + 1


def create_urls():
    Urls = []
    for i in range(projects):
        url = f'https://giulianovars.ru/realizedprojects/proekt_{i}/'
        Urls.append(url)
    print(Urls)
    return Urls


def get_all_HTML(urls):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    try:
        for url in urls:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            not_found = soup.find('div', class_='text-h2 mb-40 text-center', string='СТРАНИЦА НЕ НАЙДЕНА')
            if not_found:
                print(f'[INFO] Страница не найдена для {url}, пропускаем.')
                continue

            project_id = url.split('_')[-1].rstrip('/')
            filename = f'project_{project_id}.html'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(soup.prettify())
            print(f'[INFO] Сохранен HTML для {url} в файл {filename}')

    finally:
        driver.quit()


def parse_urls(urls):
    try:
        for url in urls:
            project_id = url.split('_')[-1].rstrip('/')
            filename = f'project_{project_id}.html'
            if not os.path.exists(filename):
                print(f'[INFO] Файл {filename} не найден, пропускаем.')
                continue
            with open(filename, 'r', encoding='utf-8') as file:
                html = file.read()
            print(f'[INFO] Парсинг HTML для {url} в файле {filename}')

            soup = BeautifulSoup(html, 'html.parser')

            text_upper_divs = soup.find_all('div', class_='text-upper color-grey')
            for text_upper_div in text_upper_divs:
                next_div = text_upper_div.find_next('div')
                if next_div:
                    print(f"{text_upper_div.text.strip()} - {next_div.text.strip()}")

            print('IMG:')
            images = soup.find_all('img', class_='img-cover', loading=False)
            for img in images:
                img_url = f'https://giulianovars.ru{img["src"]}'
                print(img_url)
    except Exception as e:
        print(f'[ERROR] {str(e)}')


def main():
    urls = create_urls()
    get_all_HTML(urls)
    parse_urls(urls)


if __name__ == '__main__':
    main()
