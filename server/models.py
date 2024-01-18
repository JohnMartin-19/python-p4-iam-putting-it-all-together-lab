from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ("-recipes.user",'-_password_hash',)

    id = db.Column(db.Integer(),primary_key = True)
    username = db.Column(db.String(64), unique=True, nullable = False)
    _password_hash = db.Column(db.String())
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', backref='user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Passwords cannot be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        return bcrypt.check_password_hash(
            self._password_hash,password.encode('utf-8')
        )
    
    def __repr__(self):
        return f"User {self.username}"

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    __table_args__ = (
        db.CheckConstraint('length(instructions) >= 50'),
    )

    id = db.Column(db.Integer(),primary_key = True)
    title = db.Column(db.String,nullable = False)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    instructions = db.Column(db.String)
    minutes_to_complete = db.Column(db.Integer )

    
    def __repr__(self):
     return f"Recipe {self.id}: {self.title}"