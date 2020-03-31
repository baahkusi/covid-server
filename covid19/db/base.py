import datetime
from peewee import Model, DateTimeField
from ..config import db

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    utime = DateTimeField(default=datetime.datetime.now)
    ctime = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = db
        legacy_table_names=False