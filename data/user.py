from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
import sqlalchemy as sql


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    email = sql.Column(sql.String, unique=True)
    password = sql.Column(sql.String, nullable=True)
    name = sql.Column(sql.String, nullable=True)
