from jinja2 import Environment, FileSystemLoader, select_autoescape
import json 
from livereload import Server
from more_itertools import chunked
import os


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml']))



def on_reload():
    with open("json/info.json", "r", encoding='utf-8') as my_file:
      books_summary = my_file.read()
    books_summary = json.loads(books_summary)
    books_summary = list(chunked(books_summary, 10))
    for number, books_group in enumerate(books_summary):
        books_subgroup = list(chunked(books_group, 2))
        template = env.get_template('template.html')
        rendered_page = template.render(
            books_subgroup=books_subgroup
            )
        with open('pages/index{}.html'.format(number), 'w', encoding="utf-8") as file:
                file.write(rendered_page)

os.makedirs("pages", exist_ok=True)

on_reload()

server = Server()

server.watch('template.html', on_reload)

server.serve(root='.')



