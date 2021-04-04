from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Regexp


class NewOrderForm(FlaskForm):
    title = StringField("Назва",
                        validators=[DataRequired(),
                                    Length(max=100)])

    description = TextAreaField("Опис: ",
                                validators=[Length(max=1000)])

    client = StringField('Клієнт',
                         id='client_autocomplete',
                         validators=[DataRequired(),
                                     Length(max=200)])

    date = StringField("Дата створення",
                       validators=[DataRequired(),
                                   Regexp(r'^(0[1-9]|[12][0-9]|3[01])[\.](0[1-9]|1[012])[\.]((19|20)\d\d|\d\d)$')],
                       default=datetime.now().strftime("%d.%m.%Y"))

    serial = StringField("Серійний номер",
                         id='serial_autocomplete',
                         validators=[Length(max=200)])

    price = FloatField("Ціна", validators=[DataRequired()])
    staff = SelectField("Виконавець")
    submit = SubmitField("Додати")

    def __init__(self, staff_choices: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.staff.choices = staff_choices


class NewClientForm(FlaskForm):
    name = StringField("Ім'я фізичної або юридичної особи",
                       validators=[DataRequired(),
                                   Length(max=200)])

    # validators = [Regexp(r'^(\+\d{1,2}\s?)?((\(?\d{3}\)?)[\s]?\d{3}[\s]?\d{4}|(\(?\d{3,4}\)?)[\s]?\d{3}[\s]?\d{3})$')]
    phone = StringField("Номер телефону",
                        validators=[DataRequired(),
                                    Length(max=80)])

    address = StringField("Адреса",
                          validators=[Length(max=200)])

    notes = TextAreaField("Примітки",
                          validators=[Length(max=1000)])

    submit = SubmitField("Зберегти")

    def __init__(self, client=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if client:
            self.name.data = client.name
            self.phone.data = client.phone
            self.address.data = client.address
            self.notes.data = client.notes


class NewDeviceForm(FlaskForm):
    name = StringField("Назва")
    serial = StringField("Серійний номер", validators=[DataRequired()])
    submit = SubmitField("Зберегти")

    def __init__(self, device=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if device:
            self.name.data = device.name
            self.serial.data = device.serial


class NewStaffForm(FlaskForm):
    name = StringField("Ім'я")
    submit = SubmitField("Зберегти")


class DeleteConfirmForm(FlaskForm):
    delete = SubmitField("Так, видалити")


class NavigationForm(FlaskForm):
    search_field = StringField("Введіть пошуковий запит")

    sort_by_field = SelectField('Сортувати за', choices=[('new_first', 'Датою (нові спочатку)'),
                                                         ('old_first', 'Датою (старі спочатку)'),
                                                         ('title', 'Назвою'),
                                                         ('client', 'Клієнтом'),
                                                         ('status', 'Статусом')])

    status_field = SelectField('Статус', choices=[('0', 'Всі'),
                                                  ('1', 'Нові'),
                                                  ('2', 'В процесі'),
                                                  ('3', 'Виконані'),
                                                  ('4', 'Скасовані')])
