"""Models."""
from common.db.models.category import Category
from common.db.models.catalog import Catalog
from common.db.models.item import Item

dao_models = (Category, Catalog, Item)
m2m_tables = ()
