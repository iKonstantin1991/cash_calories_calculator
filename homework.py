import datetime as dt


class Record:
    def __init__(self, amount, date=None, comment=None):
        self.amount = amount
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, rec):
        self.records.append(rec)

    def get_today_stats(self):
        today_date = dt.date.today()
        return sum([record.amount for record in self.records
                    if record.date == today_date])

    def get_week_stats(self):
        today_date = dt.date.today()
        week_ago_date = today_date - dt.timedelta(days=7)
        return sum([record.amount for record in self.records
                    if today_date >= record.date >= week_ago_date])

    def get_remaining(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_remaining = self.get_remaining()
        if today_remaining > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {today_remaining} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 75.0
    EURO_RATE = 90.0

    def get_today_cash_remained(self, currency):
        remained_rub = self.get_remaining()

        if remained_rub == 0:
            return 'Денег нет, держись'

        answer_lib = {
            'rub': (1, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }

        amount_currency = abs(round(remained_rub/answer_lib[currency][0], 2))
        answer = f'{amount_currency} {answer_lib[currency][1]}'

        if remained_rub > 0:
            return f'На сегодня осталось {answer}'
        else:
            return f'Денег нет, держись: твой долг - {answer}'
