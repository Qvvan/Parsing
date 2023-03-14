from bs4 import BeautifulSoup
import requests
import time
import threading
import xlsxwriter

#Создаем новый excel файл
workbook = xlsxwriter.Workbook('Результаты.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, 'URL')
worksheet.write(0, 1, 'Время обработки')
worksheet.write(0, 2, 'Кол-во найденных ссылок')
worksheet.write(0, 3, 'Имя файла с результатом')


headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729) '
                         'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


url_list = ['https://crawler-test.com/', 'http://google.com/', 'https://vk.com/', 'https://yandex.ru/', 'https://stackoverflow.com/', 'https://hh.ru/employer']
threads = []

def get_html(url):
    """Получение ответа от сервера"""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response
    else:
        return 0


def get_content(html, url):
    """Получение ссылок с сайта + записываем их в отдельные excel файлы"""
    soup = BeautifulSoup(html.text, 'lxml')
    items = soup.find_all('a')

    workbook = xlsxwriter.Workbook(url[url.find('/', 2) + 2: url.find('.')] + '.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Link')
    length = len(items) #Чтобы не считать длину два раза(для цикла и ретёрна)
    for i in range(length):
        worksheet.write(i, 0, items[i].get('href') if items[i].get('href').find('http') == 0 else url[:-1] + items[i].get('href'))
    workbook.close()
    return length


def main(url, i):
    """Основная ф-ия записи всех сайтов с их значениями в один файл"""
    x1 = time.time()
    html = get_html(url)
    if html:
        count = get_content(html, url)
        x2 = time.time()
        worksheet.write(i, 0, url) #URL страницы
        worksheet.write(i, 1, x2-x1) #Время затраченное на парсинг
        worksheet.write(i, 2, count) #Кол-во ссылок на данном сайте
        worksheet.write(i, 3, url[url.find('/', 2) + 2 : url.find('.')]) #Название файла исходя из сайта



if __name__ == '__main__':
    for i in range(len(url_list)):
        t = threading.Thread(target=main, args=(url_list[i], i+1,))
        threads.append(t)
        t.start()

    #Ждем пока все потоки завершатся, чтобы сохранить результат в excel файл
    for t in threads:
        t.join()
    workbook.close()