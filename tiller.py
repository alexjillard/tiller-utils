import csv
from datetime import datetime, timedelta
from decimal import Decimal
import glob

# Input
#  date, description, credit, debit

accounts = {
    'chequing': ('Chequing', 'xxxx6390', 'CIBC'),
    'visa': ('CIBC VISA', 'xxxx8650', 'CIBC'),
    'savings': ('Savings','xxxx2699', 'CIBC'),
    'loc': ('Line of Credit', 'xxxx2437', 'CIBC'),
}

def get_files():
    return glob.glob('./*-*.csv')

def format_row(row, account):
    amount = row.get('debit')
    if not amount:
        amount = Decimal(row.get('credit')) * -1
    

    account_info = accounts.get(account)

    txn_date = datetime.strptime(row.get('date'), '%Y-%m-%d').date()

    return {
        'date': txn_date,
        'description': row.get('description'),
        'category': '',
        'amount': amount,
        'account':account_info[0],
        'account_number':account_info[1],
        'institution': account_info[2],
        'month': f'{txn_date:%Y-%m}-01',
        'week': txn_date - timedelta(days=txn_date.isoweekday() % 7),
        'txn_id': '',
        'notes': '',
        'full_desc': row.get('description'),
        'categorized_date': '',
        'tags': '',
        'date_added': f'{datetime.today():%Y-%m-%d}',
    }

def run():
    output = []


    for f in get_files():
        print(f)
        with open(f) as in_file:
            account = f.split('-')[0].lstrip('./')
            if not account in accounts:
                raise ValueError(f'{account} not in list of valid accounts. Ensure file name is in the format of "accountname-yyyy-mm-dd.csv"')
            reader = csv.DictReader(in_file, fieldnames=['date', 'description', 'credit', 'debit'])
            for row in reader:
                output.append(format_row(row, account))
    
    output.sort(key=lambda x: x['date'])
    with open('output.csv', 'w') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=['date', 'description','category','amount','account','account_number','institution','month','week','txn_id','notes','full_desc','categorized_date','tags','date_added'])
        writer.writerows(output)



if __name__ == '__main__':
    run()