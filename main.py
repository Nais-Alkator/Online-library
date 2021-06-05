import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import argparse
import time
import logging


def check_for_redirection(response):
    response.raise_for_status()
    if response.status_code != 200: 
        raise requests.HTTPError


def get_books_urls(start_page, end_page):
    books_urls = []
    for page in range(start_page, end_page):
        url = "http://tululu.org/l55/{}".format(page)
        response = requests.get(url, verify=False)
        check_for_redirection(response)
        books_links = BeautifulSoup(response.text, "lxml").select(".bookimage")
        for book_link in books_links:
            book_link = book_link.select_one("a")["href"]
            book_url = urljoin(url, book_link)
            books_urls.append(book_url)
    return books_urls


def parse_book_page(book_url):
    book_page = requests.get(book_url, verify=False)
    check_for_redirection(book_page)
    soup = BeautifulSoup(book_page.text, 'lxml')
    title = soup.select_one("h1")
    title = title.text.split("::")
    book_filename = title[0].strip()
    book_filename = sanitize_filename(book_filename)
    book_filename = book_filename 
    author = title[1].strip()
    book_id = book_url.split(".org/b")[1][:-1]
    image_url = soup.select_one(".bookimage a img")["src"]
    image_url = urljoin(book_url, image_url)
    book_path = os.path.join(books_folder, book_filename)
    genres = soup.find("span", class_="d_book").text
    genres = genres.replace(".", '')
    genres = genres.split("Жанр книги: \xa0 ")
    genres = genres[1]
    genres = genres.split(',')
    comments_tags = soup.select("div .texts")
    comments_text = [comment_tag.select_one("span").text for comment_tag in comments_tags]
    parsed_book_page = {
        "title": book_filename, 
        "author": author, 
        "image_url": image_url, 
        "book_path": book_path, 
        "comments": comments_text, 
        "genres": genres, 
        "book_id": book_id}
    return parsed_book_page


def create_json_file(parsed_books_pages, json_path):
    with open(json_path, 'w', encoding="utf8") as file:
        json.dump(parsed_books_pages, file, ensure_ascii=False)


def download_book(book_id):
    url = "http://tululu.org/txt.php"
    payload = {"id": book_id}
    book_file = requests.get(url, params=payload, verify=False)
    check_for_redirection(book_file)
    filename = os.path.join(books_folder, "{0}{1}".format(title, ".txt"))
    with open(filename, 'wb') as file:
        file.write(book_file.content)

def download_image(image_url, images_folder, title):
    image_file = requests.get(image_url, allow_redirects=True, verify=False)
    check_for_redirection(image_file)
    filename = os.path.join(images_folder, "{0}{1}".format(title, image_url[-4:]))
    with open(filename, 'wb') as file:
        file.write(image_file.content)


def get_parser():
    parser = argparse.ArgumentParser(description="Скрипт скачивает книги и обложки к ним с сайта tululu.org")
    parser.add_argument("--start_page", help="Начальная страница для скачивания", type=int, default=1)
    parser.add_argument("--end_page", help="Конечная страница для скачивания", type=int, default=5)
    parser.add_argument("--dest_folder", help="Путь к катологу с результатами парсинга", type=str, default="data")
    parser.add_argument("--skip_imgs", help="Не скачивать картинки", action="store_true")
    parser.add_argument("--skip_txt", help="Не скачивать книги", action="store_true")
    parser.add_argument("--json_path", help="Путь к файлу json", type=str, default="media")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    start_page = args.start_page
    end_page = args.end_page
    dest_folder = args.dest_folder
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt
    json_folder = args.json_path
    books_folder = os.path.join(dest_folder, "books")
    images_folder = os.path.join(dest_folder, "images")
    json_path = os.path.join(json_folder, "info.json")
    os.makedirs(books_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(json_folder, exist_ok=True)
    books_urls = get_books_urls(start_page, end_page)
    parsed_books_pages = [parse_book_page(book_url) for book_url in books_urls]
    create_json_file(parsed_books_pages, json_path)
    for parsed_book_page in parsed_books_pages:
        book_path = parsed_book_page["book_path"]
        image_url = parsed_book_page["image_url"]
        title = parsed_book_page["title"].split("/")[0]
        book_id = parsed_book_page["book_id"]
        try:
            if skip_txt and skip_imgs:
                print("Генерируется файл с информацией о книгах. Добавлена информация о книге '{}'".format(parsed_book_page["title"]))
            elif skip_imgs:
                download_book(book_id)
                print("Скачана книга '{}'".format(title))
                time.sleep(5)    
            elif skip_txt:
                download_image(image_url, images_folder, title)
                print("Скачана обложка книги '{}'".format(title))
                time.sleep(5)
            else:
                download_book(book_id)
                download_image(image_url, images_folder, title)
                print("Скачана книга '{}'' и обложка к ней".format(title))
                time.sleep(5)
        except (requests.HTTPError, requests.ConnectionError) as error:
            logging.warning(error)
            time.sleep(5)
            pass