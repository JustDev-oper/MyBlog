import sqlalchemy as sa
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp

from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9_]+$',
                                                                          message="Имя пользователя должно содержать только латинские буквы, цифры и символы подчеркивания.")])
    password = PasswordField('Пароль', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9_]+$',
                                                                            message="Пароль должен содержать только латинские буквы, цифры и символы подчеркивания.")])
    remember_me = BooleanField('Запомнить вход')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9_]+$',
                                                                          message="Имя пользователя должно содержать только латинские буквы, цифры и символы подчеркивания.")])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9_]+$',
                                                                            message="Пароль должен содержать только латинские буквы, цифры и символы подчеркивания.")])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password'), Regexp(r'^[a-zA-Z0-9_]+$',
                                                                                   message="Пароль должен содержать только латинские буквы, цифры и символы подчеркивания.")])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Это имя пользователя уже занято.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Эта почта уже зарегистрирована.')


class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9_]+$',
                                                                          message="Имя пользователя должно содержать только латинские буквы, цифры и символы подчеркивания.")])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0)])
    avatar = FileField('Загрузить новую аватарку (необязательно)')
    submit = SubmitField('Подтвердить')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            # Создание запроса для проверки существования имени пользователя
            stmt = sa.select(User).where(User.username == username.data)
            user = db.session.scalars(stmt).first()
            if user is not None:
                raise ValidationError('Это имя пользователя уже занято.')


class CreatePostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    preview = StringField("Превью", validators=[DataRequired(), Length(min=10, max=100)])
    body = TextAreaField("Основное содержание", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Запостить')


class EditPostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    preview = StringField("Превью", validators=[DataRequired(), Length(min=10, max=100)])
    body = TextAreaField("Основное содержание", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Запостить')

    class EditPostForm(FlaskForm):
        def __init__(self, original_title, original_preview, original_body, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title.data = original_title
            self.preview.data = original_preview
            self.body.data = original_body
