"""Peewee migrations -- 001_init.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw
from decimal import ROUND_HALF_EVEN

from models.owners import Owner

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class BaseModel(pw.Model):
        id = pw.AutoField()

        class Meta:
            table_name = "basemodel"

    @migrator.create_model
    class Setting(pw.Model):
        id = pw.AutoField(primary_key=True)
        token = pw.TextField(default=None, null=True)
        owner = pw.ForeignKeyField(Owner, backref="owners")
        username = pw.TextField(default=None, null=True)
        # json формат листа с сообщениями для рассылки
        messages = pw.TextField(default="[]", null=True)
        mails = pw.TextField(default="[]", null=True)

        captcha_text = pw.TextField(default="Are you human", null=True)
        captcha_buttons = pw.TextField(default="[]", null=True)
        captcha_time = pw.IntegerField(default=30, null=True)
        captcha_first_delay = pw.IntegerField(default=30, null=True)
        captcha_is_on = pw.BooleanField(default=False, null=True)
        captcha_after = pw.BooleanField(default=False, null= True)

        class Meta:
            table_name = "settings"

    @migrator.create_model
    class User(pw.Model):
        id = pw.IntegerField(primary_key=True)
        bot = pw.ForeignKeyField(Setting, backref='settings')
        username = pw.CharField(max_length=255, null=True)
        is_admin = pw.BooleanField(constraints=[SQL("DEFAULT False")], default=False)
        created_at = pw.DateTimeField()

        class Meta:
            table_name = "users"

    @migrator.create_model
    class User(pw.Model):
        id = pw.IntegerField(primary_key=True)

        class Meta:
            table_name = "owners"


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('users')

    migrator.remove_model('settings')

    migrator.remove_model('basemodel')
