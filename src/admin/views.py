from sqladmin import ModelView

from common.db.models.category import Category
from common.db.models.item import Item


class CategoryAdmin(ModelView, model=Category):
    name = "Category"
    name_plural = "Categories"

    column_list = [
        Category.uuid,
        Category.title,
        Category.paragraph,
        Category.created_at,
    ]
    column_searchable_list = [Category.title, Category.paragraph]
    column_sortable_list = [Category.created_at, Category.title]


class ItemAdmin(ModelView, model=Item):
    name = "Item"
    name_plural = "Items"

    column_list = [
        Item.uuid,
        Item.title,
        Item.subtitle,
        Item.price,
        Item.category_uuid,
        Item.created_at,
    ]
    column_searchable_list = [Item.title, Item.subtitle]
    column_sortable_list = [Item.created_at, Item.title, Item.price]
    form_excluded_columns = ["category"]

