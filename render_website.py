from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json 


with open("json/info.json", "r", encoding='utf-8') as my_file:
    books_summary = my_file.read()



env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
	books=json.loads(books_summary)
	)

with open('index.html', 'w', encoding="utf8") as file:
	    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()