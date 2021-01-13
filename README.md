# Library's parser
Скрипт скачивает книги и обложки к ним с сайта [tululu.org](http://tululu.org/)

### Как использовать
Для работы скрипта необходим установленный интерпретатор Python3. Затем загрузите зависимости с помощью "pip" (либо "pip3", в случае конфликтов с Python2):  

    pip install -r requirements.txt

Скрипт использует встроенную библиотеку argparse, и перед его запуском пользователь по желанию указывает необходимые аргументы в командной строке. Всего используется 6 аргументов:
1) `start page` - начальная страница для скачивания;
2) `end_page` - конечная страница для скачивания;
3) `dest_folder` - путь к катологу с результатами парсинга;
4) `skip_imgs` - не скачивать картинки;
5) `skip_txt` - не скачивать книги;
6) `json_path` - путь к файлу json.

### Пример использования
Допустим пользователь хочет скачать книги с 1 по 3 страницу. В этом случает запуск скрипта будет выглядеть так:    

    python main.py --start_page 1 --end_page 3

Или необходимо скачать книги с 2 по 4 страницу без обложек:   

    python main.py --start_page 2 --end-page 4 --skip_imgs

Наконец нужно скачать лишь обложки с 3 по 5 страницу:    

    python main.py --start_page 3 --end_page 5 --skip_txt

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).
