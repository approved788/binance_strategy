from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField
from wtforms.validators import DataRequired

class SysSettings(FlaskForm):
    ma_period = IntegerField('MA Period:', validators=[DataRequired(message='Wrong format, retry')])
    ma_up = FloatField('MA Up:', validators=[DataRequired(message='Wrong format, retry')])
    ma_dn = FloatField('MA Dn:', validators=[DataRequired(message='Wrong format, retry')])
    risk_vol = FloatField('Fix Risk Vol:', validators=[DataRequired(message='Wrong format, retry')])