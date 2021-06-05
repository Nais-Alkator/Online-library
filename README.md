# Online-Library
Онлайн-библиотека книг, скачанных с сайта [tululu.org](http://tululu.org/).

### Как использовать
Для работы скрипта необходим установленный интерпретатор Python3. Затем загрузите зависимости с помощью "pip" (либо "pip3", в случае конфликтов с Python2):  

    pip install -r requirements.txt

После этого скачайте книги используя скрипт [Library's parser](https://github.com/Nais-Alkator/Library-s-parser).

Затем запустите команду:

    python render_website.py

И откройте сайт в браузере по адресу `127.0.0.1:5500`.

![Иллюстрация к проекту](https://github.com/Nais-Alkator/Online-library/screenshots/online-library.png)

Скрипт использует данные из каталогов:
1) `media` и его подкаталогов `books` и `images`, в которых находятся текстовые файлы книг в формате `txt` и обложки в формате `jpg`.
2) `json` - содержит файл info.json, с информацией о книгах.
3) `pages`, в котором хранятся страницы онлайн-библиотеки.

[Онлайн версия библиотеки](https://nais-alkator.github.io/Online-library/)

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).
