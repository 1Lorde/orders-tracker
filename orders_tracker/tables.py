from flask_table import Table, Col, DateCol


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


class SerialCol(Col):
    def td_format(self, content):
        return '<span class="tag is-medium is-rounded is-light is-primary">' + content.serial + '</span>'


class OrdersTable(Table):
    classes = ['table', 'is-striped', 'is-hoverable', 'is-fullwidth']
    created_at = DateCol("Дата", date_format="d.MM.Y")
    id = Col("№ замовлення")
    title = Col("Назва")
    client = Col("Клієнт")
    device = SerialCol("Пристрій")
    staff = Col("Працівник")
    status = StatusCol("Cтатус")

    def get_tr_attrs(self, item):
        return {'class': 'clickable-row', "data-href": "/orders/" + str(item.id)}

    def get_thead_attrs(self):
        return {'style': 'position: sticky; top: 0; '}


class StaffTable(Table):
    classes = ['table', 'is-striped', 'is-hoverable', 'is-fullwidth', 'is-bordered']
    name = Col("Працівник")
    orders_prev_month = Col("Замовлень за минулий місяць")
    orders_month = Col("Замовлень за цей місяць")
    orders_year = Col("Замовлень за рік")

    def get_tr_attrs(self, item):
        return {'style': 'text-align: center;'}

    def get_thead_attrs(self):
        return {'style': 'position: sticky; top: 0; text-align: center;'}
