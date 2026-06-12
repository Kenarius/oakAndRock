from sqladmin import ModelView
from sqlalchemy import Text, String
from sqlalchemy.dialects.postgresql import JSONB
import json

from common.db.models.blog import Blog
from common.db.models.catalog import Catalog
from common.db.models.category import Category
from common.db.models.item import Item


def json_formatter(obj):
    """Форматирует JSON для отображения в таблице"""
    if obj:
        try:
            formatted = json.dumps(obj, ensure_ascii=False, indent=2)
            return f'<pre style="max-height: 200px; overflow: auto; background: #f8f9fa; padding: 10px; border-radius: 4px; font-size: 12px;">{formatted}</pre>'
        except:
            return str(obj)
    return ""


def marks_to_html(model, column_name):
    """Форматтер для marks - column_name это строка"""
    marks = getattr(model, column_name)
    if not marks:
        return "Нет меток"

    html = '<div style="max-height: 200px; overflow: auto;">'
    for mark in marks:
        if isinstance(mark, (list, tuple)) and len(mark) >= 3:
            html += f'''
                <div style="display: flex; align-items: center; margin-bottom: 8px; padding: 8px; background: #f8f9fa; border-radius: 4px;">
                    <span style="font-size: 24px; margin-right: 12px;">{mark[0]}</span>
                    <div><strong>{mark[1]}</strong>: {mark[2]}</div>
                </div>
            '''
    html += '</div>'
    return html


def description_marks_to_html(model, column_name):
    """Форматтер для description_marks"""
    marks = getattr(model, column_name)
    if not marks:
        return "Нет меток"

    html = '<div style="max-height: 200px; overflow: auto;">'
    for mark in marks:
        if isinstance(mark, (list, tuple)) and len(mark) >= 2:
            html += f'''
                <div style="margin-bottom: 8px; padding: 8px; background: #f8f9fa; border-radius: 4px;">
                    <strong>{mark[0]}</strong>: {mark[1]}
                </div>
            '''
    html += '</div>'
    return html


def category_title_formatter(model, column_name):
    """Показывает название категории"""
    try:
        category = model.category
        return category.title if category else "Без категории"
    except:
        return "—"


def safe_image_formatter(model, column_name):
    """Безопасный форматтер для изображений"""
    url = getattr(model, column_name)
    if url:
        return f'<img src="{url}" style="max-height: 100px; max-width: 100px; object-fit: cover;" />'
    return ""


def safe_price_formatter(model, column_name):
    """Безопасный форматтер для цены"""
    price = getattr(model, column_name)
    if price:
        return f'<strong>{price}</strong>'
    return ""


class BlogAdmin(ModelView, model=Blog):
    name = "Blog"
    name_plural = "Blogs"

    column_list = [
        Blog.uuid,
        Blog.title,
        Blog.paragraph,
        Blog.description,
        Blog.first_media_url,
        Blog.second_media_url,
        Blog.created_at,
    ]
    column_searchable_list = [Blog.title, Blog.paragraph]
    column_sortable_list = [Blog.created_at, Blog.title]

    column_formatters = {
        Blog.first_media_url: lambda value, _: (
            f'<a href="{value}" target="_blank">Открыть</a>'
            if value else ""
        ),
        Blog.second_media_url: lambda value, _: (
            f'<a href="{value}" target="_blank">Открыть</a>'
            if value else ""
        ),
    }

    form_widget_args = {
        Blog.description: {"rows": 10, "cols": 100},
        Blog.first_media_url: {"placeholder": "https://example.com/image.jpg"},
        Blog.second_media_url: {"placeholder": "https://example.com/image2.jpg"},
    }


class CatalogAdmin(ModelView, model=Catalog):
    name = "Catalog"
    name_plural = "Catalogs"

    column_list = [
        Catalog.uuid,
        Catalog.title,
        Catalog.image_url,
        Catalog.pdf_url,
        Catalog.created_at,
    ]
    column_searchable_list = [Catalog.title]
    column_sortable_list = [Catalog.created_at, Catalog.title]

    column_formatters = {
        Catalog.image_url: lambda value, _: (
            f'<img src="{value}" style="max-height: 100px; max-width: 100px;" />'
            if value else ""
        ),
        Catalog.pdf_url: lambda value, _: (
            f'<a href="{value}" target="_blank">Открыть PDF</a>'
            if value else ""
        ),
    }

    form_widget_args = {
        Catalog.image_url: {"placeholder": "URL изображения каталога"},
        Catalog.pdf_url: {"placeholder": "https://example.com/catalog.pdf"},
    }


class CategoryAdmin(ModelView, model=Category):
    name = "Category"
    name_plural = "Categories"

    column_list = [
        Category.uuid,
        Category.title,
        Category.paragraph,
        Category.main_media_url,
        Category.marks,
        Category.created_at,
    ]
    column_searchable_list = [Category.title, Category.paragraph]
    column_sortable_list = [Category.created_at, Category.title]

    column_formatters = {
        'main_media_url': safe_image_formatter,
        'marks': marks_to_html,
    }

    column_labels = {
        Category.marks: "Метки вида [[\"📱\", \"Название1\", \"Описание1\"], [\"⭐\","
                        " \"Название2\", \"Описание2\"], [\"🎨\", \"Название3\", \"Описание3\"]] ",
        Category.title: "Название категории",
        Category.paragraph: "Заголовок",
        Category.description: "Описание",
        Category.main_media_url: "Ссылка на Главное фото",
        Category.first_media_url: "Ссылка на Первое фото",
        Category.second_media_url: "Ссылка на Второе фото",
    }


class ItemAdmin(ModelView, model=Item):
    name = "Item"
    name_plural = "Items"

    column_list = [
        Item.uuid,
        Item.title,
        Item.subtitle,
        Item.price,
        Item.category_uuid,
        Item.main_media_url,
        Item.marks,
        Item.description_marks,
        Item.created_at,
    ]
    column_searchable_list = [Item.title, Item.subtitle]
    column_sortable_list = [Item.created_at, Item.title, Item.price]
    column_joins = [Category]

    column_formatters = {
        'category_uuid': category_title_formatter,
        'main_media_url': safe_image_formatter,
        'price': safe_price_formatter,
        'marks': marks_to_html,
        'description_marks': description_marks_to_html,
    }

    column_labels = {
        Item.category_uuid: "Категория",
        Item.marks: "Метки",
        Item.description_marks: "Метки описания",
    }

    form_overrides = {
        Item.marks: "Textarea",
        Item.description_marks: "Textarea",
    }

    form_widget_args = {
        Item.description: {"rows": 10, "cols": 100},
        Item.subtitle: {"placeholder": "Краткое описание"},
        Item.price: {"placeholder": "0.00"},
        Item.main_media_url: {"placeholder": "Основное изображение товара"},
        Item.marks: {
            "rows": 12,
            "cols": 100,
            "placeholder": '''[
  ["📱", "Статус", "бестселлер"],
  ["⭐", "Тип", "на заказ"],
  ["🎨", "Стиль", "современный"]
]''',
        },
        Item.description_marks: {
            "rows": 10,
            "cols": 100,
            "placeholder": '''[
  ["Статус", "бестселлер"],
  ["Тип", "на заказ"],
  ["Стиль", "современный"]
]''',
        },
    }

    form_excluded_columns = ["media_urls", "category"]
