import wtforms
from wtforms.validators import length, EqualTo, DataRequired


class RegisterForm(wtforms.Form):
    id = wtforms.StringField('id', validators=[DataRequired(message="用户名不能为空"), length(min=3, max=20)])
    password1 = wtforms.StringField('password1', validators=[length(min=6, max=20)])
    password2 = wtforms.StringField('password2', validators=[EqualTo("password")])
