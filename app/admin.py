from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import Category, Product

admin = Admin(app, name='E-commerce Administration', template_mode='bootstrap4')


class ProductsView(ModelView):
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']


admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductsView(Product, db.session))
