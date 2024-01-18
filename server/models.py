from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ("-recipes.user",'-_password_hash',)

    id = db.Column(db.Integer(255),primary_key = True)
    username = db.Column(db.String(64), unique=True, nullable = False)
    password = db.Column(db.LargeBinary())
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer)
    title = db.Column(db.String,nullable = False)
    user_id = db.Column(db.Integer(64),foreign_key = True)
    instructions = db.Column(db.String)
    minutes_to_complete = db.Column(db.Integer >=(50))

    
    pass