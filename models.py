import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('taco.db')


class User(UserMixin, Model):
  email = CharField(unique=True)
  password = CharField(max_length=100)
  
  class Meta:
    database = DATABASE
    
  def get_tacos(self):
    return Tacos.self().where(Taco.user == self)
  
  @classmethod
  def create_user(cls, email, password, admin=False):
    try:
      with DATABASE.transaction():
        cls.create(
          email=email,
          password=generate_password_hash(password)
        )
    except IntegrityError:
      raise ValueError("User already exists")
    

class Taco(Model):
  timestamp = DateTimeField(default=datetime.datetime.now)
  user = ForeignKeyField(User, related_name='tacos')
  protein = TextField()
  shell = TextField()
  cheese = BooleanField()
  Extras = TextField(null=True)
  
  class Meta:
    database = DATABASE


def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, Taco], safe=True)
  DATABASE.close()