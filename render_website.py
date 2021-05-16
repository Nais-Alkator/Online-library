from jinja2 import Environment, FileSystemLoader, select_autoescape
import json 
from livereload import Server
from more_itertools import chunked
import os
import math


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml']))


def create_main_page():
    with open("json/info.json", "r", encoding='utf-8') as my_file:
      books_summary = my_file.read()
    books_summary = json.loads(books_summary)
    books_per_page = 10
    pages_quantity = (len(books_summary) / books_per_page)
    pages_quantity = math.ceil(pages_quantity)
    books_summary = list(chunked(books_summary, 2))
    template = env.get_template('main_template.html')
    rendered_page = template.render(
        books_summary=books_summary,
        pages_quantity=pages_quantity
        )
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)


def on_reload():
    with open("json/info.json", "r", encoding='utf-8') as my_file:
      books_summary = my_file.read()
    books_per_page = 10
    books_summary = json.loads(books_summary)
    books_summary = list(chunked(books_summary, books_per_page))
    pages_quantity = len(books_summary)
    page_number = 1

    for books_group in books_summary:
        books_subgroup = list(chunked(books_group, 2))
        template = env.get_template('page_template.html')
        previous_page_number = page_number - 1
        previous_page_path = 'index{}.html'.format(previous_page_number)
        next_page_number = page_number + 1
        next_page_path = 'index{}.html'.format(next_page_number)
        page_name = 'pages/index{}.html'.format(page_number)
        rendered_page = template.render(
            books_subgroup=books_subgroup,
            page_number=page_number,
            previous_page_path=previous_page_path,
            next_page_path=next_page_path,
            pages_quantity=pages_quantity,
            )
        with open(page_name, 'w', encoding="utf-8") as file:
            file.write(rendered_page)
        page_number += 1

os.makedirs("pages", exist_ok=True)

create_main_page()

on_reload()

server = Server()

server.watch('main_template.html', create_main_page)

server.serve(root='.')



