from jinja2 import Environment, FileSystemLoader, select_autoescape
import json 
from livereload import Server
from more_itertools import chunked
import os
import math


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml']))


def create_pages():
    #Создание главной страницы
    with open("media/info.json", "r", encoding='utf-8') as my_file:
      books_json = my_file.read()
    books_json = json.loads(books_json)
    books_per_page = 10
    pages_quantity = (len(books_json) / books_per_page)
    pages_quantity = math.ceil(pages_quantity)
    books_summary = list(chunked(books_json, 2))
    template = env.get_template('template.html')
    rendered_page = template.render(
        books_summary=books_summary,
        pages_quantity=pages_quantity
        )
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)

    #Создание дополнительных страниц
    books_summary = list(chunked(books_json, books_per_page))
    page_number = 1
    for books_group in books_summary:
        books_subgroup = list(chunked(books_group, 2))
        template = env.get_template('template.html')
        page_name = 'pages/index{}.html'.format(page_number)
        rendered_page = template.render(
            books_subgroup=books_subgroup,
            page_number=page_number,
            pages_quantity=pages_quantity,
            )
        with open(page_name, 'w', encoding="utf-8") as file:
            file.write(rendered_page)
        page_number += 1

if __name__ == '__main__':
    os.makedirs("pages", exist_ok=True)
    create_pages()
    server = Server()
    server.watch('template.html', create_pages)
    server.serve(root='.')



