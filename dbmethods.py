import peewee
import datetime

database = peewee.SqliteDatabase("microfinance.db")


class BaseTable(peewee.Model):
    class Meta:
        database = database


class Finance(BaseTable):
    sum = peewee.FloatField()
    category = peewee.CharField()
    tag = peewee.CharField()
    date = peewee.DateTimeField()
    name = peewee.CharField()
    operation = peewee.CharField()
    total = peewee.FloatField()
    message = peewee.CharField()


database.create_tables([Finance])


def write_to_db(amount, message, category, tag, name, operation, total):
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    new_finance = Finance.create(
        sum=amount,
        category=category,
        tag=tag,
        date=date,
        name=name,
        operation=operation,
        total=total,
        message=message
    )


def del_from_db(finance_id):
    try:
        operation = Finance.get(Finance.id == finance_id)
        operation.delete_instance()
        return True
    except Exception as err:
        print(err)
        return False


def search_today():
    operations = {}
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    try:
        query = Finance.select().where(Finance.date == date).limit(5).order_by(Finance.id.desc())
        finance_selected = query.dicts().execute()
        for finance in finance_selected:
            operations[finance['id']] = finance
    except Exception as err:
        print(err)
    return operations


def search_last():
    try:
        query = Finance.select().limit(1).order_by(Finance.id.desc())
        finance_selected = query.dicts().execute()
        return finance_selected[0]
    except Exception as err:
        print(err)


def search_date():
    pass


def search_name():
    pass


def search_summ():
    pass
