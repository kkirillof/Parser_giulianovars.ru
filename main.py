import os
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver

projects = int(input('Сколько проектов пройти? \n Введите значение: ')) + 1


# Генерация URL ссылок
def create_urls():
    Urls = []
    for i in range(projects):
        url = f'https://giulianovars.ru/realizedprojects/proekt_{i}/'
        Urls.append(url)
    print(Urls)
    return Urls


# Получение HTML кода проектов
def get_all_HTML(urls):
    # Инициализация браузера
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # Сохранение HTML проектов
    try:
        for url in urls:  # Переход по ссылкам мз списка проектов
            driver.get(url)  # Переход на ссылку в браузере
            soup = BeautifulSoup(driver.page_source, 'html.parser')  # Получение HTML кода страницы

            # Обработка 404 страницы
            not_found = soup.find('div', class_='text-h2 mb-40 text-center', string='СТРАНИЦА НЕ НАЙДЕНА')
            if not_found:
                print(f'[INFO] Страница не найдена для {url}, пропускаем.')
                continue

            # Сохранение HTML в отдельный файл
            project_id = url.split('_')[-1].rstrip('/')  # Получение номера проекта из url
            filename = f'project_{project_id}.html'  # Название файла с его номером
            with open(filename, 'w', encoding='utf-8') as file:  # Запись в файл
                file.write(soup.prettify())
            print(f'[INFO] Сохранен HTML для {url} в файл {filename}')

    # Закрытие браузера при завершении
    finally:
        driver.quit()


# Данные из HTML файла
def parse_urls(urls):
    try:
        for url in urls:  # переход по ссылкам мз списка проектов
            project_id = url.split('_')[-1].rstrip('/')  # Получение номера проекта из url
            filename = f'project_{project_id}.html'  # Название файла с его номером

            # Если файла нет, то пропуск
            if not os.path.exists(filename):
                print(f'[INFO] Файл {filename} не найден, пропускаем.')
                continue

            # Открытие файла и чтение
            with open(filename, 'r', encoding='utf-8') as file:
                html = file.read()
            print(f'[INFO] Парсинг HTML для {url} в файле {filename}')

            soup = BeautifulSoup(html, 'html.parser')  # Получение HTML кода страницы

            # Получение Информации(ГОРОД, САЛОН, ДИЗАЙНЕР-КОНСТРУКТОР)
            print('Информация:')
            text_upper_divs = soup.find_all('div', class_='text-upper color-grey')
            for text_upper_div in text_upper_divs:
                next_div = text_upper_div.find_next('div')
                if next_div:
                    print(f"{text_upper_div.text.strip()} - {next_div.text.strip()}")

            # Получение ссылок на фото проекта
            print('Фото:')
            images = soup.find_all('img', class_='img-cover', loading=False)
            for img in images:
                img_url = f'https://giulianovars.ru{img["src"]}'
                print(img_url)

    # Обработка ошибок
    except Exception as e:
        print(f'[ERROR] {str(e)}')


# Основная функция для выполнения кода
def main():
    urls = create_urls()  # Генерация ссылок
    get_all_HTML(urls)  # Парсинг ссылок на проекты
    parse_urls(urls)  # Получение HTML кода проектов


if __name__ == '__main__':
    main()
