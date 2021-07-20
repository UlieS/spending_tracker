from datetime import date as dtdate

import requests
from requests.structures import CaseInsensitiveDict

from banking.statement_parsing import _assign_category
from banking.verified_accounts import Account
from database import constants
from database.database_connection import connect_to_db, get_latest_transaction_date, write_to_db
from transactions.transactions import Transaction


def query_bank(account: Account):

    token = constants['nordigen']['access_token']
    url = f"https://ob.nordigen.com/api/accounts/{account.account_id}/transactions/"
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Token " + token

    trusted_accounts = {iban:account for account, iban in constants['wallets'].items()}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ConnectionError(response.json())

    db = connect_to_db()
    last_updated_date = get_latest_transaction_date(db)
    new_transactions = []

    for booking in response.json()['transactions']['booked']:
        date = booking['bookingDate']
        date = dtdate(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))
        if date > last_updated_date:
            desc = booking.get('remittanceInformationUnstructured', '') + ' ' + booking.get('creditorName', '')
            category = _assign_category(desc)

            entry_type = 'expense' if booking['transactionAmount']['amount'][0] == '-' else 'income'
            creditor = booking.get('creditorAccount', {}).get('iban', '')
            idx = 1 if entry_type == 'expense' else 0
            amount = float(booking['transactionAmount']['amount'][idx:])

            if creditor and creditor in trusted_accounts.keys():
                entry_type = 'transfer'

            account_type = booking.get('debtorAccount', {}).get('iban', '')
            new_transactions.append(Transaction(
                amount=amount, entry_type=entry_type, date=date, card=account_type, description=desc, category=category)
            )

    engine = connect_to_db()
    write_to_db(engine, new_transactions)
