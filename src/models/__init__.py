from .base import db
from peewee import *
from playhouse.migrate import *
from src.models import fatturaEl as m

list_of_models = [m.XmlFile, m.CliFor, m.SediCliFor, m.Doc, m.DocRow, m.Pagamenti, m.DocAttachment, m.DocAliquota]


def syncModels(model):
    if not model.table_exists():
        model.create_table()
    else:
        model_columns = model._meta.columns
        db_columns = db.get_columns(model._meta.table_name)

        if len(model_columns) > len(db_columns):
            migrator = SqliteMigrator(db)
            for column in model_columns:
                exist_db_column = False
                for db_col in db_columns:
                    if db_col.name == column:
                        exist_db_column = True
                        break
                if not exist_db_column:
                    if model_columns[column].field_type == 'VARCHAR':
                        new_field = CharField(null=True)
                    if model_columns[column].field_type == 'TEXT':
                        new_field = TextField(null=True)
                    if model_columns[column].field_type == 'BOOL':
                        new_field = BooleanField(default=False)
                    if model_columns[column].field_type == 'INT':
                        new_field = IntegerField(null=True)
                    # new_field.add_to_class(model._meta.table_name, column)
                    migrate(migrator.add_column(model._meta.table_name, column, new_field))
        
        if len(model_columns) < len(db_columns):
            for column in db_columns:
                exist_db_column = False
                for model_col in model_columns:
                    if model_col == column.name:
                        exist_db_column = True
                        break
                if not exist_db_column:
                    if column.data_type == 'VARCHAR':
                        new_field = CharField(null=True)
                    if column.data_type == 'TEXT':
                        new_field = TextField(null=True)
                    if column.data_type == 'BOOL':
                        new_field = BooleanField(default=False)
                    if column.data_type == 'INT':
                        new_field = IntegerField(null=True)
                    # new_field.add_to_class(model, column.name)
                    model._meta.add_field(column.name, new_field)


for model in list_of_models:
    syncModels(model)
