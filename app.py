"""
Домашнее задание №5
Первое веб-приложение

- в модуле `app` создайте базовое FastAPI приложение
- создайте обычные представления
  - создайте index view `/`
  - добавьте страницу `/about/`, добавьте туда текст, информацию о сайте и разработчике
  - создайте базовый шаблон (используйте https://getbootstrap.com/docs/5.0/getting-started/introduction/#starter-template)
  - в базовый шаблон подключите статику Bootstrap 5 (подключите стили), примените стили Bootstrap
  - в базовый шаблон добавьте навигационную панель `nav` (https://getbootstrap.com/docs/5.0/components/navbar/)
  - в навигационную панель добавьте ссылки на главную страницу `/` и на страницу `/about/` при помощи `url_for`
  - добавьте новые зависимости в файл `requirements.txt` в корне проекта
    (лучше вручную, но можно командой `pip freeze > requirements.txt`, тогда обязательно проверьте, что туда попало, и удалите лишнее)
- создайте api представления:
  - создайте api router, укажите префикс `/api`
  - добавьте вложенный роутер для вашей сущности (если не можете придумать тип сущности, рассмотрите варианты: товар, книга, автомобиль)
  - добавьте представление для чтения списка сущностей
  - добавьте представление для чтения сущности
  - добавьте представление для создания сущности
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import items


app = FastAPI()

# Подключение статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(items.router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    product_list = items.items_db   # передаем список товаров из api
    return templates.TemplateResponse("base.html", {"request": request, "title": "Главная", "products": product_list})

@app.get("/about/", response_class=HTMLResponse)
def about(request: Request):
    info = {
        "site_name": "HomeWork Otus",
        "developer": "RuKey-Sys",
        "description": "Это сайт, созданный для демонстрации приложения на FastAPI."
    }
    return templates.TemplateResponse("base.html", {"request": request, "title": "О нас", "info": info})

@app.post("/add_product")
def add_product(item: items.Item):
    new_id = len(items.items_db) + 1
    new_product = items.Item(id=new_id, name=item.name, description=item.description, price=item.price)
    items.items_db.append(new_product)  # Добавление товара в базу
    return {"message": "Product added successfully."}
