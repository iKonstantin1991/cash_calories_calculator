import datetime as dt


class Record:
    def __init__(self, amount,
                 date=dt.datetime.now().date().strftime('%d.%m.%Y'),
                 comment='not specified'):
        self.amount = amount
        self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, rec):
        self.records.append(rec)

    def get_today_stats(self):
        todayTotalAmount = 0
        todayDate = dt.date.today()
        for record in self.records:
            if todayDate == record.date:
                todayTotalAmount += record.amount
        return todayTotalAmount

    def get_week_stats(self):
        weekTotalAmount = 0
        weekAgoDate = dt.date.today() - dt.timedelta(days=7)
        for record in self.records:
            if record.date >= weekAgoDate and record.date <= dt.date.today():
                weekTotalAmount += record.amount
        return weekTotalAmount


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        todayStats = self.get_today_stats()
        todayRemaining = self.limit - todayStats
        if todayStats < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей ' +
                    f'калорийностью не более {todayRemaining} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    USD_RATE = float(75)
    EURO_RATE = float(90)

    def get_today_cash_remained(self, currency):
        todayStats = self.get_today_stats()
        remainedRub = self.limit - todayStats

        if currency == 'rub':
            todayRemaining = remainedRub
            currencyAnswer = 'руб'
        elif currency == 'usd':
            todayRemaining = round(remainedRub/self.USD_RATE, 2)
            currencyAnswer = 'USD'
        elif currency == 'eur':
            todayRemaining = round(remainedRub/self.EURO_RATE, 2)
            currencyAnswer = 'Euro'
        else:
            print('The currency is not accepted')

        debt = abs(todayRemaining)

        if todayStats < self.limit:
            return f'На сегодня осталось {todayRemaining} {currencyAnswer}'
        elif todayStats == self.limit:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {debt} {currencyAnswer}'
