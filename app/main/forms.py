from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required

class SearchSong(FlaskForm):
    search_item = TextAreaField(validators = [Required()])
    submit = SubmitField('Search')