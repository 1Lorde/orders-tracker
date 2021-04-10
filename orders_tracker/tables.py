from flask_table import Table, Col, DateCol, NestedTableCol


class ClientsTable(Table):
    classes = ['table', 'is-striped', 'is-hoverable', 'is-fullwidth']
    name = Col("Ім'я фізичної або юридичної особи")
    phone = Col("Номер телефону")
    address = Col('Адреса')
    notes = Col('Примітки')

    def get_tr_attrs(self, item):
        return {'class': 'clickable-row', "data-href": "/clients/" + str(item.id)}

    def get_thead_attrs(self):
        return {'style': 'position: sticky; top: 0; '}


class StatusCol(Col):
    def td_format(self, content):
        if content.name == 'Нове':
            return '<span class="tag is-medium is-rounded is-light is-link">' + content.name + '</span>'
        elif content.name == 'В процесі':
            return '<span class="tag is-medium is-rounded is-light is-warning">' + content.name + '</span>'
        elif content.name == 'Виконано':
            return '<span class="tag is-medium is-rounded is-light is-success">' + content.name + '</span>'
        elif content.name == 'Скасовано':
            return '<span class="tag is-medium is-rounded is-light is-danger">' + content.name + '</span>'

        return '<span class="tag is-medium is-rounded is-light">' + content.name + '</span>'


class SerialCol(Col):
    def td_format(self, content):
        return '<span class="tag is-medium is-rounded is-light is-primary">' + content.serial + '</span>'


class TypeCol(Col):
    def td_format(self, content):
        if content.name == 'Заправка':
            return f'<span class="tag is-black tag_shadow is-unselectable"><strong>{content.name}<strong></span>'
        elif content.name == 'Інше':
            return f'<span class="tag is-light tag_shadow is-unselectable"><strong>{content.name}<strong></span>'

        return f'<span class="tag is-white tag_shadow is-unselectable"><strong>{content.name}</strong></span>'


class OrdersTable(Table):
    classes = ['table', 'is-striped', 'is-hoverable', 'is-fullwidth']
    created_at = DateCol("Дата", date_format="d.MM.Y")
    id = Col("№ замовлення")
    type = TypeCol("Тип")
    description = Col("Опис")
    client = Col("Клієнт")
    device = SerialCol("Пристрій")
    staff = Col("Працівник")
    status = StatusCol("Cтатус")

    def get_tr_attrs(self, item):
        return {'class': 'clickable-row', "data-href": "/orders/" + str(item.id)}

    def get_thead_attrs(self):
        return {'style': 'position: sticky; top: 0; '}


class StatsCol(Col):
    def td_format(self, content):
        return f'<div class="level">' \
               f'<span class="level-item tag is-rounded is-medium is-light mr-5">' \
               f'<ion-icon name="funnel"></ion-icon>' \
               f'<strong class="pl-2">{content.refills}</strong>' \
               f'</span>' \
               f'<span class="level-item tag is-rounded is-medium is-light">' \
               f'<strong class="pr-2">{content.refills}</strong>' \
               f'<ion-icon name="bag-check"></ion-icon>' \
               f'</span>' \
               f'</div>'


class StaffTable(Table):
    classes = ['table', 'is-fullwidth', 'is-bordered', 'has-text-centered']
    name = Col("Працівник")
    stats_prev_month = StatsCol("За минулий місяць")
    stats_month = StatsCol("За цей місяць")
    stats_year = StatsCol("За рік")

    def get_thead_attrs(self):
        return {'style': 'position: sticky; top: 0;'}
