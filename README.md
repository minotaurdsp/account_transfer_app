# account_transfer_app



## install
virtualenv env

source env/bin/activate

pip install -r requirements.txt


## setup
./manage.py migrate
./manage.py update_currency_rate_index   
./manage.py init_demo_data


## ./manage.py shell
from acount.models import Account

account1  = Account.objects.filter(currency__iso_code='USD').get()

account2  = Account.objects.filter(currency__iso_code='EUR').get()

account1.transfer(account2,2)


## Deposit
account  = Account.objects.filter(currency__iso_code='USD').get()

ut = account.deposit(20)

## Withdraw
account  = Account.objects.filter(currency__iso_code='USD').get()

ut = account.withdraw(20)

## Transfer
src  = Account.objects.filter(uid=74142540).get()

dst  = Account.objects.filter(uid=15068630).get()

result = src.transfer(dst,20)

