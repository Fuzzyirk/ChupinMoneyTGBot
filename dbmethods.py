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
    total = peewee.FloatField()
    message = peewee.CharField()


database.create_tables([Finance])


def write_to_db(amount, message, category, tag, name='Max', total=0):
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    new_finance = Finance.create(
        sum=amount,
        category=category,
        tag=tag,
        date=date,
        name=name,
        total=total,
        message=message
    )


# def del_from_db(sum, tag):
#     pass


def search_today():
    operations = {}
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    try:
        query = Finance.select().where(Finance.date == date).limit(5).order_by(Finance.id.desc())
        finance_selected = query.dicts().execute()
        i = 0
        for finance in finance_selected:
            i += 1
            operations[i] = finance
    except Exception as err:
        print(err)
    return operations


def search_date():
    pass


def search_name():
    pass


def search_summ():
    pass
