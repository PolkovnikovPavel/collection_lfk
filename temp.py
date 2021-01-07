from datetime import date
from dateutil.relativedelta import relativedelta

six_months = date.today() + relativedelta(days=1)
print(six_months)