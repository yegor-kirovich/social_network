from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
import sqlalchemy as sql
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    email = sql.Column(sql.String, unique=True)
    password = sql.Column(sql.String, nullable=True)
    name = sql.Column(sql.String, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
