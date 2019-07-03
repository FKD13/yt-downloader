from wtforms import Form, TextField, validators


class DownloadForm(Form):
    name = TextField('Name: ')
    url = TextField('Url: ', validators=[validators.url()])
