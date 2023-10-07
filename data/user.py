from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
import sqlalchemy as sql
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    email = sql.Column(sql.String, unique=True)
    password = sql.Column(sql.String, nullable=True)
    name = sql.Column(sql.String, nullable=True)

    orders = relationship("Post")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    created = sql.Column(sql.DateTime(), default=datetime.now)
    title = sql.Column(sql.String, nullable=True)
    content = sql.Column(sql.String, nullable=True)
    post_owner = sql.Column(sql.String, sql.ForeignKey('users.id'), nullable=True)
